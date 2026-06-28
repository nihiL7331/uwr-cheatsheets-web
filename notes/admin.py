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


@admin.action(description="Zatwierdź wybrane notatki")
def approve_notes(modeladmin, req, queryset):
    updated = queryset.update(status=Note.Status.APPROVED)
    modeladmin.message_user(req, f"Zatwierdzono {updated} notatek.")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "run",
        "status",
        "author",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("status", "run__term", "run__course")
    search_fields = ("title", "author", "run__course__name")
    ordering = ("status", "run", "lecture_from")
    actions = [approve_notes]
