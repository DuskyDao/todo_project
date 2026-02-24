from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)


from .forms import TaskForm
from .models import Task


class TaskListView(ListView):
    template_name = "core/list.html"
    context_object_name = "tasks"
    queryset = Task.objects.all().order_by("-created_at")
    paginate_by = 5
    extra_context = {"title": "Task List"}


class TaskCreateView(CreateView):
    template_name = "core/create.html"
    form_class = TaskForm
    success_url = reverse_lazy("core:task-list")
    extra_context = {"title": "Create Task"}


class TaskDetailView(DetailView):
    template_name = "core/detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail Task"
        return context

    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs["pk"])


class TaskUpdateView(UpdateView):
    template_name = "core/create.html"
    model = Task
    form_class = TaskForm
    # success_url = reverse_lazy("core:task-list")
    extra_context = {"title": "Update Task"}

    def get_success_url(self):
        return reverse("core:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(DeleteView):
    template_name = "core/delete.html"
    model = Task
