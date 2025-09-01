import os

from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig
)

from dotenv import load_dotenv, find_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError ("Gemini api key is not set.")



# Step # 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Step # 2: Model
model = OpenAIChatCompletionsModel(
    openai_client=provider,
    model="gemini-2.0-flash"
)


# Step # 3: Config
run_config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True
)

