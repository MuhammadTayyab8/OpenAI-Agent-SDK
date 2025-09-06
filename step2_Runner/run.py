import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)

from dotenv import load_dotenv

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
    name="Application Writer",
    instructions="you are a expert application writer."
)


async def main():
    try:
        result = await Runner.run(
            starting_agent=agent,
            input="Write leave Application for college",
            run_config=run_config
        )

        print(result.final_output)

    except Exception as e:
        print(f"Error: {str(e)}")


asyncio.run(main())