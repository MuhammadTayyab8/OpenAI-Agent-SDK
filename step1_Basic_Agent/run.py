from agents import(
    Agent,
    Runner
)

from setup_config import run_config

import asyncio


agent = Agent(
    name="Text Classification",
    instructions=""""
    You are a text classification agent.
    you can update sentiment based on text
    """
)




async def main():

    try:
        result = await Runner.run(
            starting_agent=agent,
            input="I Love OpenAI SDK.",
            run_config=run_config
        )

        print(f"Agent Answer: {result.final_output}")

    except Exception as e:
        print(f"Error: {str(e)}")


asyncio.run(main())