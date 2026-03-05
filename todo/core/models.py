from django.db import models
from django.utils.translation import gettext_lazy as _

# translate and Text reader in Text form
from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field

# для среза дескрипшина
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords_html

# для удаления фотографий
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files.storage import default_storage


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
        title=models.CharField(
            max_length=255,
            verbose_name=_("Заголовок"),
        ),
        # description=models.TextField(blank=True, verbose_name=_("Опис")),
        description=CKEditor5Field(
            blank=True,
            verbose_name=_("Опис"),
            config_name="extends",
        ),
    )

    def __str__(self):
        return f"{self.title} ({self.status})"

    @property
    def short_description(self):
        """обрезаем описание до 10 слов для отображения в шаблоне списка задач"""
        if not self.description:
            return ""
        plain = strip_tags(self.description)
        return truncatewords_html(plain, 10)

    def cleanup_images(self):
        description = self.description or ""

        soup = BeautifulSoup(description, "html.parser")
        images = soup.find_all("img")

        for img in images:
            url = img.get("src")
            if not url:
                continue

            parsed_url = urlparse(url)
            file_path = parsed_url.path  # /media/2026/03/03/file.jpg

            if not file_path.startswith(settings.MEDIA_URL):
                continue

            relative_path = file_path[len(settings.MEDIA_URL) :]

            # 🔥 Удаляем через storage (правильнее чем os.remove)
            if default_storage.exists(relative_path):
                default_storage.delete(relative_path)

                # Если используется локальное хранилище —
                # можно попробовать удалить пустую папку
                absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                folder = os.path.dirname(absolute_path)

                if os.path.isdir(folder) and not os.listdir(folder):
                    os.rmdir(folder)

    def delete(self, *args, **kwargs):
        self.cleanup_images()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Завдання")
        verbose_name_plural = _("Завдання")
