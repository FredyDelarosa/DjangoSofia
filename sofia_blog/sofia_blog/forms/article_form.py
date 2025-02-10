from django import forms
from ..models.article import Article
from ..models.category import Category

class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Selecciona una categoría",
        label="Categoría"
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'category']
