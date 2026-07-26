from django import forms

from .models import Note


class NoteForm(forms.ModelForm):

    class Meta:

        model = Note

        fields = [
            "contact",
            "lead",
            "content",
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


            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter note details...",
                }
            ),

        }


        labels = {

            "contact": "Contact",

            "lead": "Lead",

            "content": "Note Content",

        }



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        self.fields["contact"].required = False

        self.fields["lead"].required = False


        self.fields["contact"].empty_label = (
            "Select Contact"
        )

        self.fields["lead"].empty_label = (
            "Select Lead"
        )



    def clean(self):

        cleaned_data = super().clean()


        contact = cleaned_data.get("contact")

        lead = cleaned_data.get("lead")


        if not contact and not lead:

            raise forms.ValidationError(
                "Please select either a Contact or a Lead."
            )


        return cleaned_data