from django import forms
from ..models.award import Award

class AwardForm(forms.ModelForm):
    year = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha del Premio"
    )

    class Meta:
        model = Award
        fields = ['name', 'category', 'year', 'movie', 'description']
