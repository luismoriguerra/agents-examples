from agno.agent import Agent
from agno.tools.duckdb import DuckDbTools

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    tools=[DuckDbTools()],
    system_message="Use this file for Movies data: https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
)

agent.print_response("What is the average rating of movies?", markdown=True, stream=False)