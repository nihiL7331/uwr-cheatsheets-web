from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, CourseRun
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def course_list(req):
    courses = Course.objects.order_by("name")
    return render(req, "uwr_cheatsheets/course_list.html", {"courses": courses})


def course_detail(req, pk):
    course = get_object_or_404(Course, pk=pk)
    runs = (
        CourseRun.objects.filter(course=course)
        .order_by("-year_start", "term")
        .prefetch_related("notes")
    )
    return render(
        req,
        "uwr_cheatsheets/course_detail.html",
        {"course": course, "runs": runs},
    )


@login_required
def upload_note(req):
    return render(req, "uwr_cheatsheets/upload_note.html")


def register(req):
    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect("uwr_cheatsheets:course_list")
    else:
        form = UserCreationForm()
    return render(req, "registration/register.html", {"form": form})
