from typing import Any, Dict

from agno.agent import Agent
from agno.tools import Toolkit

from dotenv import load_dotenv
load_dotenv()

try:
    import httpx
except ImportError:
    raise ImportError("`httpx` not installed. Run `uv pip install httpx`")


class APITools(Toolkit):
    def __init__(self, base_url: str, timeout: float = 30.0, **kwargs):
        self.base_url = base_url
        self.timeout = timeout

        # Sync tools for agent.run() and agent.print_response()
        tools = [
            self.fetch_data,
            self.post_data,
        ]

        # Async tools for agent.arun() and agent.aprint_response()
        # Format: (async_method, "tool_name")
        async_tools = [
            (self.afetch_data, "fetch_data"),
            (self.apost_data, "post_data"),
        ]

        super().__init__(name="api_tools", tools=tools, async_tools=async_tools, **kwargs)

    # Sync methods
    def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Fetch data from an API endpoint.

        Args:
            endpoint: The API endpoint to fetch data from (e.g., "/users/123")
        Returns:
            The JSON response from the API
        """
        url = f"{self.base_url}{endpoint}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    def post_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post data to an API endpoint.

        Args:
            endpoint: The API endpoint to post data to
            data: The data to post as JSON
        Returns:
            The JSON response from the API
        """
        url = f"{self.base_url}{endpoint}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    # Async methods (used automatically in async contexts)
    async def afetch_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Fetch data from an API endpoint asynchronously.

        Args:
            endpoint: The API endpoint to fetch data from (e.g., "/users/123")
        Returns:
            The JSON response from the API
        """
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def apost_data(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post data to an API endpoint asynchronously.

        Args:
            endpoint: The API endpoint to post data to
            data: The data to post as JSON
        Returns:
            The JSON response from the API
        """
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

# Create the agent with the toolkit (using JSONPlaceholder - a free fake API for testing)
agent = Agent(tools=[APITools(base_url="https://jsonplaceholder.typicode.com")], markdown=True)

# Sync usage - uses fetch_data
agent.print_response("Fetch the user with ID 1")

# Async usage - uses afetch_data automatically
import asyncio
asyncio.run(agent.aprint_response("Fetch the post with ID 1"))