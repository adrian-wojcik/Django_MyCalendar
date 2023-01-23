from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
import os

# Create your models here.
class Language(models.Model):
    """ Jezyki """
    name = models.CharField(max_length=30)
    alpha2 = models.SlugField(max_length=2, unique=True)

    class Meta:
        verbose_name = "Język"
        verbose_name_plural = "Języki"

    def __str__(self):
        return f"{self.name} ({self.alpha2})"

def person_media_path(instance, filename):
    return os.path.join("persons", "%d" % instance.id, filename)

class PersonalData(models.Model):
    """Reprezentacja danych osobowych"""
    photo = models.ImageField(null=True, upload_to=person_media_path)
    first_name = models.CharField(max_length=30, help_text="Podaj imię - zawsze od dużej litery")
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=(('f', 'Kobieta'), ('m', 'Mężczyzna'), ('o', 'Nie podaję')))
    languages = models.ManyToManyField('examples.Language')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ('first_name', 'last_name')
        verbose_name = "Osoba"
        verbose_name_plural = "Osoby"

    def get_student(self):
        try:
            return self.student
        except ObjectDoesNotExist:
            return None

def test_validator(value):
    print("Dziala z modelu !!!")

class Student(models.Model):
    """ Klasa reprezentująca studenta"""
    personal_data = models.OneToOneField('examples.PersonalData', verbose_name="Osoba", on_delete=models.PROTECT,
                                         validators=[test_validator,])
    index_number = models.PositiveIntegerField(unique=True)
    programme = models.ForeignKey('examples.Programme', verbose_name="Kierunek", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.personal_data}"

    def clean(self):
        print("POSZEDL CLEAN NA MODELU")
        raise ValidationError("TEST !!!")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Studenci"

class Programme(models.Model):
    """
    Kierunek studiow, zakładamy,
    że student mo ze być TYLKO na jednym
    kierunku studiów
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Kierunek studiów"
        verbose_name_plural = "Kierunki studiów"
