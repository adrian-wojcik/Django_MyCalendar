import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from examples.models import Student
from django.shortcuts import render, get_object_or_404
from examples.models import PersonalData
from examples import forms

# SEKCJA CLASS BASED VIEWS

class ContactFormView(FormView):
    form_class = forms.ContactForm
    template_name = 'examples/contact_form.html'
    success_url = reverse_lazy('thank_you')

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class MyTemplateView(TemplateView):
    template_name = 'examples/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'msg': datetime.datetime.now()})
        return context

class PersonalDataCreateView(CreateView):
    model = PersonalData
    fields = '__all__' #['gender', 'first_name', 'last_name']
    #initial = {'first_name': 'Anna'}
    #success_url = reverse_lazy('examples_personaldata_list')

    def get_initial(self):
        return {'first_name': "Karolina"}

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.required_css_class = 'required'
        return form_class

    def get_success_url(self):
        return reverse('examples_personaldata', kwargs={'pk': self.object.pk})

    def form_valid1(self, form):
        if form.instance.date_of_birth is None:
            form.instance.date_of_birth = '1800-01-01'
        #self.object = form.save(commit=False)
        #self.object.date_of_birth = '1900-01-01'
        return super().form_valid(form)
        #self.object.save()
        #return HttpResponseRedirect(self.get_success_url())

class PersonalDataUpdateView(UpdateView):
    model = PersonalData
    fields = '__all__'
    template_name = 'examples/personaldata_form.html'

    def get_success_url(self):
        return reverse('examples_personaldata', kwargs={'pk': self.object.pk})


class StudentCreateView(CreateView):
    model = Student
    form_class = forms.StudentForm
    template_name = 'examples/personaldata_form.html'

    def get_success_url(self):
        return reverse('test')


# Create your views here.
def test_view(request):
    return render(request, 'examples/base.html')

def personal_data_detail(request, id):
    #try:
    #    personal_data = PersonalData.objects.get(id=id)
    #except ObjectDoesNotExist:
    #    raise Http404
    personal_data = get_object_or_404(PersonalData, id=id)
    ctx = {'personal_data': personal_data}
    return render(request, 'examples/personal_data_detail.html', ctx)

def personal_data_list(request):
    personal_data = PersonalData.objects.all()
    ctx = {'personal_data': personal_data }
    return render(request, 'examples/personal_data_list.html', ctx)

def test_form(request):
    print(request.GET)
    return render(request, 'examples/test_form.html')

def contact_form(request):
    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # wysli maila, lub co trezba
            return redirect('thank_you')  #HttpResponseRedirect

    else:
        form = forms.ContactForm()
    return render(request, 'examples/contact_form.html', {'form': form})

def thank_you_view(request):
    return render(request, 'examples/thank_you.html')

def personal_data_form(request):
    if request.method == "POST":
        form = forms.PersonalDataForm(request.POST)
        if form.is_valid():
            #personal_data = PersonalData(**form.cleaned_data)
            personal_data = PersonalData(first_name=form.cleaned_data['first_name'],
                                         last_name=form.cleand_data['last_name'],
                                         date_of_birth=form.cleaned_data['date_of_birth'],
                                         gender=form.cleaned_data['gender'])
            personal_data.save()

            return redirect('examples_person_detail', id=personal_data.id)
    else:
        form = forms.PersonalDataForm()
    return render(request, 'examples/contact_form.html', {'form': form})

def student_form(request):
    if request.method == "POST":
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            # jeżeli nic nie zmieniamy to obj=form.save()
            # a jeżeli chcemy coś dodać zanim zapiszemy do bazy to:
            obj = form.save(commit=False)
            last_student = Student.objects.all().order_by('-index_number')
            if last_student.exists():
                index_nr = last_student[0].index_number + 1
            else:
                index_nr = 1
            obj.index_number = index_nr
            obj.save()
            return redirect('test')
    else:
        form = forms.StudentForm() #instance=student)
    return render(request, 'examples/contact_form.html', {'form': form})
