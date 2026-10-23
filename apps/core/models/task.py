from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from .base import TimeStampedModel, UUIDv7Model
"""Создайте связь модели пользователя (User) с моделью Task.
Добавьте связь к модели Task через поле assignee, которое будет ссылаться на
пользователя. При выборе типа связи учтите, что на одной задаче может быть
одновременно только один сотрудник.
"""

class Task(UUIDv7Model, TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        PENDING = "pending", "Pending"
        BLOCKED = "blocked", "Blocked"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    title = models.CharField(max_length=255, validators=[MinLengthValidator(10)], unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField("Category", blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NEW)
    priority = models.CharField(max_length=15, choices=Priority.choices, default=Priority.MEDIUM)
    project = models.ForeignKey("Project", related_name="tasks", on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag", related_name="tasks", blank=True)
    due_date = models.DateTimeField()
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    class Meta:
        db_table = "task_manager_task"
        ordering = ["-due_date", "assignee__username"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "project"],
                name="unique_project_title",
            ),
        ]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
