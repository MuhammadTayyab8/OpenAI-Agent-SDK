import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ModelSettings,
    RunHooks,
    function_tool,
    StopAtTools,
    RunContextWrapper,
    FunctionTool
)

from openai.types.responses import ResponseTextDeltaEvent

from dotenv import load_dotenv

from pydantic import BaseModel
from dataclasses import dataclass

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
    model="gemini-2.5-flash"
)

# Step: 3 Config
run_config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True,
)






# ================================================= Code ===========================================================


def is_admin_check(context: RunContextWrapper, agent: Agent) -> bool:
    return context.context.get("user_role") == "admin"


# Tools
@function_tool(is_enabled=is_admin_check)  # True so continue
async def add_number(a: int, b: int) -> int:
    """Add two number"""
    return a + b + 3



# Hooks
class CustomRunHook(RunHooks):
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"LLM start with {agent.name}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"LLM end with {agent.name}")

    async def on_agent_start(self, context, agent):
        print(f"Agent Start: {agent.name}")

    async def on_agent_end(self, context, agent, output):
        print(f"Agent End: {agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"Tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"Tool end: {tool.name} with result: {result}")




# Agent
agent = Agent(
    name="Math Agent",
    instructions="you are a math agent",
    tools=[add_number],
    tool_use_behavior="stop_on_first_tool"
    # tool_use_behavior=StopAtTools(stop_at_tool_names=["add_number"])
)



class UserContext(BaseModel):
    user_role: str



async def main():
    try:
        userData = {
         "user_role": "admin"   
        }
        # userData = RunContextWrapper({"user_role": "admin", "name": "Tayyab"})

        result = Runner.run_streamed(
            starting_agent=agent,
            input="add 4 + 6",
            run_config=run_config,
            context=userData,
            hooks=CustomRunHook(),
            # max_turns=2
            # max_turns=2
        )

        async for event in result.stream_events():
            # print(f"\n event: {event} \n")
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                # print("Think... \n response.")
                print(event.data.delta, end="", flush=True)

            # Agar tool ka output aaya hai
            # if event.type == "run_item_stream_event" and event.name == "tool_output":
                
            #     print("\n[Tool Output]:", event.item.output)

        # Final result after streaming
        # final_result = await result.get_final_result()
        # print("\n\nFinal Output:", result.final_output)   # yaha 11 aayega


    except Exception as e:
        print(f"Error: {str(e)}")
 
asyncio.run(main())