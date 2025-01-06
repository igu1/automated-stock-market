from celery import Celery
from app.agents.stock_agent import StockAgent

celery = Celery("tasks", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

@celery.task(name="tasks.run_stock_agent_task")
def run_stock_agent_task(query, debug=False):
    stock_agent = StockAgent()
    result = stock_agent.run(query)
    return {"query": query, "result": result}
