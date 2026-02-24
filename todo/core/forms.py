from django.forms import ModelForm
from django import forms

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }

    due_date = forms.DateField(widget=forms.SelectDateWidget())
