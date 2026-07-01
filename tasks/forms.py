from django import forms
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assigned_to",
            "related_contact",
            "related_lead",
            "due_date",
            "priority",
            "status",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter task title",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter task description",
            }),

            "assigned_to": forms.Select(attrs={
                "class": "form-select",
            }),

            "related_contact": forms.Select(attrs={
                "class": "form-select",
            }),

            "related_lead": forms.Select(attrs={
                "class": "form-select",
            }),

            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "priority": forms.Select(attrs={
                "class": "form-select",
            }),

            "status": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Restrict users (IMPORTANT for CRM security)
        self.fields["assigned_to"].queryset = User.objects.filter(is_active=True)

        # Optional labels (safe)
        self.fields["assigned_to"].label = "Assign To"
        self.fields["related_contact"].label = "Related Contact"
        self.fields["related_lead"].label = "Related Lead"