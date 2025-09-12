import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunHooks,
    RunContextWrapper,
    input_guardrail,
    TResponseInputItem,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    output_guardrail,
    OutputGuardrailTripwireTriggered
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



# ============= InputGuardrail ============= 
class InputGuardrail(BaseModel):
    is_related: bool
    reason: str


class OutputGuardrail(BaseModel):
    is_not_related: bool
    reason: str



input_guardrail_agent = Agent(
    name="Application Policy",
    instructions="check if user ask is not related to math.",
    output_type=InputGuardrail
)



@input_guardrail
async def guardrail_agent(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> bool:
    
    result = await Runner.run(
        starting_agent=input_guardrail_agent,
        input=input,
        run_config=run_config,
        context=ctx.context
    )

    print(result.final_output.is_related, "Input")

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_related
    )




# =================== Output Guardrail ====================
output_guardrail_agent = Agent(
    name="Output Check Agent",
    instructions="check if the response include math related output.",
    output_type=OutputGuardrail
)


@output_guardrail
async def output_guardrail_run(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> bool:
    
    result = await Runner.run(
        starting_agent=output_guardrail_agent,
        input=input,
        run_config=run_config,
        context=ctx.context
    )

    print(result.final_output.is_not_related, "Output")

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_related
    )






math_agent = Agent(
    name="Math Agent",
    instructions="you are a math expert. understand question defined question solve question step by step.",
    input_guardrails=[guardrail_agent],
    output_guardrails=[output_guardrail_run]
)









async def main():
    try:
        # userData = RunContextWrapper({"user_role": "admin", "name": "Tayyab"})

        result = await Runner.run(
            starting_agent=math_agent,
            input="Who won yesterday’s match? The match was between Pakistan and India in cricket.",
            run_config=run_config,
            hooks=CustomRunHook(),
            # max_turns=3
        )

        print(result.final_output)

        # async for event in result.stream_events():
        #     # print(f"\n event: {event} \n")
        #     if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
        #         # print("Think... \n response.")
        #         print(event.data.delta, end="", flush=True)

            # Agar tool ka output aaya hai
            # if event.type == "run_item_stream_event" and event.name == "tool_output":
                
            #     print("\n[Tool Output]:", event.item.output)

        # Final result after streaming
        # final_result = await result.get_final_result()
        # print("\n\nFinal Output:", result.final_output)   # yaha 11 aayega

    except InputGuardrailTripwireTriggered:
        print("Success! InputGuardrail triggered tripwire.")

    except OutputGuardrailTripwireTriggered as e:
        print("Success! OutputGuardrail triggered tripwire.")


    except Exception as e:
        print(f"Error: {str(e)}")

 
asyncio.run(main())