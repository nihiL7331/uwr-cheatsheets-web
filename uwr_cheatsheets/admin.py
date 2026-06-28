from django.contrib import admin
from .models import Course, CourseRun, Note


class CourseRunInline(admin.TabularInline):
    model = CourseRun
    extra = 0


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [CourseRunInline]


@admin.register(CourseRun)
class CourseRunAdmin(admin.ModelAdmin):
    list_display = ("course", "year_start", "term")
    list_filter = ("term", "year_start", "course")
    search_fields = ("course__name",)
    ordering = ("-year_start", "term")
    inlines = [NoteInline]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "run",
        "lecture_from",
        "lecture_to",
        "author",
        "uploaded_at",
    )
    list_filter = ("run__term", "run__course")
    search_fields = ("title", "author", "run__course__name")
    ordering = ("run", "lecture_from")
