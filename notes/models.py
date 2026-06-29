from django.db import models
from django.db.models import Q, F
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)


class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CourseRun(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="runs")
    year_start = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    TERM_CHOICES = [("Z", "zimowy"), ("L", "letni")]
    term = models.CharField(max_length=1, choices=TERM_CHOICES)

    class Meta:
        unique_together = ("course", "year_start", "term")

    def __str__(self):
        return f"{self.course.name} {self.year_start}/{self.year_start + 1}{self.term}"


class Note(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Oczekująca"
        APPROVED = "approved", "Zatwierdzona"
        REJECTED = "rejected", "Odrzucona"

    @property
    def display_author(self):
        if self.author:
            return self.author
        if self.uploaded_by:
            return self.uploaded_by.get_full_name() or self.uploaded_by.username
        return ""

    run = models.ForeignKey(CourseRun, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    lecture_from = models.PositiveSmallIntegerField(null=True, blank=True)
    lecture_to = models.PositiveSmallIntegerField(null=True, blank=True)
    pdf = models.FileField(
        upload_to="notes_pdfs/", validators=[FileExtensionValidator(["pdf"])]
    )
    author = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_notes",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["lecture_from", "title"]
        permissions = [("can_publish_directly", "Może publikować bez moderacji")]
        constraints = [
            models.CheckConstraint(
                condition=Q(lecture_to__gte=F("lecture_from")),
                name="lecture_to_gte_from",
            )
        ]

    def __str__(self):
        return self.title
