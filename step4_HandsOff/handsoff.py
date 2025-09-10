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
    FunctionTool,
    handoff
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
    print("Call")
    print(f"context: {context} \n agent: {agent} \n")
    return context.context.get("user_role") == "admin"


# Tools
@function_tool(is_enabled=is_admin_check)
async def add_number(a: int, b: int) -> int:
    """Add two number"""
    return a + b + 3



@function_tool
async def accounts_department(invoice_number: str) -> dict:
    """find invoice by invoice number and make a copy"""
    try:
        prompt = f"Generate invoice data aganist {invoice_number} add all information dummy. the invoice must be in markdown code make code clean"

        response = await provider.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": prompt}]
        )

        invoice_data = response.choices[0].message.content.strip()
        return {"invoice": invoice_data}
    except Exception as e:
        print(f"Error: {str(e)}")




# Hooks
class CustomRunHook(RunHooks):
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"LLM start with {agent.name}")
        for h in agent.handoffs:
            print(f" -> HANDOFF TOOL name: {h}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"LLM end with {agent.name}")

    async def on_agent_start(self, context, agent):
        print(f"Agent Start: {agent.name}")
        for h in agent.handoffs:
            print(f" -> HANDOFF TOOL name: {h}")

    async def on_agent_end(self, context, agent, output):
        print(f"Agent End: {agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"Tool start: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"Tool end: {tool.name} with result: {result}")

    async def on_handoff(self, context, from_agent, to_agent):
        print(f"Handsoff from {from_agent.name} to: {to_agent.name}")




class InputData(BaseModel):
    reason: str
    order_id: str



# HandsOff 
async def agents_handsoff(ctx: RunContextWrapper, input_data: InputData) -> str:
    print(f"Escalating order {input_data.order_id} because: {input_data.reason}")



# Agent
# ===================== customer agent ===================== 

customer_agent = Agent(
    name="Customer Agent",
    instructions="You are a customer support agent. Deal customer with friendly way.",
)

customer_agent_handsoff = handoff(
    agent=customer_agent,
    on_handoff=agents_handsoff,
    input_type=InputData
)

# ===================== customer agent ===================== 



it_department_agent = Agent(
    name="IT Department Agent",
    instructions="you are an it department agent. entertain customer technical queries."
)





# ==================== Custom Handoff Account Agent with Logging ====================

accounts_agent = Agent(
    name="Accounts Agent",
    instructions="""
    You are an accounts agent. 
    Always use the tool `accounts_department` to fetch invoice details 
    when the user asks about billing, payments, or invoices. 
    Return the tool output directly.
    """,
    tools=[accounts_department]
)


def log_accounts_handoff(ctx: RunContextWrapper, input_data: InputData) -> str:
    print(f"[HANDOFF LOG] Transferring to Accounts Agent because {input_data.reason}")


accounts_handoff = handoff(
    agent=accounts_agent,
    # tool_name_override="escalate_to_accounts",
    # tool_description_override="Use this when user asks about billing, invoices, or payments.",
    on_handoff=log_accounts_handoff,
    input_type=InputData
)

# ==================== Custom Handoff Account Agent with Logging ====================



main_agent = Agent(
    name="Main Agent",
    instructions="""
    you are a main agent your role here is like an manager understand user question and handsoff to 
    specilist agent
    - user question is related to accounts, billing, payment must handsoff to `accounts_agent`.
    - user question related to technical issues handsoff to `it_department_agent`.
    - user question related to normal support desk level question then handsoff to `customer_agent`.
    - if you cannot specify the agent according to question so let the `customer_agent` agent to 
    entertain customer.
    """,
    handoffs=[customer_agent_handsoff, it_department_agent, accounts_handoff]
)


class UserContext(BaseModel):
    user_role: str



async def main():
    try:
        # userData = RunContextWrapper({"user_role": "admin", "name": "Tayyab"})

        result = Runner.run_streamed(
            starting_agent=main_agent,
            input="I lost my invoice, please send billing details or if possible send a copy. my name is Aftab and invoice number is SI-00091",
            run_config=run_config,
            hooks=CustomRunHook(),
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