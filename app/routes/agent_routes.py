from flask import Blueprint, request, jsonify
from app.tasks.stock_task import run_stock_agent_task

agent_bp = Blueprint("agent", __name__)

@agent_bp.route('/agent/run', methods=['POST'])
def run_agent():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    debug = data.get('debug', False)
    task = run_stock_agent_task.apply_async(args=[query, debug])
    return jsonify({"task_id": task.id}), 202

@agent_bp.route('/agent/status/<task_id>', methods=['GET'])
def agent_status(task_id):
    task = run_stock_agent_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state == 'SUCCESS':
        response = {"state": task.state, "result": task.result}
    else:
        response = {"state": task.state, "status": str(task.info)}
    return jsonify(response)
