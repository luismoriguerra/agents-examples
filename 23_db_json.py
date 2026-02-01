from agno.agent import Agent
from agno.db.json import JsonDb
from agno.models.openai import OpenAIResponses
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv
load_dotenv()

# Setup the JSON database
db = JsonDb(db_path="tmp/json_db")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    tools=[HackerNewsTools()],
    add_history_to_context=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")