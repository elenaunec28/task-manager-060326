from django.db import models
from .base import TimeStampedModel, UUIDv7Model



class Project(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    files = models.ManyToManyField("ProjectFile", related_name="projects", blank=True)

    class Meta:
        db_table = "task_manager_project"
        ordering = ["-title"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "description"],
                name="unique_project_title_description",
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def file_count(self):
        return self.files.count()


class ProjectFile(UUIDv7Model, TimeStampedModel):
    file_name = models.CharField(max_length=120)
    file = models.FileField(upload_to="projects/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_manager_project_file"
        ordering = ["-created_at"]
        verbose_name = "Project File"
        verbose_name_plural = "Project Files"

    def __str__(self):
        return self.file_name
