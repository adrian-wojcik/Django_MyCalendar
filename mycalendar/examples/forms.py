from django import forms
from django.core.exceptions import ValidationError
from examples.models import Student


class ContactForm(forms.Form):
    error_css_class = 'testerror'
    required_css_class = 'required'

    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    age = forms.IntegerField(required=False, label="Wiek")


def upper_first_char(value):
    print(value)
    if not value or not value[0].isupper():
        raise ValidationError("Musi się zaczynać dużą literą")


class PersonalDataForm(forms.Form):
    required_css_class = 'required'

    first_name = forms.CharField(max_length=30, label="Imię", validators=[upper_first_char,])
    last_name = forms.CharField(max_length=30, label="Nazwisko")
    date_of_birth = forms.DateField(label="Data urodzenia")
    gender = forms.ChoiceField(choices=(('f', 'Kobieta'), ('m', 'Mężczyzna'), ('o', 'Nie podaję')), label="Płeć")

    #def clean_first_name(self):
    #    print(self.cleaned_data)
    #    return self.cleaned_data['first_name']

    def clean(self):
        print("CAŁOŚĆ")
        print(self.cleaned_data)
        raise ValidationError("BLAD FORMULARZA")


class StudentForm(forms.ModelForm):
    required_css_class = 'required'

    def clean_personal_data(self):
        print("ODPALILEM W FORMIE")
        return self.cleaned_data['personal_data']

    class Meta:
        model = Student
        fields = ['personal_data', 'programme']
        #labels = {'personal_data': "Osoba", 'programme': "Kierunek"}
        #exclude = ['personal_data',]