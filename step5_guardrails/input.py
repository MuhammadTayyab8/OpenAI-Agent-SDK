import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunHooks,
    function_tool,
    RunContextWrapper,
    handoff,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    TResponseInputItem,
    input_guardrail,
)

from openai.types.responses import ResponseTextDeltaEvent

from agents.extensions import handoff_filters

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



# ======================= handsoff input ======================
class InputData(BaseModel):
    reason: str
    order_id: str


# =========================== Guarduail ============================
class GuardrailInput(BaseModel):
    is_related: bool
    reason: str


# ======================= Guardrail Agent Start =============================
input_guardrail_agent = Agent(
    name="Input Guardrail",
    instructions="Check if user question is related to software support, it consultancy, company related question",
    output_type=GuardrailInput
)


@input_guardrail
async def input_guardrail_run(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    print(f"Guard run with {agent.name}")
    try:
        result = await Runner.run(
            starting_agent=input_guardrail_agent,
            input=input,
            run_config=run_config,
            context=ctx.context
        ) 

        print(result.final_output, "final output")

        return GuardrailFunctionOutput(
            output_info=result.final_output,
            tripwire_triggered=result.final_output.is_related
        )

    except Exception as e:
        print(f"Error input: {str(e)}")




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



main_agent = Agent(
    name="Main Agent",
    instructions="""
    you are a main agent of an software company your role here is like an manager understand user question and handsoff to 
    specilist agent
    - user question is related to accounts, billing, payment must handsoff to `accounts_agent`.
    - user question related to technical issues handsoff to `it_department_agent`.
    - user question related to normal support desk level question then handsoff to `customer_agent`.
    """,
    handoffs=[customer_agent_handsoff, it_department_agent],
    input_guardrails=[input_guardrail_run]
)


class UserContext(BaseModel):
    user_role: str



async def main():
    try:
        # userData = RunContextWrapper({"user_role": "admin", "name": "Tayyab"})

        result = Runner.run_streamed(
            starting_agent=main_agent,
            input="solve 2x^2+3x+1 = 0",
            run_config=run_config,
            hooks=CustomRunHook(),
            # max_turns=3
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
    except InputGuardrailTripwireTriggered:
        print(f"Fire, Input Triger fire.")
 
asyncio.run(main())