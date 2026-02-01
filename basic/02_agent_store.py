from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[YFinanceTools()],
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

session_id = "finance-session"

# Turn 1: Analyze a stock
agent.print_response(
    "Give me a quick analysis of NVIDIA",
    session_id=session_id,
    stream=True,
)

# Turn 2: The agent remembers NVDA from turn 1
agent.print_response(
    "Compare that to AMD",
    session_id=session_id,
    stream=True,
)

# Turn 3: Ask based on full conversation
agent.print_response(
    "Which looks like the better investment?",
    session_id=session_id,
    stream=True,
)