from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead

        fields = [
            'title',
            'contact',
            'assigned_to',
            'status',
            'estimated_value',
            'expected_close',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'contact': forms.Select(attrs={
                'class': 'form-select'
            }),

            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'estimated_value': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'expected_close': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }