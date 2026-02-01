from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow
from agno.workflow.parallel import Parallel

# Create agents
news_researcher = Agent(name="News Researcher", tools=[HackerNewsTools()])
finance_researcher = Agent(name="Finance Researcher", tools=[YFinanceTools()])
writer = Agent(name="Writer")
reviewer = Agent(name="Reviewer")

# Create individual steps
research_news_step = Step(name="Research News", agent=news_researcher)
research_finance_step = Step(name="Research Finance", agent=finance_researcher)
write_step = Step(name="Write Article", agent=writer)
review_step = Step(name="Review Article", agent=reviewer)

# Create workflow with parallel research
workflow = Workflow(
    name="Content Creation Pipeline",
    steps=[
        Parallel(research_news_step, research_finance_step, name="Research Phase"),
        write_step,
        review_step,
    ],
)

workflow.print_response("Write about the latest AI developments and stock trends")