from typing import Optional, List, Any
from app.agents.core import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool, ManagedAgent, ToolCallingAgent
from app.tools import *

from flask import current_app

class StockAgent:
    """
    Main agent class for handling stock trading operations.

    This agent provides capabilities for:
    - Web searching and data gathering
    - Stock trading operations
    - Portfolio management
    - Market data analysis

    Attributes:
        debug (bool): Debug mode flag from app config
        max_iterations (int): Maximum iterations for agent operations
        used_packages (List[str]): List of used Python packages
        model_id (LiteLLMModel): AI model for agent operations
        web_agent (ToolCallingAgent): Agent for web search operations
        managed_web_agent (ManagedAgent): Managed wrapper for web agent
        trader (CodeAgent): Agent for trading operations
        managed_trader_agent (ManagedAgent): Managed wrapper for trader agent
        manager (CodeAgent): Main agent manager coordinating all operations
    """

    def __init__(self) -> None:
        """
        Initialize the StockAgent with configuration from Flask app.

        Sets up:
        - Debug mode from app config
        - Maximum iterations for agent operations
        - Web search agent with DuckDuckGo and webpage visit tools
        - Trading agent with all registered tools
        - Main manager agent coordinating all operations
        """
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
        """
        Execute a trading task using the agent system.


        Args:
            task (str, optional): The task to execute. Must be provided.

        Returns:
            Any: Result of the agent operation

        Raises:
            ValueError: If no task is provided
        """
        if not task:
            raise ValueError("Task must be provided.")
        return self.manager.run(task)

    def registerAllTools(self) -> List[Any]:
        """
        Register all available tools for the trading agent.

        Returns:
            List[Any]: List of all registered tools categorized by:
                - Data gathering tools
                - Trading tools
                - Asset management tools
                - Portfolio tools
        """
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
            # GetAssetsTool(),
            CheckAssetTradabilityTool(),
            AccountInfoTool(),
            PortfolioGainLossTool(),

            # Position Tools
            PortfolioTool(),
            StockPricePredictorTool(),
        ]
