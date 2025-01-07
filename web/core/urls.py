from django.contrib import admin
from django.urls import path
from agent.views import index, tasks, agent_run, agent_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('task/<str:status>/', tasks, name='tasks'),
    path('agent/run/', agent_run, name='agent_run'),
    path('agent/status/<str:status_id>/', agent_status, name='agent_status'),
]