from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint

from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/agents_memory.db")

memory_manager = MemoryManager(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
)

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[YFinanceTools()],
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    markdown=True,
)

user_id = "investor@example.com"

# Tell the agent about yourself
agent.print_response(
    "I'm interested in AI and semiconductor stocks. My risk tolerance is moderate.",
    user_id=user_id,
    stream=True,
)

# The agent now knows your preferences
agent.print_response(
    "What stocks would you recommend for me?",
    user_id=user_id,
    stream=True,
)

# View stored memories
memories = agent.get_user_memories(user_id=user_id)
print("\nStored Memories:")
pprint(memories)