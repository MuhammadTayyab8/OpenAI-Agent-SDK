from agents import(
    Agent,
    Runner
)

from setup_config import run_config


agent = Agent(
    name="Text Classification",
    instructions=""""
    You are a text classification agent.
    you can update sentiment based on text
    """
)


try:
    result = Runner.run_sync(
        starting_agent=agent,
        input="I Love OpenAI SDK.",
        run_config=run_config
    )

    print(result.final_output)

except Exception as e:
    print(f"Error: {str(e)}")
