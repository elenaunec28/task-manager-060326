from django.contrib import admin, messages
from django.utils import timezone
from .models import Category, SubTask, Task, Project, ProjectFile, Tag


@admin.action(description="заменять пробелы на нижние подчёркивания для объектов проекта")
def replace_spaces_with_underscores(modeladmin, request, queryset):
    bool = False
    for obj in queryset:
        if " " in obj.title:
            obj.title = obj.title.replace(" ", "_")
            obj.updated_at = timezone.now()
            obj.save()
            bool = True

    if bool:
        modeladmin.message_user(request, f"Все пробелы успешно заменены на нижние подчёркивания.", messages.SUCCESS)
    else:
        modeladmin.message_user(request, f"Объект {obj} не содержит пробелов в названии.", messages.SUCCESS)


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



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "file_count")
    search_fields = ("title", "description")
    actions = [replace_spaces_with_underscores]




@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ("file_name", "file", "created_at")
    search_fields = ("file_name",)
    actions = [replace_spaces_with_underscores]



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    actions = [replace_spaces_with_underscores]
