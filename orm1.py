import os
from datetime import date, datetime, timedelta
from idlelib import search

from django.db.models import Q, F, Count
from django.utils import timezone

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from apps.tasks.models import Tag, Task, Category
from apps.projects.models import Project, ProjectFile

# 1 Создание тэгов для будущих задач

# new_tag = Tag.objects.create(name="Backend")
# new_tag = Tag.objects.create(name="Frontend")
# new_tag = Tag.objects.create(name="Q&A")
# new_tag = Tag.objects.create(name="Design")
# new_tag = Tag.objects.create(name="Devops")

# 2 Создание проектов и файлов для них
# new_project1 = Project.objects.create(title="Project1", description="This is my first project.")
#
# project2 = Project(title = "Project2", description = "This is my second project.")
# project2.save()
#
# proj1_file = ProjectFile.objects.create(file_name="file1.txt", file="projects/1/file.txt")
# proj2_file = ProjectFile.objects.create(file_name="file2.txt", file="projects/2/file.txt")
#
# new_project1.files.add(proj1_file)
# project2.files.add(proj2_file)

# 3 Создание пользователей для работы в проекте.
# Импортируйте модель Пользователя (User), которого по умолчанию предлагает Django.

# backend_user = User.objects.create(username="Backend", password="password")
# frontend_user = User.objects.create(username="Frontend", password="password")
# devops_user = User.objects.create(username="DevOPS", password="password")
# qa_user = User.objects.create(username="Q&A", password="password")
# designer_user = User.objects.create(username="Designer", password="password")


# пролверка, что все пользователи созданы
# user = User.objects.filter(username="Designer").first()

# users = User.objects.filter(
#     username__in=["Backend", "Frontend", "DevOPS", "Q&A", "Designer"]
# )
#
# print(list(users.values("id", "username")))
# print("Количество:", users.count())

"""Задание 5
1. Импортируйте модель Task.
2. Для каждого проекта создайте задачи. По одной-две для каждого тега.
3. Для foreignkey полей передаём объекты, которые мы создавали ранее.
4. Убедитесь, что данные были созданы и сохранены в базу данных.
"""

# task1 = Task.objects.create(
#     title="Backend Task 2",
#     description="This is a backend task.",
#     status=Task.Status.NEW,
#     priority=Task.Priority.HIGH,
#     project=Project.objects.get(title="Project1"),
#     due_date=date(2024, 6, 30),
#     assignee=User.objects.get(username="Backend"),
# )
#
# task2 = Task.objects.create(
#     title="Frontend Task 2",
#     description="This is a frontend task.",
#     #categories= Category.objects.get(name="Category1"),
#     status=Task.Status.NEW,
#     priority=Task.Priority.MEDIUM,
#     project=Project.objects.get(title="Project1"),
#     due_date=date(2024, 7, 15),
#     assignee=User.objects.get(username="Frontend")
# )

# task3 = Task.objects.create(
#     title="DevOps Task 2",
#     description="This is a DevOps task.",
#     status=Task.Status.NEW,
#     priority=Task.Priority.LOW,
#     project=Project.objects.get(title="Project2"),
#     due_date=timezone.make_aware(datetime(2024, 6, 30)),
#     assignee=User.objects.get(username="DevOPS")
# )

"""Задание 6
1. Получите все объекты тегов.
2. У каждого объекта созданных задач обратитесь к полю тегов через точку.
3. У поля ManyToMany (tags) вызовите метод add и передайте ему объект тега.
○ Объект тега будет зависеть от того, какой title будет в задаче, например:
(‘Добавить новый эндпоинтʼ - Backend tag, ‘Обновить страницу ответа 404ʼ - Frontend tag)"""

# task1 = Task.objects.get(title="Backend Task 2")
# backend_tag = Tag.objects.get(name="Backend")
# task1.tag.add(backend_tag)

###tiger_task_1.tags.add(back_tag)

# task2 = Task.objects.get(title="Frontend Task 2")
# frontend_tag = Tag.objects.get(name="Frontend")
# task2.tag.add(frontend_tag)
#
# task3 = Task.objects.get(title="Backend Task 1")
# backend_tag = Tag.objects.get(name="Backend")
# task3.tag.add(backend_tag)

"""Задание 7
1. Импортируйте модели тегов Tag.
2. Напишите запрос, который позволит получить список всех тегов.
3. Выведите имя каждого тега.
4. Получите самый первый тег.
5. Получите самый последний тег.
6. Получите кол-во всех тегов.
"""


# all_tags = Tag.objects.all()
# for tag in all_tags:
#     print(tag.name)
#
# first_tag = Tag.objects.first()
# print("Первый тег:", first_tag.name)
#
# last_tag = Tag.objects.last()
# print("Последний тег:", last_tag.name)
#
# tags_count = Tag.objects.count()
# print("Количество тегов:", tags_count)

"""Задание 8
1. Напишите запрос, который будет искать тэг по определённому имени
2. Проверьте наличие такого тега методом, который выдаёт True или False на наличие объекта.
"""

# tag_name = "Backend"
# tag_exists = Tag.objects.filter(name=tag_name).exists()
# if tag_exists:
#     print(f"Тег с именем '{tag_name}' существует.")
# else:
#     print(f"Тег с именем '{tag_name}' не существует.")

"""Задание 9
1. Напишите запрос, который позволит получить теги, у которых в имени будет совпадение по
переданной строке, например: “...Tagˮ
2. Выведите имена всех этих тегов."""

# search_string = "e"
# matching_tags = Tag.objects.filter(name__icontains=search_string)
# for tag in matching_tags:
#     print(tag.name)

"""Задание 10
1. Импортируйте модуль datetime и модель Project.
2. Создайте объект даты, по которой нужно сделать поиск.
3. Напишите запрос, который позволит получить список проектов, которые равны или старше
переданной даты создания.
4. Выведите имена таких проектов"""

# search_date = timezone.make_aware(datetime(2026, 6, 1))
#
# project = Project.objects.filter(created_at__gte=search_date)
# for proj in project:
#     print(proj.title)


"""Задание 11
1. Импортируйте модель Project.
2. Напишите запрос, который позволит получить необходимые проекты:
○ Реализуйте фильтрацию, которая будет проходить два условия:
■ Проекты, равные или больше указанной даты
■ Проекты, у которых в имени есть строка ‘TIʼ
3. Выведите имена таких проектов.
"""
# search_date = timezone.make_aware(datetime(2026, 6, 1))
# project = Project.objects.filter(Q(created_at__gte=search_date)& Q(title__icontains="1"))
# for proj in project:
#     print(proj.title)


"""Задание 12
1. Напишите запрос, который позволит получить список всех файлов, которые привязаны к
конкретному проекту. Поиск произведите по имени проекта.
2. Выведите только пути к каждому файлу.
"""

# project_files= ProjectFile.objects.filter(projects__title="Project1")
# for file in project_files:
#     print(file.file.url)


"""Задание 13
1. Напишите запрос, который поможет получить только те задачи, у которых:
○ Статус “newˮ
○ Приоритетность “Urgentˮ
2. Выведите информацию по каждой такой задаче:
○ Название
○ Статус
○ Приоритетность
○ Дата, когда задача должна быть сдана
○ Email сотрудника, за которым закреплена эта задача"""

# tasks_filter = Task.objects.filter(status=Task.Status.NEW, priority=Task.Priority.HIGH)
# for task in tasks_filter:
#     print(f"Название: {task.title}")
#     print(f"Статус: {task.status}")
#     print(f"Приоритетность: {task.priority}")
#     print(f"Дата сдачи: {task.due_date}")
#     print(f"Email сотрудника: {task.assignee.email if task.assignee else 'Нет назначенного сотрудника'}")
#     print("-----")

"""Задание 14
1. Напишите запрос, который поможет получить конкретную задачу
2. Обратитесь к полю статуса и обновите его на новое значение, например “pendingˮ. Сделайте это
через метод update().
"""

# task = Task.objects.filter(title="Backend Task 2")
# task.update(status=Task.Status.PENDING)

"""Задание 15
1. Напишите запрос, который будет содержать в себе прохождение одной из комбинаций:
○ статус и приоритетность
○ прохождение несовпадения по тегу
2. Выведите название этих задач, проект и email разработчиков.
"""

# task_filter2 = Task.objects.filter(
#     Q(status=Task.Status.NEW) & Q(priority=Task.Priority.HIGH) | ~Q(tag__name="Tag1")
# )
# for task in task_filter2:
#     print(f"Название: {task.title}")
#     print(f"Проект: {task.project.title}")
#     print(f"Email разработчика: {task.assignee.email if task.assignee else 'Нет назначенного сотрудника'}")
#     print("-----")

"""Задание 16
1. Импортируйте модель Task.
2. Импортируйте F класс.
3. Обновите приоритет задач, которые должны быть выполнены в следующем месяце, на "Critical".
Используйте Fкласс."""

# today = timezone.localdate()
# if today.month == 12:
#     year, month = today.year + 1, 1
# else:
#     year, month = today.year, today.month + 1
#
# Task.objects.filter(due_date__year=year, due_date__month=month).update(priority=Task.Priority.HIGH)

###Task.objects.filter(due_date__month=F('created_date__month') + 1).update(priority="Critical")

"""Задание 17
1. Импортируйте модуль timedelta из библиотеки datetime.
2. Импортируйте модель Task.
3. Обновите все объекты задач по полю due_date на + 1 неделю. Используйте Fкласс.
"""

# Task.objects.update(due_date=F('due_date') + timedelta(weeks=1))


"""Задание 18
1. Импортируйте модель Task.
2. Напишите запрос, который поможет профильтровать по lookups полю те задачи, у которых нет
назначенного разработчика.
3. Выведите название таких задач и название проекта для этих задач.
"""

# tasks_w_assignee = Task.objects.filter(assignee__isnull=True)
# for task in tasks_w_assignee:
#     print(f"Название задачи: {task.title}")
#     print(f"Название проекта: {task.project.title}")
#     print("-----")

"""Задание 19
Необходимо получить все задачи, связанные с тэгами и содержащими определённое ключевое слово.
1. Импортируйте модель Task.
2. Напишите запрос, который поможет отфильтровать задачи через конкретный тэг. Q&A
○ Запрос должен быть написан с использованием lookups полей
○ Запрос должен начинаться с модели Task, через эту модель нужно получить доступ к
конкретному тэгу.
3. Выведите информацию по каждой задаче:
○ Имя задачи
○ Статус задачи
○ Приоритет задачи
○ Имя проекта этой задачи"""

###???
# task_wi_qa = Task.objects.filter(tag__name__icontains="Backend")
# for task in task_wi_qa:
#     print(f"Имя задачи: {task.title}")
#     print(f"Статус задачи: {task.status}")
#     print(f"Приоритет задачи: {task.priority}")
#     print(f"Имя проекта: {task.project.title}")
#     print("-----")


"""Задание 20
Необходимо получить все проекты, связанные с файлами, созданными в определенный период (последняя
неделя).
1. Импортируйте модели Project, ProjectFile.
2. Создайте переменную с датой периода создания файлов (от текущего дня 7 дней)
3. Напишите первый запрос, который поможет получить те файлы, которые должны быть больше, или
равны полученной дате по полю создания этого файла
4. Напишите запрос, который поможет получить только те проекты, у которых есть те файлы, что мы
получили предыдущим запросом.
5. Выведите информацию об этих проектах: имя проекта и дата создания."""

# last_week = timezone.now() - timedelta(days=7)
# recent_files = ProjectFile.objects.filter(created_at__gte=last_week)
# projects_with_recent_files = Project.objects.filter(files__in=recent_files).distinct()
#
# for project in projects_with_recent_files:
#     print(f"Имя проекта: {project.title}")
#     print(f"Дата создания: {project.created_at}")
#     print("-----")

"""Задание 21
1. Импортируйте модель Task.
2. Напишите запрос, который отфильтрует задачи по определённому статусу (‘newʼ).
3. Для всех полученных задач обновите поле status на новое значение ‘in_progressʼ.
4. У модели вызовите метод, который позволит массово применить обновления.
5. Посмотрите результат, выведите поле статуса у всех задач.
"""

# tasks = list(Task.objects.filter(status=Task.Status.NEW))
#
# for task in tasks:
#     task.status = Task.Status.IN_PROGRESS
#     task.updated_at = timezone.now()
#
# Task.objects.bulk_update(tasks, ["status", "updated_at"])

"""Задание 22
1. Импортируйте модель Task.
2. Импортируйте модуль timedelta из библиотеки datetime и F класс.
3. Получите список задач со статусом ‘in_progressʼ.
4. Для каждого полученного объекта измените дату для завершения задачи, увеличив её на 3 дня от
той даты, что в задаче указана.
5. У модели Task вызовите метод, который поможет массово обновить данные.
"""

# task_to_update = list(Task.objects.filter(status=Task.Status.IN_PROGRESS))
# for task in task_to_update:
#     task.due_date = F('due_date') + timedelta(days=3)
#     task.updated_at = timezone.now()
#
# Task.objects.bulk_update(task_to_update, ["due_date", "updated_at"])

"""Задание 23
1. Импортируйте класс Count для подсчёта кол-ва файлов.
2. Импортируйте модуль timezone из фреймворка django.
3. Импортируйте модель Project.
4. Создайте переменную в которой будет храниться искомая дата проекта, например “20230707ˮ.
5. Напишите запрос, который будет фильтровать проекты по следующим параметрам:
○ Дата создания должна быть больше той даты, что мы получили ранее
○ Кол-во файлов для проекта должно быть больше, или равно переданному, например трём"""

# my_date = timezone.datetime(2020, 7, 7).astimezone()
# # my_date = timezone.make_aware(datetime.date(2020, 7, 7))
#
# projects_filtered = Project.objects.annotate(file_count=Count('files')).filter(
#     Q(created_at__gt=my_date) &
#     Q(file_count__gte=1)
# )
##??
# for project in projects_filtered:
#     print(f"Имя проекта: {project.title}")
#     print(f"Дата создания: {project.created_at}")
#     print(f"Количество файлов: {project.file_count}")
#     print("-----")



"""Задание 24
1. Импортируйте модель Task.
2. Импортируйте класс Q и модуль datetime из фреймворка django
3. Импортируйте модуль timezone из Django и библиотеку calendar(базовая).
4. Напишите функцию, которая будет высчитывать конец месяца от текущей даты.
5. Напишите запрос, который будет фильтровать задачи по нескольким условиям:
○ Приоритет задачи или “Criticalˮ или “Urgentˮ
○ Дата, когда задача должна быть закрыта(due_date) - дата конца месяца с текущей даты"""

import calendar

def get_end_of_month():
    today = timezone.localtime(timezone.now())
    last_day = calendar.monthrange(today.year, today.month)[1]
    end_of_month = today.replace(day=last_day)
    return end_of_month

end_of_month = get_end_of_month()
tasks_filtered = Task.objects.filter(
 Q(priority="High") |
Q(priority="Low"),
 due_date__lte=end_of_month
)

"""Задание 25
1. Импортируйте модель Task.
2. Импортируйте класс Q.
3. Напишите запрос, который будет получать все задачи, кроме тех, что будут переданы в фильтр,
например: “pendingˮ и “closedˮ.
"""


"""Задание 26
1. Импортируйте модель Task.
2. Импортируйте F класс, модуль timezone из фреймворка Django, модуль datetime.
3. Создайте переменную, где будет храниться определённая дата (месяц назад относительно текущей
даты).
4. Напишите запрос, который будет получать все задачи из конкретного проекта, например “TIGERˮ,
которые были созданы месяц назад.
5. Обновите приоритетность таких задач на самую высокую."""

