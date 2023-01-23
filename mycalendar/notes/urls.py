from django.urls import path
from django.views.generic import ListView, DetailView

from . import views
from . import models

urlpatterns = [
    path('notes/<int:id>', views.note_detail, name='notes_detail'),
    path('notes/', views.note_list, name='notes_list'),
    path('notes-unpublished/', views.note_unpublished_list, name='notes_unpublished_list'),
    path('notes-published/', views.note_published_list, name='notes_published_list'),
    path('categories/', views.category_list, name='notes_category_list'),
    path('categories/<int:id>/', views.category_detail, name='notes_category_detail' ),
    path('create/category/', views.category_create, name='notes_category_create'),
    path('create/note/', views.note_create, name="notes_note_create"),
    path('update/note/<int:id>/', views.note_update, name='notes_note_update'),
    #path('cbv/notes/', ListView.as_view(model=models.Note, template_name='notes/cbv_note_list.html'), name='notes_cbv_notes'),
    path('cbv/categories/', ListView.as_view(model=models.Category, template_name='notes/cbv_category_list.html'), name='notes_cbv_categories'),
    path('cbv/note/<int:pk>/', DetailView.as_view(model=models.Note, template_name='notes/cbv_note_detail.html'), name='notes_cbv_note'),
    path('cbv/notes/', views.NoteListView.as_view(), name='notes_cbv_notes'),
    path('cbv/category/<int:pk>/', DetailView.as_view(model=models.Category, template_name='notes/cbv_category_detail.html'), name='notes_cbv_category'),
    path('cbv/create/note/', views.NoteCreateView.as_view(), name='notes_cbv_create_note'),
    path('cbv/update/note/<int:pk>/', views.NoteUpdateView.as_view(), name='notes_cbv_update_note'),
    path('cbv/delete/note/<int:pk>/', views.NoteDeleteView.as_view(), name='notes_cbv_delete_note'),
    path('cbv/create/category/', views.CategoryCreateView.as_view(), name='notes_cbv_create_category'),
    path('cbv/create/todolist/<int:note_id>/', views.ToDoListCreateView.as_view(), name='notes_cbv_create_list'),
    path('cbv/create/todolist-item/<int:list_id>/', views.ToDoListItemCreateView.as_view(), name='notes_cbv_create_list_item'),

]