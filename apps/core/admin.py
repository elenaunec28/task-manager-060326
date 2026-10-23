from django.contrib import admin, messages
from django.utils import timezone


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


