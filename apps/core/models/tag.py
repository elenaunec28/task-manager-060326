from django.db import models

from apps.core.models.base import UUIDv7Model


class Tag(UUIDv7Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name