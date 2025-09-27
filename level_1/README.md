# 📝 Short Summary Notes

## 🔹 Prompt Engineering

* **Temperature** → randomness control

  * Low = same/focused, High = creative/unpredictable
* **Top-k** → only top *k* tokens kept
* **Top-p** → only tokens covering *p* probability kept
* **Safe system messages** → hide sensitive info, guide model safely
* **Chain of Thought (CoT)** → model shows reasoning step by step
* **Tree of Thoughts (ToT)** → multiple reasoning branches explored

---

## 🔹 Markdown

* **Clickable images + tooltips** → `[![alt](img.png "tooltip")](url)`
* **Numbered lists** → `1. item` → auto continues numbering
* **Bulleted lists** → `- item` or `* item`

---

## 🔹 Pydantic

* `@pydantic.dataclasses.dataclass` → like Python `dataclass` but with validation
* `BaseModel` → full validation + schema definition
* **Type hints** → auto validation + JSON schema
* **Agents** → can use dataclass as `output_type` for structured outputs

---

## 🔹 OpenAI Agents SDK

* **Concepts & defaults** → need model + instructions + tools; defaults: temp=1, top-p=1
* **Handoffs** → transfer run between agents; supports parameters + callbacks
* **Tool calls** → agent can invoke Python tools; SDK handles JSON repair if malformed
* **Dynamic instructions** → update agent context at runtime with new info
* **Guardrails** → safety checks (before input, during output, or blocking); tripwires stop unsafe runs
* **Tracing** →

  * *Trace* = whole run
  * *Span* = smaller step inside run (e.g. tool call)
* **Hooks** →

  * `RunHooks` = before/after full run
  * `AgentHooks` = finer control (per step/tool)
* **Exception handling** →

  * `MaxTurnsExceeded` (too many loops)
  * `ModelBehaviorError` (bad model output/tool misuse)
* **Runner methods** →

  * `run` → normal sync run
  * `run_sync` → blocking, for sync code
  * `run_streamed` → stream tokens + tool calls together
* **ModelSettings & resolve()** → merge defaults with overrides to produce final config
* **output_type** → define structured schema; strict → rejects malformed data
