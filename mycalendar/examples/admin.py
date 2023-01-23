from django.contrib import admin
from examples.models import PersonalData, Student, Programme, Language

@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender')
    ordering = ('date_of_birth', )
    search_fields = ('first_name', 'last_name',)
    list_filter = ('gender',)
    #readonly_fields = ('first_name', 'date_of_birth')



# Register your models here.
#admin.site.register(PersonalData, PersonalDataAdmin)

admin.site.register(Student)
admin.site.register(Programme)
admin.site.register(Language)