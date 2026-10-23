from django.db import models

from .base import UUIDv7Model


class Category(UUIDv7Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
