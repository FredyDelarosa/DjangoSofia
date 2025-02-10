from django import forms
from ..models.movie import Movie

class MovieForm(forms.ModelForm):
    release_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de estreno"
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'poster']
