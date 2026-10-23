from django.contrib import admin, messages
from django.utils import timezone

from apps.tasks.models import Category, SubTask, Tag, Task
from apps.core.admin import replace_spaces_with_underscores


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    actions = [replace_spaces_with_underscores]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "created_at", "due_date", "assignee")
    list_filter = ("status", "priority", "project", "created_at", "due_date", "assignee")
    search_fields = ("title",)
    actions = [replace_spaces_with_underscores, "update_status_to_closed"]

    @admin.action(description="обновлять статус всех выделенных задач на 'Закрыто'")
    def update_status_to_closed(self, request, queryset):
        updated_count = queryset.update(status=Task.Status.DONE, updated_at=timezone.now())
        self.message_user(request,f"Статус всех выделенных задач успешно обновлен на 'Закрыто'. "
                                f"Количество обновленных задач: {updated_count}.", messages.SUCCESS)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "due_date", "created_at")
    list_filter = ("status", "task", "created_at", "due_date")
    search_fields = ("title",)
    actions = [replace_spaces_with_underscores]



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    actions = [replace_spaces_with_underscores]
