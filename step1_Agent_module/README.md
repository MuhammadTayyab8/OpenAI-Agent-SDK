# Topic cover in this step

Agent
===

```
agent = Agent(
    name="name entity relations",
    instructions="you are a name entity agent. extract name entity relations from given text.",
)
```

Agents Hooks
===

Return not allowed here only print to show output.

```
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

```

Structure Output
===

```
# custom class in which you want to show output
class EntityOutput(BaseModel):
    name: str
    role: str


# in agent pass
agent = Agent(
    name="name entity relations",
    instructions="Extract person name and their role from the text.",
    hooks=CustomAgentHooks(),
    output_type=EntityOutput,
)


```

---

Setup MaxToken and Temperature
```
agent = Agent(
    name="name entity relations",
    instructions="you are a name entity agent. extract name entity relations from given text.",
    hooks=CustomAgentHooks(),
    model_settings=ModelSettings(
        temperature=0.1,  # Very focused
        max_tokens=500,    # Enough for detailed steps
        tool_choice="required"   # always use tools ( if not required also )
        
    )
)

```
