# **OpenAI Agent SDK Course**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white, "Python")
![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI-API-green?logo=openai&logoColor=white, "OpenAI Agents SDK")

[![Gemini Badge](https://img.shields.io/badge/Gemini-AI-blue "Google Gemini - Click to Learn More")](https://gemini.google.com/)


OpenAI Agent SDK is a **Python library** designed for building intelligent agents using OpenAI models.
This repository contains a **complete step-by-step course** on creating agents, integrating tools, managing memory, and advanced agent workflows.

---

## **What Here**

* How to **set up the environment** for OpenAI SDK
* How to **work with APIs** and configure models
* Building **basic and advanced agents**
* Adding **tools, memory, and structured outputs**
* Implementing **guardrails and lifecycle management**
* **Streaming, cloning agents, and UI integration** with Chainlit
* Deploying agents and using external tracing providers

---

## 🛠 **Basic Setup**

### **1. Install UV (Virtual Environment Tool)**

UV is a fast virtual environment and dependency management tool. Install UV by running:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### **2. Create and Activate Virtual Environment**

Inside your project folder:

```bash
uv venv
```

Activate the environment:

* **Windows**:

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux**:

  ```bash
  source venv/bin/activate
  ```

---

### **3. Install Dependencies**

```bash
uv add openai-agents chainlit python-dotenv
```

---

### **4. Get API Key**

1. Go to **Google AI Studio** → [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Generate an **API key**
3. Add it to your `.env` file:

```
GEMINI_API_KEY="AI..........."
```

---

### **5. Base URL for Gemini (OpenAI-Compatible)**

Copy the Base URL from:
[https://ai.google.dev/gemini-api/docs/openai](https://ai.google.dev/gemini-api/docs/openai)
Add to `.env`:

```
BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
```

---

# Agent SDK Topics Table

| **Category**               | **Topics** |
|-----------------------------|------------|
| **Agent System**            | Agent, AgentHooks, AgentOutputSchema, AgentOutputSchemaBase |
| **Runner and Execution**    | Runner, run, run_sync, run_streamed, RunConfig, RunHooks, RunResult, RunResultStreaming, RunContextWrapper, RunErrorDetails, Tools |
| **Tool Types**              | Tool, function_tool, FunctionTool, FunctionToolResult, WebSearchTool, FileSearchTool, ComputerTool, CodeInterpreterTool, ImageGenerationTool, LocalShellTool, LocalShellCommandRequest, LocalShellExecutor, HostedMCPTool |
| **Handoffs**                | handoff, Handoff, HandoffInputData, HandoffInputFilter |
| **Input Guardrails**        | input_guardrail, InputGuardrail, InputGuardrailResult, InputGuardrailTripwireTriggered |
| **Output Guardrails**       | output_guardrail, OutputGuardrail, OutputGuardrailResult, OutputGuardrailTripwireTriggered, GuardrailFunctionOutput |
| **Models and Providers**    | Model, ModelProvider, ModelTracing, ModelSettings, OpenAIChatCompletionsModel, OpenAIResponsesModel, OpenAIProvider |
| **Streaming and Events**    | StreamEvent, RunItemStreamEvent, AgentUpdatedStreamEvent, RawResponsesStreamEvent |
| **Items and Data Structures** | TResponseInputItem, MessageOutputItem, ModelResponse, RunItem, HandoffCallItem, HandoffOutputItem, ToolCallItem, ToolCallOutputItem, ReasoningItem, ItemHelpers |
| **Tracing and Observability - Core Tracing** | trace, Trace, TracingProcessor, add_trace_processor, set_trace_processors, set_tracing_disabled |
| **Tracing and Observability - Spans** | Span, SpanData, SpanError, agent_span, custom_span, function_span, generation_span, guardrail_span, handoff_span |
| **Tracing and Observability - Span Data Types** | AgentSpanData, CustomSpanData, FunctionSpanData, GenerationSpanData, GuardrailSpanData, HandoffSpanData |
| **Computer Use**            | Computer, AsyncComputer, Environment, Button |
| **Exceptions**              | AgentsException, MaxTurnsExceeded, ModelBehaviorError, UserError |



---

# Modules

| Module | Topic                    | Description                     |
| ------ | ------------------------ | ------------------------------- |
| 00     | **Swarm**                | Multi-agent orchestration       |
| 01     | **UV**                   | Setup environment using UV      |
| 02     | **What is API**          | Understanding APIs              |
| 03     | **Get API Key**          | Generate and secure API key     |
| 04     | **Hello Agent**          | Your first agent                |
| 05     | **Model Configuration**  | Configure OpenAI models         |
| 06     | **Basic Tools**          | Add simple tools                |
| 07     | **Model Settings**       | Advanced model options          |
| 08     | **Local Context**        | Context injection               |
| 09     | **Dynamic Instructions** | Change instructions dynamically |
| 10     | **Streaming**            | Real-time responses             |
| 11     | **Agent Clone**          | Clone agents                    |
| 12     | **Basic Tracing**        | Debug and trace agents          |
| 13     | **Agents as Tool**       | Agents working as tools         |
| 14     | **Basic Handoff**        | Simple handoff between agents   |
| 15     | **Advanced Tools**       | Complex tool integration        |
| 16     | **Advanced Handoffs**    | Multi-agent workflows           |
| 17     | **Structured Output**    | JSON and schema validation      |
| 18     | **Guardrails**           | Control and safety              |
| 19     | **Agent Lifecycle**      | Lifecycle stages                |
| 20     | **Run Lifecycle**        | Managing runs                   |
| 21     | **Session Memory**       | Short-term memory               |
| 22     | **Memory Management**    | Advanced memory handling        |
| 23     | **Custom Runner**        | Build your runner               |
| 24     | **External Tracing**     | Langfuse / OpenTelemetry        |
| 25     | **Chainlit**             | Build UI for agents             |
