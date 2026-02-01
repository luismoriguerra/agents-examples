import random

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools import tool

from dotenv import load_dotenv
load_dotenv()

def get_weather(city: str) -> str:
    """Get the weather for the given city.

    Args:
        city (str): The city to get the weather for.
    """

    # In a real implementation, this would call a weather API
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    random_weather = random.choice(weather_conditions)

    return f"The weather in {city} is {random_weather}."

# To equipt our Agent with our tool, we simply pass it with the tools parameter
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[get_weather],
    markdown=True,
    debug_mode=True,
)

# Our Agent will now be able to use our tool, when it deems it relevant
agent.print_response("What is the weather in San Francisco?", stream=True)