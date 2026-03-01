from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields


class Task(TranslatableModel):

    class Status(models.TextChoices):
        NEW = "new", _("Нова")
        IN_PROGRESS = "in_progress", _("В процесі")
        DONE = "done", _("Виконано")

    class Priority(models.TextChoices):
        LOW = "low", _("Не високий")
        MEDIUM = "medium", _("Середній")
        HIGH = "high", _("Терміновий")
        IMMEDIATE = "immediate", _("Негайний")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name=_("Статус"),
    )

    is_active = models.BooleanField(default=True, verbose_name=_("Активна"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата створення")
    )
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Виконати до"))

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name=_("Пріоритет"),
    )

    translations = TranslatedFields(
        title=models.CharField(max_length=255, verbose_name=_("Заголовок")),
        description=models.TextField(blank=True, verbose_name=_("Опис")),
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = _("Завдання")
        verbose_name_plural = _("Завдання")
