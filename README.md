# **OpenAI Agent SDK Course**

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
pip install openai chainlit python-dotenv
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

## **Roadmap**

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
