from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# ==========================================
# USER REGISTRATION FORM
# ==========================================

class RegisterForm(UserCreationForm):

    class Meta:

        model = CustomUser

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Username",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter First Name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Last Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Email Address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )


# ==========================================
# ADMIN - CREATE USER FORM
# ==========================================

class UserCreateForm(UserCreationForm):

    class Meta:

        model = CustomUser

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "is_active",
            "profile_pic",
        )

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "profile_pic": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        )

        self.fields["is_active"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )


# ==========================================
# ADMIN - UPDATE USER FORM
# ==========================================

class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = CustomUser

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "is_active",
            "profile_pic",
        )

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "profile_pic": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["is_active"].widget.attrs.update(
            {
                "class": "form-check-input",
            }
        )