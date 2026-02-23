from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import TaskForm
from .models import Task


class TaskListView(ListView):
    template_name = "core/list.html"
    context_object_name = "tasks"
    queryset = Task.objects.all().order_by("-created_at")
    paginate_by = 10
    extra_context = {"title": "Task List"}


class TaskCreateView(CreateView):
    template_name = "core/create.html"
    form_class = TaskForm
    success_url = reverse_lazy("core:task-list")
    extra_context = {"title": "Create Task"}
