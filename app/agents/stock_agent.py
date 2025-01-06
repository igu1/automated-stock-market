import os
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool, ManagedAgent, ToolCallingAgent
from app.tools import *
from flask import current_app


class StockAgent:
    def __init__(self):
        config = current_app.config if current_app else {}
        self.debug = config.get("DEBUG", True)
        self.max_iterations = config.get("MAX_ITERATIONS", 10)
        self.used_packages = []
        if not self.debug:
            self.model_id = LiteLLMModel("deepseek/deepseek-coder")
        else:
            self.model_id = LiteLLMModel("gemini/gemini-2.0-flash-exp")
        self.web_agent: ToolCallingAgent = ToolCallingAgent(
            tools=[VisitWebpageTool(), DuckDuckGoSearchTool()],
            model=self.model_id,
            max_iterations=self.max_iterations,
        )
        self.managed_web_agent: ManagedAgent = ManagedAgent(
            agent=self.web_agent,
            name="search",
            description="Runs web searches for you. Give it your query as an argument.",
        )

        self.trader: CodeAgent = CodeAgent(
            tools=self.registerAllTools(),
            model=self.model_id,
            max_iterations=self.max_iterations,
        )
        self.managed_trader_agent: ManagedAgent = ManagedAgent(
            agent=self.trader,
            name="trader",
            description="Use to fetch market data, place orders, retrieve orders, get assets, check asset tradability, and more.",
        )

        self.manager: CodeAgent = CodeAgent(
            tools=[],
            model=self.model_id,
            max_iterations=self.max_iterations,
            managed_agents=[self.managed_web_agent, self.managed_trader_agent],
            additional_authorized_imports=self.used_packages,
            planning_output=os.path.join(os.getcwd()),
        )

    def run(self, task=None):
        if not task:
            raise ValueError("Task must be provided.")
        return self.trader.run(
            f"{task}, use {', '.join(self.used_packages)} python package" if self.used_packages else task
        )

    def registerAllTools(self):
        return [

            # Gather Tools
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

            # Trade Tools
            MarketOrderTool(),
            LimitOrderTool(),
            ShortOrderTool(),
            ClientOrderIDTool(),
            BracketOrderTool(),
            TrailingStopOrderTool(),
            RetrieveOrdersTool(),

            # Assets Tools
            GetAssetsTool(),
            CheckAssetTradabilityTool(),
            PortfolioTool(),
            AccountInfoTool(),
            PortfolioGainLossTool(),

            # Position Tools
            PortfolioTool(),
        ]
