from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField('auth.user', on_delete=models.CASCADE)
    info = models.TextField()

    class Meta:
        verbose_name = "Profil"
        verbose_name = "Profile"

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    """ Kategoria notatki """
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

#def is_letters(value):
#    if not value.isalpha():
#        raise ValidationError("Moga być tylko litery !!!")

class Note(models.Model):
    """ Prosta notatka"""
    STATUSES = (('a', 'Nieopublikowana'), ('b','Opublikowana'))
    title = models.CharField(max_length=30) #, validators=[is_letters,])
    category = models.ForeignKey('notes.Category', on_delete=models.PROTECT)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    note = models.TextField()
    status = models.CharField(max_length=1, choices=STATUSES, default='a')
    profile = models.ForeignKey('notes.profile', on_delete=models.CASCADE) # editable=False)

    def __str__(self):
        return f"{ self.title}"

    class Meta:
        verbose_name = "Notatka"
        verbose_name_plural = "Notatki"

class ToDoList(models.Model):
    """ Lista TODO do notatki """
    note = models.ForeignKey('notes.Note', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('-id',)
        unique_together = ('note', 'title')
        verbose_name = "Lista TODO"
        verbose_name_plural = "Listy TODO"

    def __str__(self):
        return f"{self.title}"

class ToDoListItem(models.Model):
    """ elementy listy ToDo """
    STATUSES = (('a', 'Aktualne'), ('b', 'Wykonane'))
    status = models.CharField(max_length=1, choices=STATUSES, default='a')
    todo_list = models.ForeignKey('notes.ToDoList', on_delete=models.CASCADE)
    note = models.CharField(max_length=200)

    class Meta:

        verbose_name = "Element listy"
        verbose_name_plural = "Elemnty listy"

    def __str__(self):
        return f"{self.todo_list} {self.id}"
