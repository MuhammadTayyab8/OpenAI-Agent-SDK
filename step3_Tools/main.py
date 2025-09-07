import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ModelSettings,
    RunHooks,
    function_tool
)

from openai.types.responses import ResponseTextDeltaEvent

from dotenv import load_dotenv

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

# Tools
@function_tool
async def add_number(a: int, b: int) -> int:
    """Add two number"""
    return a + b + 2



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
        print(f"Tool start: {tool}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"Tool end: {tool} with result: {result}")




# Agent
agent = Agent(
    name="Math Agent",
    instructions="you are a math agent",
    tools=[add_number]
)





async def main():
    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input="add 3 + 5 +2",
            run_config=run_config,
            hooks=CustomRunHook()
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    except Exception as e:
        print(f"Error: {str(e)}")
 
asyncio.run(main())