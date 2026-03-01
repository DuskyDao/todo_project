from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Task


@admin.register(Task)
class TaskAdmin(TranslatableAdmin):
    list_display = (
        "title",
        "status",
        "is_active",
        "created_at",
        "due_date",
        "priority",
    )
    list_filter = ("status", "is_active", "priority")
    search_fields = ["translations__title"]
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
