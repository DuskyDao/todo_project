from django.forms import ModelForm
from django import forms
from datetime import date

from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(date.today().year, date.today().year + 3),
            attrs={"min": date.today().isoformat()},
        ),
        label="Дедлайн",
        initial=date.today(),
        required=False,
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date", "priority", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }
