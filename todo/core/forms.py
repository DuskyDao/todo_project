from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils.translation import gettext_lazy as _


from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.SelectDateWidget(
            years=range(date.today().year, date.today().year + 3),
            attrs={"min": date.today().isoformat()},
        ),
        label=_("Виконати до"),
        initial=date.today(),
        required=False,
    )

    title = forms.CharField(max_length=255, required=True, label=_("Заголовок"))
    description = forms.CharField(
        widget=forms.Textarea, required=False, label=_("Опис")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["title"].initial = self.instance.title
            self.fields["description"].initial = self.instance.description

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.title = self.cleaned_data["title"]
        instance.description = self.cleaned_data["description"]
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date", "priority", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 50, "rows": 10}),
        }
