from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator, MaxValueValidator


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
    run = models.ForeignKey(CourseRun, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    lecture_from = models.PositiveSmallIntegerField(null=True, blank=True)
    lecture_to = models.PositiveSmallIntegerField(null=True, blank=True)
    pdf = models.FileField(upload_to="notes_pdfs/")
    author = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["lecture_from", "title"]
        constraints = [
            models.CheckConstraint(
                condition=Q(lecture_to__gte=F("lecture_from")),
                name="lecture_to_gte_from",
            )
        ]

    def __str__(self):
        return self.title
