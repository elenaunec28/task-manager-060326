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

# from django.db.models import Avg
# from core.models import Project
#
# projects = Project.objects.annotate(task_count=Count("tasks"))
#
# # Number of tasks for each project
# for project in projects:
#     print(f"Project: {project.title}, Tasks: {project.task_count}")
#
# # Average number of tasks across all projects
# result = projects.aggregate(avg_tasks=Avg("task_count"))
# print(f"Average Number of Tasks: {result['avg_tasks']}")

"""Задание 6
1. Импортируйте модель User из django.
2. Импортируйте класс Count из django.
3. Напишите запрос, который получит из базы данных количество задач для каждого пользователя.
4. В запросе укажите, что хотим работать только с конкретными полями:
○ Username
○ Наше собственно созданное поле count_of_tasks
5. Выведите как результат никнейм разработчика и количество прикреплённых за ним задач."""

# from django.db.models import Count
# from django.contrib.auth.models import User
#
# count_of_tasks = User.objects.annotate(count_of_tasks=Count("tasks")).values("username", "count_of_tasks")
# for user in count_of_tasks:
#     print(f"Username: {user['username']}, Count of Tasks: {user['count_of_tasks']}")

"""Задание 7
1. Импортируйте модель Task.
2. Напишите запрос, который сможет отсортировать все задачи по нескольким полям:
○ Приоритет задачи
○ Дата к которой задача должна быть выполнена
3. Выведите название задачи, приоритет и дату завершения.
"""
#
# from core.models import Task
# tasks = Task.objects.all().order_by("priority", "due_date")
# for task in tasks:
#     print(f"Task: {task.title}, Priority: {task.priority}, Due Date: {task.due_date}")

"""Задание 8
1. Импортируйте модель User из django.
2. Напишите запрос, который будет сортировать всех пользователей исходя из того,
как много у каждого задач.
3. Отсортируйте от самого загруженного сотрудника, к самому свободному по задачам.
4. Конкретизируйте запрос таким образом, чтобы в него включались только поля:
○ Username
○ Count_of_tasks
5. Выведите все данные в консоль.
"""

# from django.contrib.auth.models import User
# from django.db.models import Count
#
# count_of_tasks = User.objects.annotate(count_of_tasks=Count("tasks")).values("username", "count_of_tasks").order_by("-count_of_tasks")
# for user in count_of_tasks:
#     print(f"Username: {user['username']}, Count of Tasks: {user['count_of_tasks']}")


"""Задание 9
1. Импортируйте модель Task.
2. Импортируйте класс Paginator.
3. Напишите запрос для получения всех задач.
4. Реализуйте пагинацию для того, чтобы в рамках одной страницы отображалось ровно 10 задач,
не более.
5. Выведите данные об этих 10-ти задачах:
○ Название
○ Статус
○ Приоритетность
○ Username разработчика"""

# from django.core.paginator import Paginator
# from core.models import Task
#
# sorted_users = (User.objects.annotate(count_of_tasks=Count("tasks")).values_list("username", "count_of_tasks").order_by("-count_of_tasks"))
# for username, count_of_tasks in sorted_users:
#     print(f"Username: {username}, Count of Tasks: {count_of_tasks}")

"""from core.models import Task
from django.core.paginator import Paginator

task = Task.objects.all()
paginator = Paginator(task, 10)  # 10 tasks per page
page_number = 1  # You can change this to get different pages
page_obj = paginator.get_page(page_number)
for task in page_obj:
    print(f"Task: {task.title}, Status: {task.status}, Priority: {task.priority}, Username: {task.assignee}")"""


"""Задание 10
1. Установите модуль djangorestframework.
2. Добавить этот модуль в файл requirements.txt.
3. Добавить этот модуль в список установленных приложений в файле settings.py.
4. Создать новый пакет serializers, в котором создать первый файл - projects
5. Импортируйте класс ModelSerializer.
6. Напишите первый сериализатор, который будет обрабатывать поля id и name для проекта,
выдавая общую базу для вывода всех проектов."""

"""Задание 11
1. Импортируйте ранее написанный сериализатор в файл, где будет реализовываться первое
представление.
2. Импортируйте дополнительные методы и классы:
○ Request из rest_framework (для типизации объекта запроса)
○ JsonResponse из django (для возврата и типизации ответов)
○ Status из rest_framework (для указания статусов ответов)
○ Api_view из rest_framework.decorators (для конкретики обрабатываемых методов)
○ Модель Project (для запросов к таблице проектов в базе данных)
3. Напишите функцию, которая будет обрабатывать GET запросы для получения списка всех проектов
из Базы данных.
4. Зарегистрировать эту функцию в списке эндпоинтов в файле urls.py
5. Проверьте работу готового эндпоинта.
"""


"""Задание 12
1. Создайте новый файл для сериализаторов задач.
2. Импортируйте класс ModelSerializer.
3. Напишите сериализатор для модели Task с полями id, name, status, priority для получения общей
информации о задачах.
4. Напишите сериализатор для модели Task с полями id, name, status, priority, description,"""


"""Задание 13
1. Импортируйте модель Task
2. Импортируйте написанный ранее сериализатор AllTasksSerializer
3. Напишите отображение, которое будет выводить JSON данные о всех задачах из базы данных:
○ Если при отправке запроса не передавать конкретный проект - выводить все задачи
○ Если был указан конкретный проект, например “TIGERˮ - выводить только те задачи, которые
принадлежат этому проекту"""