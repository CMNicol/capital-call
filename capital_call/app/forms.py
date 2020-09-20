from django import forms
from .models import DataCall


class CallForm(forms.ModelForm):
    class Meta:
        model = DataCall
        fields = [
            'date',
            'investment_name',
            'capital_requirement'
        ]
