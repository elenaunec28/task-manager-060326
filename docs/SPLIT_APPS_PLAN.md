# Разделение core на apps/tasks и apps/projects

Oct 23, 2026 · @Viktor Khomenko

Переносим `core` в пакет `apps` и раскладываем его модели по двум новым приложениям: `apps/tasks` и `apps/projects`. Данные в базе и права групп сохраняются, адреса API не меняются. Состояние до разделения сохранено в ветке `before-apps-split` (коммит `eff73b8`). Все шаги сначала прогнаны на копии этой ветки вместе с её `db.sqlite3`, затем выполнены и влиты в `main`.

## Что получится

Все три приложения лежат в пакете `apps`. В `apps/core` остаются только абстрактные базовые модели, общий admin action и view `hello`. Все рабочие модели переезжают в `apps/tasks` и `apps/projects`.

```text
task-manager-060326/
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── admin.py            # только replace_spaces_with_underscores
│   │   ├── apps.py             # name = 'apps.core', label = 'core'
│   │   ├── migrations/         # 0001–0003 как были + 0004 (переезд моделей)
│   │   ├── models/
│   │   │   ├── __init__.py     # пустой
│   │   │   └── base.py         # UUIDv7Model, TimeStampedModel
│   │   ├── tests.py
│   │   ├── urls.py             # только hello
│   │   └── views.py            # только hello
│   ├── projects/
│   │   ├── __init__.py
│   │   ├── admin.py            # ProjectAdmin, ProjectFileAdmin
│   │   ├── apps.py             # name = 'apps.projects'
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── project.py      # Project, ProjectFile
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   └── projects.py     # AllProjectsSerializer
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py            # get_all_projects
│   └── tasks/
│       ├── __init__.py
│       ├── admin.py            # CategoryAdmin, TaskAdmin, SubTaskAdmin, TagAdmin
│       ├── apps.py             # name = 'apps.tasks'
│       ├── migrations/
│       │   ├── __init__.py
│       │   └── 0001_initial.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── category.py
│       │   ├── subtask.py
│       │   ├── tag.py
│       │   └── task.py
│       ├── serializers/
│       │   ├── __init__.py
│       │   ├── tags.py
│       │   └── tasks.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py            # tasks + tags endpoints
├── config/
├── docs/                       # PDF с заданиями, Postman-коллекция, этот план
└── manage.py
```

| Модель | Было | Стало | Таблица в БД |
| --- | --- | --- | --- |
| Task | core | apps.tasks | task\_manager\_task |
| SubTask | core | apps.tasks | task\_manager\_subtask |
| Category | core | apps.tasks | task\_manager\_category |
| Tag | core | apps.tasks | core\_tag, после шага 12 task\_manager\_tag |
| Project | core | apps.projects | task\_manager\_project |
| ProjectFile | core | apps.projects | task\_manager\_project\_file |
| UUIDv7Model, TimeStampedModel | core | apps.core | нет таблиц (abstract) |

**Почему нельзя просто перенести классы и запустить makemigrations + migrate.** Django узнаёт модель по паре «метка приложения (label) + имя». Если класс `Task` переехал из `core` в `tasks`, Django решит, что `core.Task` удалили, а `tasks.Task` создали. Миграция сделает DROP TABLE и CREATE TABLE, и все данные пропадут. Поэтому в шаге 10 мы оборачиваем миграции в `SeparateDatabaseAndState`. Это значит: «поменялось только описание моделей в Django, база остаётся как есть». Таблицы сохраняют свои имена, потому что у моделей явно задан `db_table`.

С самим `core` такой проблемы нет. У папки `apps/core` метка по-прежнему `core`, поэтому Django считает его тем же приложением, и перенос папки не требует миграций (проверено: `makemigrations --check` → `No changes detected`).

Assumption: `Category` и `Tag` относятся к задачам и идут в `apps.tasks`.

## Что берём у сокурсника

Раскладку папок берём из ветки `malcov_vitalii` (коммит `b5006a8 add task api vies`), но в текущем виде его проект не запускается. `python manage.py check` падает с `ImproperlyConfigured: Cannot import 'core'`. Ниже список: что перенимаем и чего избегаем.

| Что | У сокурсника | Как делаем мы |
| --- | --- | --- |
| Папки `apps/core`, `apps/tasks`, `apps/projects`, пакеты `models/` и `serializers/` внутри приложений | Есть | Берём как есть |
| Общий action `replace_spaces_with_underscores` импортируется в admin каждого приложения | Есть | Берём, импорт из `apps.core.admin` |
| `apps/core/apps.py` | Осталось `name = 'core'`, поэтому падает `check` | `name = 'apps.core'`, `label = 'core'` |
| Импорт базовых моделей | `from models.base import ...`: такого модуля нет | `from apps.core.models.base import ...` |
| `apps/core/models/__init__.py` | Реэкспортирует модели из tasks/projects, а код по-прежнему импортирует `from core.models` | Файл пустой, каждый импортирует из своего приложения |
| `apps/tasks/models.py` рядом с папкой `models/` | Оставлен, конфликт имён | Удаляем `models.py` |
| Миграции новых приложений | Нет. Обычный makemigrations + migrate удалит данные | `SeparateDatabaseAndState`, шаг 10 |
| `Tag` без `db_table` | В новом приложении Django искал бы таблицу `tasks_tag` | `db_table = "core_tag"` |
| Подключение urls | `path('projects/', include(...))`, а внутри снова `'projects/'`. Адрес становится `/projects/projects/`, Postman-коллекция ломается | `path('', include(...))`, адреса прежние |
| views | Лежат в `tasks_wiews/`, а `tasks/urls.py` импортирует из несуществующего `.views` | Один `views.py` на приложение |
| `apps/tasks/admin.py` | Нет импортов `timezone` и `messages`: action «Закрыто» упадёт с `NameError` | Импорты есть |

## Шаг 0. Подготовка

Исходная точка — ветка `before-apps-split` на GitHub. Это снимок проекта до разделения (коммит `eff73b8`), её не меняем. Перенос делается в новой ветке `split-apps` от этого снимка, а в конце вливается в `main` (шаг 13). Перенос делает один человек, остальные потом только забирают `main` (см. раздел для команды). Команды ниже выполняются из корня проекта (там, где `manage.py`), с активированным `.venv`. Примеры команд даны для PowerShell.

1. Рабочая папка должна быть чистой: `git status` ничего не показывает. Если есть незакоммиченные правки, закоммитьте их в своей ветке до начала.
2. Забрать снимок и создать от него рабочую ветку:

   ```powershell
   git fetch origin
   git switch before-apps-split
   git switch -c split-apps
   ```

   `git switch before-apps-split` сам создаст локальную ветку из `origin/before-apps-split`, если её ещё нет. `split-apps` начинается ровно с состояния до разделения: `core` в корне, папки `apps` нет.
3. Отдельный бэкап базы не нужен. `db.sqlite3` хранится в git (учебный проект, так задумано), и если что-то пойдёт не так, её можно вернуть так:

   ```powershell
   git restore db.sqlite3
   ```
4. Все миграции `core` должны быть применены. Новые миграции строятся поверх `core 0003`:

   ```powershell
   python manage.py showmigrations core
   ```

   Ожидается три строки с `[X]`, последняя `0003_project_projectfile_tag_alter_task_options_and_more`. Если где-то `[ ]`, сначала `python manage.py migrate`.
5. Проект должен быть здоров до начала работы:

   ```powershell
   python manage.py check
   ```

   Ожидается `System check identified no issues (0 silenced).`

## Шаги 1–3. Папка apps, перенос core, новые приложения

### Шаг 1. Создать пакет apps и перенести в него core

Это чистый перенос папки без изменения моделей. Его удобно сделать отдельным коммитом: если дальше что-то сломается, его не нужно переделывать.

1. Создать папку `apps` и пустой `apps/__init__.py` (в PyCharm: New → Python Package → `apps`). `__init__.py` делает `apps` пакетом, иначе не сработает `import apps.core`.
2. Перенести папку через git, чтобы сохранилась история файлов:

   ```powershell
   git mv core apps/core
   ```

   `git mv` переносит только файлы из git. Старая папка `core/` останется, и в ней будут только `__pycache__`. Удалите её: если её оставить, Python продолжит видеть пакет с именем `core`.
3. **Файл `apps/core/apps.py`** — указать новый путь и зафиксировать метку:

   ```python
   from django.apps import AppConfig
   
   
   class CoreConfig(AppConfig):
       name = 'apps.core'
       label = 'core'
   ```

   `name` — это путь для импорта. `label` — имя приложения, которое хранится в базе (таблицы `django_migrations`, `django_content_type`) и в миграциях (`'core.project'`). По умолчанию Django и так берёт последнюю часть `name`, то есть `core`. Явная строка нужна, чтобы метку никто не поменял случайно. С другой меткой Django посчитал бы приложение новым и потерял историю миграций.
4. **Файл `config/settings.py`**, список `INSTALLED_APPS`: строку `'core',` заменить на `'apps.core',`.
5. **Файл `config/urls.py`**: `include('core.urls')` заменить на `include('apps.core.urls')`.
6. Импорты `from core.models` заменить на `from apps.core.models` в этих файлах (относительные импорты `from .base` не трогаем):
   - `apps/core/models/tag.py`
   - `apps/core/serializers/projects.py`, `tags.py`, `tasks.py`
   - `apps/core/views.py`
   - `orm1.py`, `orm4.py` (строка 14)
7. Проверка. Вторая команда подтверждает, что перенос папки не потребовал миграций:

   ```powershell
   python manage.py check
   python manage.py makemigrations --check --dry-run
   ```

   Ожидается `System check identified no issues (0 silenced).` и `No changes detected`. После этого можно сделать коммит «Move core into apps package».

### Шаг 2. Создать приложения tasks и projects

`startapp` создаёт каркас приложения в уже существующей папке, поэтому сначала создаём папки:

```powershell
mkdir apps/tasks, apps/projects
python manage.py startapp tasks apps/tasks
python manage.py startapp projects apps/projects
```

После этого:

1. **Файл `apps/tasks/apps.py`**: `name = 'tasks'` → `name = 'apps.tasks'`.
2. **Файл `apps/projects/apps.py`**: `name = 'projects'` → `name = 'apps.projects'`. `startapp` записывает короткое имя (проверено). С ним Django стал бы искать модуль `tasks` в корне проекта. Метки получатся `tasks` и `projects`, они понадобятся в строках вида `"projects.Project"`.
3. Удалить `apps/tasks/models.py` и `apps/projects/models.py`. Вместо них будут папки `models/`. Модуль `models.py` и пакет `models/` с одним именем конфликтуют.
4. Создать папки под перенос. `git mv` в следующих шагах требует, чтобы папка назначения уже существовала:

   ```powershell
   mkdir apps/tasks/models, apps/tasks/serializers, apps/projects/models, apps/projects/serializers
   ```

### Шаг 3. Подключить приложения

**Файл `config/settings.py`**, `INSTALLED_APPS` — добавить две строки после `'apps.core'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.core',
    'apps.tasks',
    'apps.projects',
]
```

Полный путь к классу (`apps.tasks.apps.TasksConfig`) писать не нужно: Django сам найдёт единственный `AppConfig` в `apps.py`. В текущей заготовке в `settings.py` написано `'apps.tasks.apps.TaskConfig'`, а класс называется `TasksConfig`. Из-за этого падает `ImportError`.

## Шаги 4–5. Перенос моделей

### Шаг 4. Перенести файлы моделей

Файлы переносим целиком через `git mv`, а не копированием. Так git видит переименование, и в старом месте не остаётся дубликат класса.

```powershell
git mv apps/core/models/task.py apps/core/models/subtask.py apps/core/models/category.py apps/core/models/tag.py apps/tasks/models/
git mv apps/core/models/project.py apps/projects/models/
```

В `apps/core/models/` остаются только `__init__.py` и `base.py`.

### Шаг 5. Поправить код внутри перенесённых моделей

После переноса `from .base import ...` указывает на несуществующий файл, потому что `base.py` остался в `apps/core`. Базовые классы импортируем по абсолютному пути.

1. **Файл `apps/tasks/models/task.py`** — две правки:

   ```python
   # было
   from .base import TimeStampedModel, UUIDv7Model
   # стало
   from apps.core.models.base import TimeStampedModel, UUIDv7Model
   ```

   ```python
   # было
   project = models.ForeignKey("Project", related_name="tasks", on_delete=models.CASCADE)
   # стало
   project = models.ForeignKey("projects.Project", related_name="tasks", on_delete=models.CASCADE)
   ```

   Строка без метки (`"Project"`) ищет модель в том же приложении. `Project` теперь в другом, поэтому пишем `"projects.Project"`. `"Category"` и `"Tag"` не трогаем: они в том же `tasks`.
2. **Файл `apps/tasks/models/subtask.py`**: строку `from .base import TimeStampedModel, UUIDv7Model` заменить на `from apps.core.models.base import TimeStampedModel, UUIDv7Model`. Строка `from .task import Task` остаётся.
3. **Файл `apps/tasks/models/category.py`**: `from .base import UUIDv7Model` → `from apps.core.models.base import UUIDv7Model`.
4. **Файл `apps/tasks/models/tag.py`**: импорт уже исправлен в шаге 1. Добавить в `Meta` строку `db_table`:

   ```python
   class Meta:
       db_table = "core_tag"
       ordering = ["name"]
       verbose_name = "Tag"
       verbose_name_plural = "Tags"
   ```

   Сейчас таблица тегов называется `core_tag`. Это имя по умолчанию: метка приложения + имя модели. В приложении `tasks` имя по умолчанию стало бы `tasks_tag`, и Django не нашёл бы старые данные. Остальные модели уже имеют `db_table`.
5. **Файл `apps/projects/models/project.py`**: `from .base import TimeStampedModel, UUIDv7Model` → `from apps.core.models.base import TimeStampedModel, UUIDv7Model`.
6. **Файл `apps/tasks/models/__init__.py`** (создать):

   ```python
   from .category import Category
   from .task import Task
   from .subtask import SubTask
   from .tag import Tag
   
   __all__ = ("Category", "Task", "SubTask", "Tag")
   ```
7. **Файл `apps/projects/models/__init__.py`** (создать):

   ```python
   from .project import Project, ProjectFile
   
   __all__ = ("Project", "ProjectFile")
   ```

   Django ищет модели приложения в `<app>.models`. Импорт в `__init__.py` регистрирует их и позволяет писать `from apps.tasks.models import Task`.
8. **Файл `apps/core/models/__init__.py`**: удалить всё содержимое, файл оставить пустым. Старые импорты указывают на файлы, которых здесь больше нет. Реэкспорт из других приложений, как у сокурсника, создаёт путаницу и циклические импорты. `base.py` импортируется напрямую: `from apps.core.models.base import ...`.

## Шаги 6–9. Сериализаторы, views, urls, admin

Принцип один: код лежит в том приложении, чью модель он использует. Тела функций не меняются, меняются только файлы и импорты.

### Шаг 6. Сериализаторы

```powershell
git mv apps/core/serializers/tasks.py apps/core/serializers/tags.py apps/tasks/serializers/
git mv apps/core/serializers/projects.py apps/projects/serializers/
git rm apps/core/serializers/__init__.py
```

1. **`apps/projects/serializers/projects.py`**: `from apps.core.models import Project` → `from apps.projects.models import Project`.
2. **`apps/tasks/serializers/tags.py`**: `from apps.core.models import Tag` → `from apps.tasks.models import Tag`.
3. **`apps/tasks/serializers/tasks.py`**: `from apps.core.models import Task` → `from apps.tasks.models import Task`.
4. **`apps/projects/serializers/__init__.py`** (создать):

   ```python
   from .projects import AllProjectsSerializer
   ```
5. **`apps/tasks/serializers/__init__.py`** (создать):

   ```python
   from .tasks import TaskSerializer
   from .tags import TagSerializer
   ```

### Шаг 7. Views

**Файл `apps/projects/views.py`** (заменить содержимое полностью). Сюда переезжает `get_all_projects` из `apps/core/views.py`:

```python
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.projects.models import Project
from apps.projects.serializers import AllProjectsSerializer


@api_view(['GET'])
def get_all_projects(request: Request):
    projects = Project.objects.all()
    serializer = AllProjectsSerializer(projects, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
```

**Файл `apps/tasks/views.py`** (заменить содержимое полностью). Вверху файла импорты, ниже шесть функций из `apps/core/views.py` без изменений: `get_all_tasks`, `get_task_by_project_name`, `get_all_tags`, `get_tag_by_id`, `update_tag`, `create_tag`.

```python
from uuid import UUID

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request

from apps.tasks.models import Tag, Task
from apps.tasks.serializers import TagSerializer, TaskSerializer


# сюда шесть функций с @api_view из apps/core/views.py, как есть
```

**Файл `apps/core/views.py`**: остаётся только `hello`. Импорты, которые стали не нужны, удаляем вместе с функциями:

```python
from django.http import HttpResponse


def hello(request, name):
    return HttpResponse(f'Hello, {name}!')
```

### Шаг 8. URLs

**Файл `apps/projects/urls.py`** (создать):

```python
from django.urls import path

from .views import get_all_projects

app_name = 'projects'

urlpatterns = [
    path('projects/', get_all_projects, name='get_all_projects'),
]
```

**Файл `apps/tasks/urls.py`** (создать):

```python
from django.urls import path

from .views import (
    create_tag,
    get_all_tags,
    get_all_tasks,
    get_tag_by_id,
    get_task_by_project_name,
    update_tag,
)

app_name = 'tasks'

urlpatterns = [
    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/<str:name>/', get_task_by_project_name, name='get_task_by_project_name'),
    path('tags/', get_all_tags, name='get_all_tags'),
    path('tags/<uuid:tag_id>/', get_tag_by_id, name='get_tag_by_id'),
    path('tags/<uuid:tag_id>/update/', update_tag, name='update_tag'),
    path('tags/create/', create_tag, name='create_tag'),
]
```

**Файл `apps/core/urls.py`** (заменить содержимое):

```python
from django.urls import path

from .views import hello

app_name = 'core'

urlpatterns = [
    path('<str:name>/', hello, name='hello'),
]
```

**Файл `config/urls.py`**, список `urlpatterns`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.projects.urls')),
    path('', include('apps.tasks.urls')),
    path('', include('apps.core.urls')),  # catch-all '<str:name>/' must stay last
]
```

Порядок важен. В `core` есть маршрут `<str:name>/`, и он перехватит `/projects/`, `/tasks/` и `/tags/`, если стоит раньше. Префикс `''` оставляет адреса прежними, поэтому Postman-коллекция `docs/task060326.postman_collection.json` продолжает работать.

### Шаг 9. Admin и orm-скрипты

**Файл `apps/core/admin.py`**: оставить импорты `admin, messages`, `timezone` и функцию `replace_spaces_with_underscores`. Удалить строку `from .models import ...` и все классы `@admin.register(...)`: они переезжают ниже.

**Файл `apps/projects/admin.py`** (заменить содержимое):

```python
from django.contrib import admin

from apps.core.admin import replace_spaces_with_underscores
from apps.projects.models import Project, ProjectFile


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
```

**Файл `apps/tasks/admin.py`** (заменить содержимое). Классы `CategoryAdmin`, `TaskAdmin` (вместе с `update_status_to_closed`), `SubTaskAdmin` и `TagAdmin` переносятся из старого `core/admin.py` без изменений. Новая только шапка файла:

```python
from django.contrib import admin, messages
from django.utils import timezone

from apps.core.admin import replace_spaces_with_underscores
from apps.tasks.models import Category, SubTask, Tag, Task


# далее CategoryAdmin, TaskAdmin, SubTaskAdmin, TagAdmin из старого core/admin.py, как есть
```

`messages` и `timezone` нужны для `update_status_to_closed`. Именно их забыл сокурсник.

**Файлы `orm1.py` и `orm4.py`**, строка 14 (после шага 1 она выглядит так: `from apps.core.models import Tag, Project, ProjectFile, Task, Category`). Заменить на:

```python
from apps.tasks.models import Tag, Task, Category
from apps.projects.models import Project, ProjectFile
```

Промежуточная проверка: `python manage.py check` → `System check identified no issues (0 silenced).`

## Шаг 10. Миграции без потери данных

Самый важный шаг. Django сам создаст миграции, но в них будут реальные DROP TABLE и CREATE TABLE. Мы вручную превращаем их в миграции «только для описания моделей». **Не запускайте `migrate`, пока не правятся все три файла.**

### 10.1. Сгенерировать миграции

```powershell
python manage.py makemigrations
```

Появятся три файла (имя файла в `core` может отличаться, ориентируйтесь на номер `0004`):

- `apps/projects/migrations/0001_initial.py`: Create model ProjectFile, Project
- `apps/tasks/migrations/0001_initial.py`: Create model Category, Tag, Task, SubTask
- `apps/core/migrations/0004_remove_project_unique_project_title_description_and_more.py`: Remove field …, Delete model …

### 10.2. Обернуть операции в SeparateDatabaseAndState

Во всех трёх файлах делаем одно и то же. Всё, что было внутри `operations = [ ... ]`, переносим в `state_operations`, а `database_operations` оставляем пустым. Операции внутри не меняем. В PyCharm удобно выделить старый блок и дважды нажать Tab.

```python
# было
operations = [
    migrations.CreateModel(...),
    migrations.CreateModel(...),
]

# стало
operations = [
    migrations.SeparateDatabaseAndState(
        state_operations=[
            migrations.CreateModel(...),
            migrations.CreateModel(...),
        ],
        database_operations=[],
    ),
]
```

### 10.3. Дописать зависимости

**Файл `apps/projects/migrations/0001_initial.py`**, добавить в `dependencies`:

```python
dependencies = [
    ('core', '0003_project_projectfile_tag_alter_task_options_and_more'),
]
```

**Файл `apps/tasks/migrations/0001_initial.py`**, добавить первой строкой (две остальные Django уже написал):

```python
dependencies = [
    ('core', '0003_project_projectfile_tag_alter_task_options_and_more'),
    ('projects', '0001_initial'),
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
]
```

Зачем это нужно: на новой пустой базе (у нового участника, в тестах) таблицы по-прежнему создают миграции `core` 0001–0003. Новые приложения должны идти после них.

### 10.4. Миграция core 0004: зависимости и перенос content types

**Файл `apps/core/migrations/0004_remove_project_unique_project_title_description_and_more.py`.** Кроме обёртки из 10.2 сделать две вещи:

1. `core` удаляет модели из своего описания только после того, как новые приложения их забрали. Поэтому в зависимости добавляем их миграции.
2. Переносим записи в `django_content_type` с `core` на новые приложения. К этим записям привязаны права (`core.add_task` и т.д.), выданные группам Manager, Client и Developer, и история действий в админке. Без этого Django создаст новые права `tasks.add_task`, а группы потеряют доступ.

Итоговая шапка и структура файла (операции Django внутри `state_operations` остаются свои, их 17 штук):

```python
from django.db import migrations

MOVED_MODELS = {
    "category": "tasks",
    "subtask": "tasks",
    "tag": "tasks",
    "task": "tasks",
    "project": "projects",
    "projectfile": "projects",
}


def move_content_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    for model, app_label in MOVED_MODELS.items():
        ContentType.objects.filter(app_label="core", model=model).update(app_label=app_label)


def return_content_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    for model, app_label in MOVED_MODELS.items():
        ContentType.objects.filter(app_label=app_label, model=model).update(app_label="core")


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('tasks', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0003_project_projectfile_tag_alter_task_options_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveConstraint(
                    model_name='project',
                    name='unique_project_title_description',
                ),
                # ... остальные RemoveField / RemoveConstraint / DeleteModel как сгенерировал Django
                migrations.DeleteModel(
                    name='Task',
                ),
            ],
            database_operations=[],
        ),
        migrations.RunPython(move_content_types, return_content_types),
    ]
```

`return_content_types` нужна для отката миграции (`migrate core 0003`). Код в `RunPython` обращается к модели через `apps.get_model`, а не через обычный импорт. Так принято в миграциях: они должны работать с версией модели на момент миграции.

### 10.5. Проверить до применения и применить

```powershell
python manage.py makemigrations --check --dry-run
python manage.py migrate --plan
```

- Первая команда должна написать `No changes detected`. Это значит, что модели в коде и миграции совпадают.
- В плане должны быть только `Custom state/database change combination` и одна `Raw Python operation`. Если видно `Create model` или `Delete model`, какая-то миграция не обёрнута. Вернитесь к 10.2.

После этого:

```powershell
python manage.py migrate
```

Ожидаемый вывод (получен на копии вашей базы):

```text
Running migrations:
  Applying projects.0001_initial... OK
  Applying tasks.0001_initial... OK
  Applying core.0004_remove_project_unique_project_title_description_and_more... OK
```

## Шаг 11. Проверка и коммит

Работа считается сделанной, когда проходят все проверки ниже. В столбце «Результат на копии» показано, что выдал прогон на копии `before-apps-split` с её `db.sqlite3`.

| Проверка | Команда | Результат на копии |
| --- | --- | --- |
| Проект запускается | `python manage.py check` | `System check identified no issues (0 silenced).` |
| Модели и миграции совпадают | `python manage.py makemigrations --check --dry-run` | `No changes detected` |
| Данные на месте | скрипт ниже | `tasks 6 tags 7 cats 1 projects 5 files 3` (столько же, сколько было до переноса) |
| Права групп сохранились | скрипт ниже | `Manager ['auth', 'projects', 'tasks']`, то же для Client и Developer |
| API отвечает по старым адресам | `python manage.py runserver` + Postman-коллекция или браузер | `/projects/`, `/tasks/`, `/tasks/Project1/`, `/tags/`, `/tags/<id>/`, `/Alice/` → 200; `POST /tags/create/` → 201; `/admin/login/` → 200 |
| С нуля миграции тоже работают | `python manage.py test` | Тестовая база создаётся из миграций без ошибок. Единственный тест падает `404 != 200`, но он падает и на `before-apps-split` (см. последний раздел) |

Скрипт для данных и прав. Выполните `python manage.py shell` и вставьте:

```python
from apps.tasks.models import Task, Tag, Category
from apps.projects.models import Project, ProjectFile
from django.contrib.auth.models import Group

print('tasks', Task.objects.count(), 'tags', Tag.objects.count(), 'cats', Category.objects.count(),
      'projects', Project.objects.count(), 'files', ProjectFile.objects.count())
for g in Group.objects.all():
    print(g.name, sorted(set(g.permissions.values_list('content_type__app_label', flat=True))))
```

У вас числа могут отличаться. Сравнивайте с тем, что было в вашей базе до переноса. В списке прав групп не должно остаться `core`.

Коммит. В него должны попасть новые файлы, три миграции и мигрированная `db.sqlite3`: база хранится в репозитории умышленно, и в каждой ветке остаётся своя её версия. Перед коммитом проверьте `git status`: там не должно быть файлов `__pycache__`.

```powershell
git add apps config orm1.py orm4.py db.sqlite3
git status
git commit -m "Split core models into apps.tasks and apps.projects"
```

## Шаг 12. Переименовать таблицу тегов

Приводим все таблицы к виду `task_manager_*`. В отличие от шага 10, здесь меняется сама база, поэтому это отдельный коммит после шага 11, вместе с обновлённой `db.sqlite3`.

1. **Файл `apps/tasks/models/tag.py`**: в `Meta` заменить `db_table = "core_tag"` на `db_table = "task_manager_tag"`.
2. Создать и применить миграцию. Здесь оборачивать ничего не нужно:

   ```powershell
   python manage.py makemigrations tasks
   python manage.py migrate
   ```

   На копии получилось `apps\tasks\migrations\0002_alter_tag_table.py` с операцией `Rename table for tag to task_manager_tag` и `Applying tasks.0002_alter_tag_table... OK`. Связи задач с тегами сохранились.
3. Перезапустить `runserver`. Уже запущенный без автоперезагрузки сервер будет искать старую таблицу и вернёт `OperationalError: no such table: core_tag`.
4. Коммит:

   ```powershell
   git add apps/tasks db.sqlite3
   git commit -m "Rename tag table to task_manager_tag"
   ```

В вашей ранней заготовке `tag.py` были ещё два изменения. Их лучше не смешивать с переносом:

- `MinLengthValidator(4)` для `name` можно добавить отдельным коммитом. Это новая функциональность, а не часть переноса.
- `class Tag(models.Model)` вместо `UUIDv7Model` меняет первичный ключ с UUID на число. Это сломает существующие связи в `task_manager_task_tag` и адреса `tags/<uuid:tag_id>/`. Не делать без отдельного решения команды.

## Шаг 13. Влить в main и отправить на GitHub

`split-apps` начиналась от `before-apps-split`, а `main` с тех пор не менялась, поэтому слияние проходит без конфликтов (fast-forward). Сама `before-apps-split` остаётся снимком и не меняется.

```powershell
git switch main
git pull
git merge split-apps
git push origin main
git branch -d split-apps
```

Если `git merge` сообщает о конфликтах, значит в `main` за это время появились чужие коммиты. Остановитесь и разберите их вместе с автором.

## Для остальных участников команды

Миграции создаёт один человек (шаги 0–13). Остальные их не генерируют. В `main` вместе с миграциями лежит уже мигрированная `db.sqlite3`, поэтому с базой из `main` `migrate` просто ответит `No migrations to apply`. Если вы работаете со своей базой из другой ветки, миграции применяются к ней: они работают для любой базы, где применена `core 0003`.

1. До слияния ветки не менять модели и не создавать новые миграции в `core`. Иначе появятся две разные `0004` и конфликт миграций.
2. После слияния закоммитить свои незаконченные правки в своей ветке и забрать изменения:

   ```powershell
   git switch main
   git pull
   ```
3. Применить миграции. `makemigrations` не запускать, все миграции уже в репозитории:

   ```powershell
   python manage.py migrate
   python manage.py makemigrations --check --dry-run
   ```

   Вторая команда должна написать `No changes detected`.
4. Поправить импорты в своей рабочей ветке. Везде, где есть `from core.models import ...`, нужен импорт из нового места:
   - `Task`, `SubTask`, `Category`, `Tag` → `from apps.tasks.models import ...`
   - `Project`, `ProjectFile` → `from apps.projects.models import ...`
   - `UUIDv7Model`, `TimeStampedModel` → `from apps.core.models.base import ...`
5. Если `migrate` упал, верните базу командой `git restore db.sqlite3` и пришлите вывод тому, кто делал перенос.

## Что найдено, но не входит в этот план

Эти проблемы есть уже на `before-apps-split`, перенос их не создаёт и не исправляет. Исправлять лучше отдельными задачами.

| Проблема | Где | Что происходит |
| --- | --- | --- |
| Тест запрашивает `/hello/Alice/`, а маршрут `<str:name>/` принимает только один сегмент пути | `apps/core/tests.py` | `python manage.py test` → `AssertionError: 404 != 200` |
| `requirements.txt` сохранён в кодировке UTF-16, и в нём нет `djangorestframework` (в `.venv` стоит 3.18.3) | `requirements.txt` | У нового участника после `make install` не будет DRF, и проект не запустится (needs verification: выполнить `make install` в чистой папке) |
| `replace_spaces_with_underscores` обращается к `obj.title`, а у `Category` и `Tag` поле называется `name` | admin action | Действие на категориях и тегах упадёт с `AttributeError` |
| Вариант с MySQL (`MYSQL=True` в `.env`) не проверялся | `config/settings.py` | needs verification: прогнать шаги 10–12 на копии MySQL-базы |
