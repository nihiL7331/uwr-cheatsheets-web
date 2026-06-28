from django import forms
from .models import Note


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
