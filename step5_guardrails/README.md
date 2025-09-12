# Input Guardrail

While making an input guardrail, keep in mind that the prompt is very important. The input guardrail needs to return True to stop.

``
return GuardrailFunctionOutput(
    output_info=result.final_output,
    tripwire_triggered=result.final_output.is_not_related   # if this True Agent not run
)

```


case 1:
i want that my agent is only answer math related question
input: `Who won yesterday’s match? The match was between Pakistan and India in cricket.`

```
class InputGuardrail(BaseModel):
    is_related: bool
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

    print(result.final_output.is_related) # False because input is not math related.

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_related
    )
```

so tripwire not triggered. agent run

case 2:
input: `Who won yesterday’s match? The match was between Pakistan and India in cricket.`

```
class InputGuardrail(BaseModel):
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

    print(result.final_output.is_not_related) # true 

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_not_related
    )




math_agent = Agent(
    name="Math Agent",
    instructions="you are a math expert. understand question defined question solve question step by step.",
    input_guardrails=[guardrail_agent]
)
```

not agent not run and this exception raise.
```
except InputGuardrailTripwireTriggered:
    print("Success! InputGuardrail triggered tripwire.")
```

