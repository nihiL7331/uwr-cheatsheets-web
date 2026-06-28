from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("courses/", views.course_list, name="course_list"),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
    path("upload/", views.upload_note, name="upload_note"),
    path("register/", views.register, name="register"),
    path("note/<int:pk>/", views.note_reader, name="note_reader"),
]
