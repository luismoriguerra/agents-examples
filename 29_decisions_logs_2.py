from agno.learn import LearningMachine, LearningMode, DecisionLogConfig

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.learn import LearningMachine, DecisionLogConfig
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/29_decisions_logs_2.db")

agent = Agent(
    id="my-agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    learning=LearningMachine(
        decision_log=DecisionLogConfig(mode=LearningMode.ALWAYS),
    ),
    tools=[DuckDuckGoTools()],
)

agent.print_response("What are the latest developments in AI agents?")
# Tool calls are automatically recorded as decisions