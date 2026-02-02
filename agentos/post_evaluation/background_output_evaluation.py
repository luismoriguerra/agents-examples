from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS

from dotenv import load_dotenv
load_dotenv()

# Setup database for agent and evaluation storage
db = AsyncSqliteDb(db_file="tmp/evaluation.db")

# Create the evaluator using Agent as Judge
evaluator = AgentAsJudgeEval(
    db=db,
    name="Response Quality Check",
    model=OpenAIResponses(id="gpt-5.2"),
    criteria="Response should be helpful, accurate, and well-structured",
    additional_guidelines=[
        "Evaluate if the response addresses the user's question directly",
        "Check if the information provided is correct and reliable",
        "Assess if the response is well-organized and easy to understand",
    ],
    threshold=7,
    run_in_background=True,  # Runs evaluation without blocking the response
)

# Create the main agent with Agent as Judge evaluation
main_agent = Agent(
    id="support-agent",
    name="CustomerSupportAgent",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "You are a helpful customer support agent.",
        "Provide clear, accurate, and friendly responses.",
        "If you don't know something, say so honestly.",
    ],
    db=db,
    post_hooks=[evaluator],  # Automatically evaluates each response
    markdown=True,
    debug_mode=True,
)

# Create AgentOS
agent_os = AgentOS(agents=[main_agent])
app = agent_os.get_app()


if __name__ == "__main__":
    agent_os.serve(app="background_output_evaluation:app", port=7777, reload=True)