from django import forms
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["run", "title", "pdf", "author", "lecture_from", "lecture_to"]

    def clean_pdf(self):
        pdf = self.cleaned_data["pdf"]
        max_mb = 20
        if pdf.size > max_mb * 1024 * 1024:
            raise forms.ValidationError(f"Plik jest za duży (maksimum {max_mb} MB).")
        return pdf


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name")
        labels = {
            "first_name": "Imię",
            "last_name": "Nazwisko",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = {"first_name", "last_name"}
        labels = {"first_name": "Imię", "last_name": "Nazwisko"}
