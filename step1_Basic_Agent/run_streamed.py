from agents import(
    Agent,
    Runner
)

from setup_config import run_config

from openai.types.responses import ResponseTextDeltaEvent

import asyncio


agent = Agent(
    name="Text Classification",
    instructions=""""
    You are a article writer agent.
    you can write article in easy words.
    - about toipc introduction.
    - background of topic
    - current position of topic
    - future scope of topic
    """
)





async def main():

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input="Write Article on OpenAI SDK",
            run_config=run_config
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)


    except Exception as e:
        print(f"Error: {str(e)}")


asyncio.run(main())