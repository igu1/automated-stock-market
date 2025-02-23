from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import TaskModel
import asyncio
import aiohttp
import json

BASE_URL = "http://127.0.0.1:5000/agent/"

async def run_agent(query):
    url = BASE_URL + "run"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"query": query}) as response:
            return await response.json()

async def get_status(status_id):
    url = BASE_URL + f"status/{status_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def agent_status(request, status_id):
    if request.method == "GET":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        status = loop.run_until_complete(get_status(status_id))
        if status["state"] == "SUCCESS":
            task = TaskModel.objects.get(task_id=status_id)
            if ('error' in status):
                task.response = status["error"]['message']
            else:
                task.response = status["result"]["result"]
            task.status = status["state"]
            task.save()
        return redirect("index")
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def agent_run(request):
    if request.method == "POST":
        try:
            query = request.POST['keyword']
            if not query:
                return JsonResponse({"error": "Query is required"}, status=400)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_agent(query))
            response = TaskModel.objects.create(**result, user=request.user, question=query)
            return redirect('index')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)

def index(request):
    if request.user.is_authenticated:
        tasks = TaskModel.objects.filter(user=request.user).order_by("-created_at")
        return render(request, "index.html", {"tasks": tasks, "message": ""})
    else:
        return redirect("admin:login")


def tasks(request, status):
    tasks = TaskModel.objects.filter(user=request.user, status=status).order_by("-created_at")
    return render(request, "task.html", {"tasks": tasks, "status": status})