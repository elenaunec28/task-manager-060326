from django.db import models

from .base import TimeStampedModel, UUIDv7Model
from .task import Task


class SubTask(UUIDv7Model, TimeStampedModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(max_length=20, choices=Task.Status.choices, default=Task.Status.NEW)
    due_date = models.DateTimeField()

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ["-created_at"]
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"

    def __str__(self):
        return self.title
