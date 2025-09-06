import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)

from dotenv import load_dotenv

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
    model="gemini-2.0-flash"
)

# Step: 3 Config
run_config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True
)





# ================================================= Code ===========================================================
agent = Agent(
    name="Assistant",
    instructions="you are a math expert"
)


result = Runner.run_sync(
    agent,
    input="Solve 2x+3x^2+1 = 0 make data, solution, result headings use math languages and english",
    run_config=run_config
)

print(f"Answer: {result.final_output}")



