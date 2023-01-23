from django.urls import path, reverse_lazy
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, CreateView
from . import models
from . import views
import datetime

urlpatterns = [
    path('test/', views.test_view, name="test"),
    path('personaldata/<int:id>/', views.personal_data_detail, name='examples_person_detail'),
    path('personaldata/', views.personal_data_list),
    path('test-form/', views.test_form),
    path('contact-form/', views.contact_form),
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('create/personaldata/', views.personal_data_form),
    path('create/student/', views.student_form),
    #path('cbv/thank-you/', TemplateView.as_view(template_name='examples/thank_you.html')),
    path('cbv/thank-you/', views.MyTemplateView.as_view()),
    path('cbv/onet/', RedirectView.as_view(url="https://onet.pl")),
    path('cbv/test/', RedirectView.as_view(pattern_name='test')),
    path('cbv/personaldata/', ListView.as_view(model=models.PersonalData, ordering='first_name'), name='examples_personaldata_list'),
    path('cbv/personaldata/women/', ListView.as_view(queryset=models.PersonalData.objects.filter(gender='f')),),
    path('cbv/personaldata/<int:pk>/', DetailView.as_view(model=models.PersonalData), name='examples_personaldata'),
    #path('cbv/create/personaldata/', CreateView.as_view(model=models.PersonalData, fields="__all__", success_url=reverse_lazy('examples_personaldata_list'))),
    path('cbv/create/personaldata/', views.PersonalDataCreateView.as_view()),
    path('cbv/update/personaldata/<int:pk>/', views.PersonalDataUpdateView.as_view(), name="examples_update_personaldata"),
    path('cbv/create/student/', views.StudentCreateView.as_view()),
    path('cbv/contact/', views.ContactFormView.as_view()),

]