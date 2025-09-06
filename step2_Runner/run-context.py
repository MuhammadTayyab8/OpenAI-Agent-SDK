import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ModelSettings,
    RunHooks,
    RunContextWrapper,
    function_tool
)

from dataclasses import dataclass

from openai.types.responses import ResponseTextDeltaEvent

from dotenv import load_dotenv

from pydantic import BaseModel

import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("API key is not defined.")


# step: 1 provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
) 

# Step: 2 Model
model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model="gemini-2.0-flash"
)

# Step: 3 Config
run_config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True,
)






# ================================================= Code ===========================================================

# Hooks
class CustomRunHook(RunHooks):
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"====================== {agent, system_prompt, input_items} ========================")
        print(f"LLM start with {agent.name}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"====================== {context, agent, response} ========================")
        print(f"LLM end with {agent.name}")

    async def on_agent_start(self, context, agent):
        print(f"Agent Start: {agent.name}")

    async def on_agent_end(self, context, agent, output):
        print(f"Agent End: {agent.name}")


# Context
@dataclass
class UserData:
    name: str
    age: int
    location: str





@function_tool
async def fetch_data(context: RunContextWrapper[UserData]) -> str:
    """Tool to get user data name, age and location"""
    return f"My Name is {context.context.name}, my age is {context.context.age} and i am live at {context.context.location}"



# Agent
agent = Agent(
    name="Essay Writer",
    instructions="""you are a essay writer. understand topic make 5 headings according to topic 
    must add introduction and conclusion. Must use tool if user ask is not related to essay""",
    tools=[fetch_data]
)



# runner
async def main():
    try:

        user_data = UserData("tayyab", 17, "Karachi, Pakistan")

        result = Runner.run_streamed(
            starting_agent=agent,
            input="What is my name and age. please write name and age only",
            run_config=run_config,
            context=user_data
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    except Exception as e:
        print(f"Error: {str(e)}")


asyncio.run(main())