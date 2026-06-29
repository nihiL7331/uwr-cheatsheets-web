from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import NoteUploadForm, Note, RegisterForm, ProfileForm
from itertools import groupby


def landing(req):
    return render(req, "notes/landing.html")


@login_required
def upload_note(req):
    if req.method == "POST":
        form = NoteUploadForm(req.POST, req.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = req.user
            if req.user.has_perm("notes.can_publish_directly"):
                note.status = Note.Status.APPROVED
                messages.success(req, "Notatka opublikowana.")
            else:
                note.status = Note.Status.PENDING
                messages.success(req, "Notatka oczekuje na zatwierdzenie.")
            note.save()
            return redirect("notes:note_reader", pk=note.run.course.pk)
    else:
        form = NoteUploadForm()
    return render(req, "notes/upload_note.html", {"form": form})


@login_required
def profile(req):
    if req.method == "POST":
        form = ProfileForm(req.POST, instance=req.user)
        if form.is_valid():
            form.save()
            messages.success(req, "Zapisano zmiany.")
            return redirect("notes:profile")
    else:
        form = ProfileForm(instance=req.user)
    return render(req, "notes/profile.html", {"form": form})


def register(req):
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            messages.success(
                req,
                f"Witaj, {user.get_full_name() or user.username}! Konto zostalo utworzone.",
            )
            return redirect("notes:reader_home")
    else:
        form = RegisterForm()
    return render(req, "registration/register.html", {"form": form})


def _approved_tree():
    approved = (
        Note.objects.filter(status=Note.Status.APPROVED)
        .select_related("run", "run__course")
        .order_by(
            "run__course__name",
            "-run__year_start",
            "run__term",
            "lecture_from",
            "title",
        )
    )
    tree = []
    for course, course_notes in groupby(approved, key=lambda n: n.run.course):
        runs = [
            {"run": run, "notes": list(rn)}
            for run, rn in groupby(course_notes, key=lambda n: n.run)
        ]
        tree.append({"course": course, "runs": runs})

    return tree


def note_reader(req, pk):
    note = get_object_or_404(Note, pk=pk, status=Note.Status.APPROVED)

    if req.headers.get("HX-Request"):
        return render(req, "notes/_reader_main.html", {"current_note": note})

    tree = _approved_tree()

    return render(req, "notes/reader.html", {"current_note": note, "tree": tree})


def reader_home(req):
    tree = _approved_tree()

    return render(req, "notes/reader.html", {"current_note": None, "tree": tree})
