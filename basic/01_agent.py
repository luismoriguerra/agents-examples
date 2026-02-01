from typing import List, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel, Field


from dotenv import load_dotenv
load_dotenv()

class StockAnalysis(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Full company name")
    current_price: float = Field(..., description="Current price in USD")
    pe_ratio: Optional[float] = Field(None, description="P/E ratio")
    summary: str = Field(..., description="One-line summary")
    key_drivers: List[str] = Field(..., description="2-3 key growth drivers")
    key_risks: List[str] = Field(..., description="2-3 key risks")


agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[YFinanceTools()],
    output_schema=StockAnalysis,
    debug_mode=True,
)

response = agent.run("Analyze NVIDIA stock")

# Access typed data directly
analysis: StockAnalysis = response.content
print(f"{analysis.company_name} ({analysis.ticker})")
print(f"Price: ${analysis.current_price}")
print(f"P/E Ratio: {analysis.pe_ratio or 'N/A'}")
print(f"Summary: {analysis.summary}")
print("Key Drivers:")
for driver in analysis.key_drivers:
    print(f"  - {driver}")
print("Key Risks:")
for risk in analysis.key_risks:
    print(f"  - {risk}")
