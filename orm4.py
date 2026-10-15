import os
from datetime import date, datetime, timedelta
from idlelib import search

from django.db.models import Q, F, Count
from django.utils import timezone

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Tag, Project, ProjectFile, Task, Category

"""Задание 1
1. Импортируйте модель Project.
2. Импортируйте модуль timezone из django.
3. Напишите запрос, который выдаст только те проекты, которые были созданы в текущем
месяце (месяц брать от даты текущего дня).
4. Если есть хоть один проект - выведите информацию:
○ Название проекта
○ Полная дата его создания"""

# cur_month_projects = Project.objects.filter(created_at__month=timezone.now().month, created_at__year=timezone.now().year)
# for project in cur_month_projects:
#     print(f"Название проекта: {project.title}")
#     print(f"Полная дата его создания: {project.created_at}")

"""Задание 2
1. Импортируйте модель ProjectFile.
2. Импортируйте класс ExtractWeekDay из django.
3. Напишите запрос, который будет получать список файлов за определённый день, например
понедельник:
○ Для выборки конкретного значения по полю даты создания используйте класс ExtractWeekDay.
○ Для упрощения работы с таким значением задайте для него новое, не заявленное в модели поле,
например weekday.
○ Проведите фильтрацию по этому новому полю.
4. Если файлов не было найдено - выведите сообщение “Empty Dataˮ, если был найден хоть один файл -
выведите информацию о нём:
○ Название файла
○ Путь к файлу, где он сохранён"""

# import django
# from django.db.models.functions import ExtractWeekDay
# from core.models.project import ProjectFile
#
# monday_project_files = ProjectFile.objects.annotate(weekday=ExtractWeekDay('created_at')).filter(weekday=3) # 3 соответствует вторнику, так как в Django неделя начинается с воскресенья (1 - воскресенье, 2 - понедельник, 3 - вторник и т.д.)
#
# if monday_project_files.exists():
#     for project_file in monday_project_files:
#         print(f"Название файла: {project_file.file_name}")
#         print(f"Путь к файлу: {project_file.file}")
# else:
#     print("Empty Data")


"""Задание 3
1. Импортируйте модель Project.
2. Напишите запрос, который будет считать количество всех проектов, которые есть в базе данных.
3. Выведите количество всех проектов в консоль.
"""
#
# project_count = Project.objects.count()
# print(f"Количество всех проектов: {project_count}")


"""Задание 4
1. Импортируйте модель Project.
2. Импортируйте класс Count из django.
3. Напишите запрос, который будет считать количество файлов для каждого проекта персонально.
4. Выведите информацию о количестве файлов для каждого проекта.
"""

from django.db.models import Count
from core.models import Project

project = Project.objects.all()
project_file_count = {}

for p in project:
    project_file_count = project.project