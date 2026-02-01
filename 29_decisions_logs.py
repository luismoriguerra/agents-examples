from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb
from agno.learn import LearningMachine, DecisionLogConfig
from agno.models.openai import OpenAIChat

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    id="my-agent",
    model=OpenAIChat(id="gpt-4o"),
    db=SqliteDb(db_file="tmp/29_decisions_logs.db"),
    learning=LearningMachine(
        decision_log=DecisionLogConfig(),
    ),
    instructions=[
        "When you make a significant choice, use log_decision to record it.",
        "Include your reasoning and alternatives you considered.",
    ],
)

agent.print_response(
    "I need help choosing between Python and JavaScript for web scraping.",
    session_id="session_1",
)

# View logged decisions
lm = agent.get_learning_machine()
lm.decision_log_store.print(agent_id="my-agent", limit=5)