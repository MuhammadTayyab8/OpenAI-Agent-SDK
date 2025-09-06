import os

from agents import (
    Agent,
    Runner,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    ModelSettings
)

from openai.types.responses import ResponseTextDeltaEvent

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
    tracing_disabled=True,
)





# ================================================= Code ===========================================================
agent = Agent(
    name="Application Writer",
    instructions="you are a expert application writer.",
    model_settings=ModelSettings(
        temperature=0.1,  # Very focused
        max_tokens=500    # Enough for detailed steps
    )
)


async def main():
    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input="write sick leave for school",
            run_config=run_config
        )

        async for event in result.stream_events():
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    except Exception as e:
        print(f"Error: {str(e)}")
 
asyncio.run(main())