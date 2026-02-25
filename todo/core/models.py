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

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Опис")

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Статус"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активна")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    due_date = models.DateField(null=True, blank=True, verbose_name="Дедлайн")

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Пріоритет",
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"
