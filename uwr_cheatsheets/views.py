from django.shortcuts import render, get_object_or_404
from .models import Course, CourseRun


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
