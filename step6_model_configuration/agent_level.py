import os
import asyncio

from agents import (
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled,
    Agent,
    Runner,
    RunHooks
)

from dotenv import load_dotenv



#======================= env load ====================
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("API key is not defined.")


#======================= env load ====================



set_tracing_disabled(disabled=True)


# step 1: provider called it client
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



# Hooks
class CustomRunHook(RunHooks):
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"LLM start with {agent.name}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"LLM end with {agent.name}")

    async def on_agent_start(self, context, agent):
        print(f"Agent Start: {agent.name}")
        # for h in agent.handoffs:
        #     print(f" -> HANDOFF TOOL name: {h}")

    async def on_agent_end(self, context, agent, output):
        print(f"Agent End: {agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"Tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"Tool end: {tool.name} with result: {result}")

    async def on_handoff(self, context, from_agent, to_agent):
        print(f"Handsoff from {from_agent.name} to: {to_agent.name}")
        print("---- Conversation passed to new agent ----")
        print(context.context)
        print("-----------------------------------------")





# agent
agent = Agent(
    name="Math Agent",
    instructions="You are a math agent. solve math question step by step.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
)



async def main():
    try:
        result = await Runner.run(
            starting_agent=agent,
            input="What is the sum of 2+2+4. and then the answer * 4. then answer-8",
            hooks=CustomRunHook()
        )

        print(result.final_output)

    except Exception as e:
        print(f"Error: {str(e)}")


asyncio.run(main())