from django.forms import ModelForm
from django import forms
from datetime import date
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.widgets import CKEditor5Widget

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
        widget=CKEditor5Widget(config_name="extends"), required=False, label=_("Опис")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            current_language = self.instance.get_current_language()
            self.fields["title"].initial = self.instance.title
            self.fields["description"].initial = self.instance.description

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        instance.set_current_language(instance.get_current_language())

        instance.title = self.cleaned_data["title"]
        instance.description = self.cleaned_data["description"]
        if commit:
            instance.save_translations()
        return instance

    class Meta:
        model = Task
        fields = ["title", "description", "status", "due_date", "priority", "is_active"]
        # widgets = {
        #     "title": forms.TextInput(attrs={"class": "form-input"}),
        #     # "description": forms.Textarea(attrs={"cols": 50, "rows": 10}),
        #     "description": CKEditor5Widget(
        #         attrs={"class": "django_ckeditor_5"}, config_name="extends"
        #     ),
        # }
