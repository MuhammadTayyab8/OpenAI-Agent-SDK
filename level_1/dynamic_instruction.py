import os
import asyncio

from agents import (
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled,
    Agent,
    Runner,
    RunHooks,
    RunConfig,
    RunContextWrapper
)
from dotenv import load_dotenv


from pydantic import BaseModel

from openai.types.responses import ResponseTextDeltaEvent


#======================= env load ====================
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("API key is not defined.")



# ===================== step 1 gemini steps ===============
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ==================== step 2 Model ==========================

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash"
)

# ========================= Run Config =====================
run_config = RunConfig(
    model_provider=client,
    model=model,
    tracing_disabled=True
)



# =================== Hooks ====================

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


# =================== Hooks ====================


# ===== dynamic instruction ======
def get_dynamic_instructions(context: RunContextWrapper, agent: Agent) -> str:
    print(context, "CONTEXT")
    print("User role:", context.context.role)  # string field access
    if context.context.role.lower() == "customer":
        return "You are IT support Agent. your role to solve customer issue related to system."
    else:
        return "You are IT support Agent. you see if not customer in friendly manners sorry user and tell only allowed for IT Support. Must Not Answer to non customer"



billing_agent = Agent(
    name="Billing Agent",
    instructions="you are a billing agent at inotivex. your role to solve user billing related queries"
)

it_expert = Agent (
    name="IT Support",
    instructions=get_dynamic_instructions,
)

main_agent = Agent(
    name="Main Agent",
    instructions="""
    You are a front desk agent. Route queries to the correct specialist.
    - If billing/account related → handoff to Billing Agent
    - If software/system related → handoff to IT Support Agent
    """,
    handoffs=[billing_agent, it_expert]   # allowed handoffs
)



class UserInfo(BaseModel):
    name: str
    role: str

user_info = UserInfo(name="Tayyab", role="Guest")

async def main():
    try:
        result = Runner.run_streamed(
            starting_agent=main_agent,
            input="i need assitant on software bill print. its not working today.",
            run_config=run_config,
            context=user_info,
            hooks=CustomRunHook()
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    except Exception as e:
        print(f"Error: {str(e)}")
 
asyncio.run(main())