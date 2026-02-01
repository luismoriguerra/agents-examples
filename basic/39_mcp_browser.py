import asyncio
import os
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.mcp import MCPTools

from dotenv import load_dotenv
load_dotenv()


async def run_agent(message: str) -> None:
    # Environment variables for browserbase MCP server
    env = {
        **os.environ,
        "BROWSERBASE_API_KEY": os.getenv("BROWSERBASE_API_KEY"),
        "BROWSERBASE_PROJECT_ID": os.getenv("BROWSERBASE_PROJECT_ID"),
    }

    # Use npx to run the browserbase MCP server directly
    mcp_tools = MCPTools(
        command="npx @browserbasehq/mcp-server-browserbase",
        env=env,
        timeout_seconds=60,
    )
    await mcp_tools.connect()

    try:
        agent = Agent(
            model=OpenAIResponses(id="gpt-5.2"),
            tools=[mcp_tools],
            instructions=dedent("""\
                You are a web scraping assistant that creates concise reader's digests from Hacker News.

                CRITICAL INITIALIZATION RULES - FOLLOW EXACTLY:
                1. NEVER use screenshot tool until AFTER successful navigation
                2. ALWAYS start with stagehand_navigate first
                3. Wait for navigation success message before any other actions
                4. If you see initialization errors, restart with navigation only
                5. Use stagehand_observe and stagehand_extract to explore pages safely

                Available tools and safe usage order:
                - stagehand_navigate: Use FIRST to initialize browser
                - stagehand_extract: Use to extract structured data from pages
                - stagehand_observe: Use to find elements and understand page structure
                - stagehand_act: Use to click links and navigate to comments
                - screenshot: Use ONLY after navigation succeeds and page loads

                Your goal is to create a comprehensive but concise digest that includes:
                - Top headlines with brief summaries
                - Key themes and trends
                - Notable comments and insights
                - Overall tech news landscape overview

                Be methodical, extract structured data, and provide valuable insights.
            """),
            markdown=True,
            debug_mode=True,
        )
        await agent.aprint_response(message, stream=True)
    finally:
        # Always close the connection when done
        await mcp_tools.close()


if __name__ == "__main__":
    asyncio.run(
        run_agent(
            "Create a comprehensive Hacker News Reader's Digest from https://news.ycombinator.com"
        )
    )