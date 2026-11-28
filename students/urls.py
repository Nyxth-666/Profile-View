from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.student_list, name="list"),
    path("add/", views.student_save, name="add"),
    path("<int:pk>/", views.student_detail, name="detail"),
    path("<int:pk>/edit/", views.student_save, name="edit"),
    path("<int:pk>/delete/", views.student_delete, name="delete"),
    path("<int:pk>/photo/", views.student_photo, name="photo"),
    path("<int:pk>/photo/file/", views.student_photo_file, name="photo_file"),
]