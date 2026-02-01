import asyncio

from agno.agent import Agent
from agno.knowledge.embedder.cohere import CohereEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.cohere import CohereReranker
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.models.openai import OpenAIResponses
from dotenv import load_dotenv
load_dotenv()

# Create knowledge base with hybrid search and reranking
knowledge = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=CohereEmbedder(id="embed-v4.0"),
        reranker=CohereReranker(model="rerank-v3.5"),
    ),
)

# Load content
asyncio.run(
    knowledge.ainsert(url="https://docs.agno.com/agents/overview.md")
)

# Create agent with knowledge
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    knowledge=knowledge,
    search_knowledge=True,
    instructions=[
        "Search your knowledge before answering.",
        "Include sources in your response.",
    ],
    markdown=True,
    debug_mode=True,
)

agent.print_response("What are Agents?", stream=True)