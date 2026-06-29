from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("courses/", views.reader_home, name="reader_home"),
    path("course/<int:pk>/", views.reader_home, name="reader_home"),
    path("upload/", views.upload_note, name="upload_note"),
    path("register/", views.register, name="register"),
    path("note/<int:pk>/", views.note_reader, name="note_reader"),
    path("profile/", views.profile, name="profile"),
]
