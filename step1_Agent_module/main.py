import os

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    AgentHooks,
    ModelSettings
)

import asyncio

from openai.types.responses import ResponseTextDeltaEvent

from dotenv import load_dotenv, find_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError ("Gemini api key is not set.")



# Step # 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Step # 2: Model
model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model="gemini-2.0-flash"
)


# Step # 3: Config
run_config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True
)



# Hooks
class CustomAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        print( f"- Agent Start {agent.name}")
    
    async def on_end(self, context, agent, output):
        print( f"- Agent End {agent.name}")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print( f"- LLM Start with {agent.name}")
    
    async def on_llm_end(self, context, agent, response):
        print( f"- LLM End with {agent.name}")
    
    async def on_handoff(self, context, agent, source):
        print(f"HandsOff {agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"Agent {agent.name} Start tool: {tool}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"Agent {agent.name} End tool: {tool} and produce output: {result}")




# Agent
agent = Agent(
    name="name entity relations",
    instructions="you are a name entity agent. extract name entity relations from given text.",
    hooks=CustomAgentHooks(),
    model_settings=ModelSettings(
        temperature=0.1,  # Very focused
        max_tokens=500    # Enough for detailed steps
    )
)



async def main():
    try: 
        result = Runner.run_streamed(
            starting_agent=agent,
            input="My name is Aftab and i am going to Karachi tommorrow.",
            run_config=run_config
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta)

    except Exception as e:
        print(f"Error: {str(e)}")

asyncio.run(main())