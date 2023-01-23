from django.contrib import admin
from notes.models import Note, Category, ToDoList, ToDoListItem, Profile

# Register your models here.
admin.site.register(Note)
admin.site.register(Category)
admin.site.register(ToDoList)
admin.site.register(ToDoListItem)
admin.site.register(Profile)