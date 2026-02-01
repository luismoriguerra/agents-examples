from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.youtube_reader import YouTubeReader
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Create Knowledge Instance
knowledge = Knowledge(
    name="YouTube Knowledge Base",
    description="Knowledge base from YouTube video transcripts",
    vector_db=PgVector(
        table_name="youtube_vectors",
        db_url=db_url
    ),
)

# Add YouTube video content synchronously
knowledge.insert(
    metadata={"source": "youtube", "type": "educational"},
    urls=[
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Replace with actual educational video
        "https://www.youtube.com/watch?v=example123"   # Replace with actual video URL
    ],
    reader=YouTubeReader(),
)

# Create an agent with the knowledge
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

# Query the knowledge base
agent.print_response(
    "What are the main topics discussed in the videos?",
    markdown=True
)