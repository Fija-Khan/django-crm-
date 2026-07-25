from django import forms
from .models import Deal


class DealForm(forms.ModelForm):

    class Meta:

        model = Deal

        fields = [
            "lead",
            "amount",
            "stage",
            "close_date",
            "notes",
        ]


        widgets = {

            "lead": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),


            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter deal amount"
                }
            ),


            "stage": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),


            "close_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),


            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Add deal notes..."
                }
            ),

        }