from typing import Optional, List, Any
from app.agents.core import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool, ManagedAgent, ToolCallingAgent
from app.tools import *

from flask import current_app

class StockAgent:

    def __init__(self) -> None:
        config = current_app.config if current_app else {}
        self.debug = config.get("DEBUG", True)
        self.max_iterations = config.get("MAX_ITERATIONS", 10)
        self.used_packages = []
        self.model_id = LiteLLMModel("deepseek/deepseek-chat", api_key="sk-994e446ef21d432388f30ceae8149501")
        self.web_agent = ToolCallingAgent(
            tools=[VisitWebpageTool(), DuckDuckGoSearchTool()],
            model=self.model_id,
        )
        self.managed_web_agent = ManagedAgent(
            agent=self.web_agent,
            name="search",
            description="Runs web searches for you. Give it your query as an argument.",
        )

        self.trader = CodeAgent(
            tools=self.registerAllTools(),
            model=self.model_id,
        )
        self.managed_trader_agent: ManagedAgent = ManagedAgent(
            agent=self.trader,
            name="trader",
            description="Use to fetch market data, place orders, retrieve orders, get assets, check asset tradability, and more.",
        )

        self.manager = CodeAgent(
            tools=[],
            model=self.model_id,
            managed_agents=[self.managed_web_agent, self.managed_trader_agent],
            additional_authorized_imports=self.used_packages,
        )

    def run(self, task: Optional[str] = None) -> Any:
        if not task:
            raise ValueError("Task must be provided.")
        return self.manager.run(task)

    def registerAllTools(self) -> List[Any]:
        return [
            AnalystRecommendationsTool(),
            CompanyInfoTool(),
            CompanyNewsTool(),
            HistoricalStockPricesTool(),
            IncomeStatementTool(),
            KeyFinancialRatiosTool(),
            StockFundamentalsTool(),
            StockPriceTool(),
            TechnicalIndicatorsTool(),
            TickerByNameTool(),
            MarketOrderTool(),
            LimitOrderTool(),
            ShortOrderTool(),
            ClientOrderIDTool(),
            BracketOrderTool(),
            TrailingStopOrderTool(),
            RetrieveOrdersTool(),
            CheckAssetTradabilityTool(),
            AccountInfoTool(),
            PortfolioGainLossTool(),
            PortfolioTool(),
            StockPricePredictorTool(),
        ]
