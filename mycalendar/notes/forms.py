from django import forms
from django.core.exceptions import ValidationError
from notes.models import Category, Note

class CategoryForm(forms.Form):
    required_css_class = 'required'
    name = forms.CharField(max_length=30, label="Nazwa kategorii")

    def clean_name(self):
        if Category.objects.filter(name=self.cleaned_data['name']).exists():
            raise ValidationError("Taka kategoria już jest")
        return self.cleaned_data['name']

class NoteForm(forms.Form):
    required_css_class = 'required'

    title = forms.CharField(max_length=30, label="Tytuł", widget=forms.TextInput(attrs={'placeholder': "Tytuł notatki"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Kategoria")
    note = forms.CharField(widget=forms.Textarea, label="Treść")
    status = forms.ChoiceField(choices=Note.STATUSES, label="Status")
