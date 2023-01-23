from django.shortcuts import render, get_object_or_404, redirect
from notes.models import Note, Category, ToDoList, ToDoListItem
from notes import forms
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
# Create your views here.

#CLASS BASED VIEWS

class ToDoListItemCreateView(CreateView):
    model = ToDoListItem
    fields = ['note',]
    template_name = 'notes/form.html'

    def get_list(self):
        return get_object_or_404(ToDoList, pk=self.kwargs['list_id'])

    def get_success_url(self):
        return reverse('notes_cbv_note', kwargs={'pk': self.get_list().note.pk}) #self.object.todo_list.note.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        list = self.get_list() # get_object_or_404(ToDoList, pk=self.kwargs['list_id'])
        ctx['cancel'] = reverse('notes_cbv_note', kwargs={'pk': list.note.pk})
        return ctx

    def form_valid(self, form):
        list = self.get_list() #get_object_or_404(ToDoList, pk=self.kwargs['list_id'])
        form.instance.todo_list = list
        return super().form_valid(form)


class ToDoListCreateView(CreateView):
    model = ToDoList
    # field = '__all__'
    fields = ['title',]
    template_name = 'notes/form.html'

    # ODKOMENTOWAC jestli fields = '__all__'
    #def get_initial(self):
    #    note = get_object_or_404(Note, pk=self.kwargs['note_id'])
    #    return {'note': note}

    def get_success_url(self):
        return reverse('notes_cbv_note', kwargs={'pk': self.object.note.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel'] = reverse('notes_cbv_note', kwargs={'pk': self.kwargs['note_id']})
        return ctx

    def form_valid(self, form):
        note = get_object_or_404(Note, pk=self.kwargs['note_id'])
        # self.object = super().save(commit=False)
        # self.object.note = note
        # return super().form_valid(form)
        form.instance.note = note
        return super().form_valid(form)

class NoteListView(ListView):
    model = Note
    template_name = 'notes/cbv_note_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(profile__user=self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = '__all__'
    template_name = 'notes/form.html'

    def get_success_url(self):
        return reverse('notes_cbv_note', kwargs={'pk': self.object.pk})

class NoteUpdateView(UpdateView):
    model = Note
    fields = '__all__'
    template_name = 'notes/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel'] = self.get_success_url()
        return context

    def get_success_url(self):
        return reverse('notes_cbv_note', kwargs={'pk': self.object.pk})

class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('notes_cbv_notes')
    template_name = 'notes/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel'] = reverse('notes_cbv_note', kwargs={'pk': self.object.pk})
        return context

#class CategoryCreateView(UserPassesTestMixin, CreateView):
class CategoryCreateView(PermissionRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    template_name = 'notes/form.html'

    #permission_required = 'notes.add_category'
    permission_required = ('notes.view_category', 'notes.add_category')

    #def test_func(self):
    #    if self.request.user.email.endswith('@gmail.com'):
    #        return True
    #    return False

    def get_success_url(self):
        return reverse('notes_cbv_category', kwargs={'pk': self.object.pk})


# FUNCTION BASED VIEWS
def note_detail(request, id):
    note = get_object_or_404(Note, id=id)
    ctx = {'note': note}
    return render(request, 'notes/note_detail.html', ctx)

def correct_mail(user):
    if user.email.endswith('@gmail.com'):
        return True
    return False

@user_passes_test(correct_mail)
def note_list(request):
    search = request.GET.get('search', None)
    if search:
        notes = Note.objects.filter(title__icontains=search)
    else:
        notes = Note.objects.all()
    ctx = {'notes': notes, 'page_title': 'Lista wszystkich notatek'}
    return render(request, 'notes/note_list.html', ctx)

def note_unpublished_list(request):
    notes = Note.objects.filter(status='a')
    ctx = {'notes': notes, 'page_title': 'Lista notatek nieopublikowanych'}
    return render(request, 'notes/note_list.html', ctx)

def note_published_list(request):
    notes = Note.objects.filter(status='b')
    ctx = {'notes': notes, 'page_title': 'Lista notatek opublikowanych'}
    return render(request, 'notes/note_list.html', ctx)

@permission_required('notes.view_category', raise_exception=True)
@permission_required('notes.add_category', raise_exception=True)
def category_list(request):
    categories = Category.objects.all()
    ctx = {'categories': categories}
    return render(request, 'notes/category_list.html', ctx)

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    ctx = {'category': category}
    return render(request, 'notes/category_detail.html', ctx)

def category_create(request):
    if request.method == "POST":
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            category = Category(name=form.cleaned_data['name'])
            category.save()
            return redirect('notes_category_detail', id=category.id)
    else:
        form = forms.CategoryForm()
    return render(request, 'notes/form.html', {'form': form})

@login_required
def note_create(request):
    #if not request.user.is_authenticated:
    #    return redirect('login')

    if request.method == "POST":
        form = forms.NoteForm(request.POST)
        if form.is_valid():
            note = Note.objects.create(**form.cleaned_data)
            return redirect('notes_detail', id=note.id)
    else:
        form = forms.NoteForm() #initial={'title': "Tytuł domyślny"})
    return render(request, 'notes/form.html', {'form':form})

def note_update(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        form = forms.NoteForm(request.POST)
        if form.is_valid():
            for field, value in form.cleaned_data.items():
                setattr(note, field, value)
            note.save()
            return redirect('notes_detail', id=note.id)
    else:
        form = forms.NoteForm(initial={'title': note.title, 'category': note.category,
                                       'note': note.note, 'status': note.status })
    return render(request, 'notes/form.html', {'form': form})