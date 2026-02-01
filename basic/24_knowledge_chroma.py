from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

from dotenv import load_dotenv
load_dotenv()

# Create a knowledge base
knowledge = Knowledge(
    vector_db=ChromaDb(collection="docs", path="tmp/24_chromadb", persistent_client=True),
)

# Load content
knowledge.insert(url="https://docs.agno.com/introduction.md")

# Create an agent that searches the knowledge base
agent = Agent(knowledge=knowledge, search_knowledge=True)
agent.print_response("What is Agno?")