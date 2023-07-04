from django.urls import path
from . import views


urlpatterns = [
    path('books',views.books, name='books'),
    path('',views.home),
    path('notes',views.notes,name='notes'),
    path('delete_note/<int:pk>/',views.delete_note, name='delete_note'),
    path('delete_homework/<int:pk>/',views.delete_homework, name='delete_homework'),
    path('notes-detail/<int:pk>/',views.NotesDetailView.as_view(), name='notes-detail'),
    path('notesdetail/<int:pk>/',views.notesdetail,name='detail'),
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update_homework'),
    path('youtube',views.youtube,name='youtube'),
    path('todo',views.todo,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name='update_todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete_todo'),
    path('books',views.books,name='books'),


    


]
