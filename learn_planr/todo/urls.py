from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path('', views.MainView.as_view(), name="main"),
    path("<int:todo_id>/", views.get_todo, name="get_todo"),
    path("todos/", views.get_list_todo, name="get_todos"),
    path("toggle_task_completion/", views.toggle_task_completion, name="toggle_task_completion"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("todo/<int:todo_id>/delete", views.delete_todo, name="delete_todo"),
]