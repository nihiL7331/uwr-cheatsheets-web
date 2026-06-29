from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, CourseRun
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import NoteUploadForm, Note
from django.db.models import Prefetch
from itertools import groupby


def landing(req):
    return render(req, "notes/landing.html")


def course_list(req):
    courses = Course.objects.order_by("name")
    return render(req, "notes/course_list.html", {"courses": courses})


def course_detail(req, pk):
    course = get_object_or_404(Course, pk=pk)
    approved = Note.objects.filter(status=Note.Status.APPROVED)
    runs = (
        CourseRun.objects.filter(course=course)
        .order_by("-year_start", "term")
        .prefetch_related(Prefetch("notes", queryset=approved))
    )
    return render(
        req,
        "notes/course_detail.html",
        {"course": course, "runs": runs},
    )


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
            return redirect("notes:course_detail", pk=note.run.course.pk)
    else:
        form = NoteUploadForm()
    return render(req, "notes/upload_note.html", {"form": form})


def register(req):
    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect("notes:course_list")
    else:
        form = UserCreationForm()
    return render(req, "registration/register.html", {"form": form})


def note_reader(req, pk):
    note = get_object_or_404(Note, pk=pk, status=Note.Status.APPROVED)

    if req.headers.get("HX-Request"):
        return render(req, "notes/_reader_main.html", {"current_note": note})

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

    return render(req, "notes/reader.html", {"current_note": note, "tree": tree})
