from agno.learn import LearningMachine, SessionContextConfig

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.db.sqlite import SqliteDb

from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        session_context=SessionContextConfig(enable_planning=True),
    ),
    markdown=True,
    debug_mode=True,
)

agent.print_response(
    "Help me deploy a Python app to production. Give me the steps.",
    user_id="alice@example.com",
    session_id="deploy_app",
)

# Later, progress is tracked
agent.print_response(
    "Done with step 1. What's next?",
    user_id="alice@example.com",
    session_id="deploy_app",
)