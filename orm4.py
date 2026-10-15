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

# from django.db.models import Count
# from core.models import Project
#
# projects = Project.objects.all()
# project_file_counts = {}
# for project in projects:
#     file_count = project.files.aggregate(num_files=Count('id'))
#     project_file_counts[project.title] = file_count['num_files']
# for project_name, num_files in project_file_counts.items():
#     print(f"Project: {project_name}, Number of files: {num_files}")

"""Задание 5
1. Импортируйте модель Project.
2. Импортируйте класс AVG из django.
3. Напишите запрос, который сможет для каждого проекта выведите среднее количество задач.
4. Выведите полученные данные.
"""

from django.db.models import Avg
from core.models import Project

projects = Project.objects.annotate(task_count=Count("tasks"))

# Number of tasks for each project
for project in projects:
    print(f"Project: {project.title}, Tasks: {project.task_count}")

# Average number of tasks across all projects
result = projects.aggregate(avg_tasks=Avg("task_count"))
print(f"Average Number of Tasks: {result['avg_tasks']}")

"""Задание 6
1. Импортируйте модель User из django.
2. Импортируйте класс Count из django.
3. Напишите запрос, который получит из базы данных количество задач для каждого пользователя.
4. В запросе укажите, что хотим работать только с конкретными полями:
○ Username
○ Наше собственно созданное поле count_of_tasks
5. Выведите как результат никнейм разработчика и количество прикреплённых за ним задач."""

