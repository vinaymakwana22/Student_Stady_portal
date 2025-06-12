from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),  # Home page view
    path('notes', views.notes, name="notes"),  # List of notes for the user
    path('delete_note/<int:pk>', views.delete_note, name="delete-notes"),  # Delete note functionality
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name="notes_detail"),  # Detail view of a single note
    
    path('homework', views.homework, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),

    path('youtube', views.youtube, name="youtube"),

    path('todo', views.todo, name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),

    path('books', views.books, name="books"),

    path('dictionary', views.dictionary, name="dictionary"),

    path('wiki', views.wiki, name="wiki"),

    path('conversion', views.conversion, name="conversion"),

    path('ai-chat/', views.ai_chat_view, name='ai_chat'),
]