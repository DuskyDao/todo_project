from django.db import models


class Task(models.Model):

    class Status(models.TextChoices):
        NEW = "new", "Нова"
        IN_PROGRESS = "in_progress", "В процесі"
        DONE = "done", "Виконано"

    class Priority(models.TextChoices):
        LOW = "low", "Легка"
        MEDIUM = "medium", "Середня"
        HIGH = "high", "Висока"
        IMMEDIATE = "immediate", "Негайний"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )

    def __str__(self):
        return f"{self.title} ({self.status})"
