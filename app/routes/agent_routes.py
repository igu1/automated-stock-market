from flask import Blueprint, request, jsonify
from app.tasks.stock_task import run_stock_agent_task

agent_bp = Blueprint("agent", __name__)

@agent_bp.route('/agent/run', methods=['POST'])
def run_agent():
    """
    Endpoint to initiate a stock agent task.

    Receives a query from the request, triggers the stock agent task asynchronously,
    and returns the task ID.

    Request body:
        - query (str): The query for the stock agent.

    Returns:
        JSON response containing the task ID.
    """
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    task = run_stock_agent_task.apply_async(args=[query])
    return jsonify({"task_id": task.id}), 202

@agent_bp.route('/agent/status/<task_id>', methods=['GET'])
def agent_status(task_id):
    """
    Endpoint to check the status of a stock agent task.

    Retrieves the status of the asynchronous task based on the provided task ID.

    Args:
        task_id (str): The ID of the task to check.

    Returns:
        JSON response containing the task state and result or status.
    """
    task = run_stock_agent_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state == 'SUCCESS':
        response = {"state": task.state, "result": task.result}
    else:
        response = {"state": task.state, "status": str(task.info)}
    return jsonify(response)
