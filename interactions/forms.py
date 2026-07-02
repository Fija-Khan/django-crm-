from django import forms
from .models import Interaction


class InteractionForm(forms.ModelForm):

    class Meta:
        model = Interaction
        fields = [
            "contact",
            "lead",
            "type",
            "summary",
            "interaction_date",
        ]

        widgets = {
            "contact": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "lead": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "summary": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter interaction summary",
                }
            ),

            "interaction_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["lead"].required = False

        self.fields["contact"].empty_label = "Select Contact"
        self.fields["lead"].empty_label = "Select Lead"