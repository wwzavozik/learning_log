# Learning Log

Учебный проект **Learning Log** (Django 5.2 LTS, Python 3.12): приложение-журнал,
где пользователь ведёт темы и записи. Есть регистрация и вход, каждая тема
принадлежит конкретному пользователю, чужие данные недоступны. Оформление —
Bootstrap 4 (django-bootstrap4). Продакшен-запуск — Gunicorn + WhiteNoise
в Docker Compose.

## Структура проекта

```text
learning_log/
├── manage.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env                  # создаётся вручную (см. ниже), в git не попадает
├── learning_log/         # настройки проекта (settings.py, urls.py, wsgi.py)
├── learning_logs/        # основное приложение: модели, формы, страницы
└── users/                # регистрация, вход и выход
```

## Локальный запуск (без Docker)

```sh
python3.12 -m venv ll_env
source ll_env/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Проект открывается по адресу http://127.0.0.1:8000/, админка — http://127.0.0.1:8000/admin/.

Тесты: `python manage.py test` (ожидается `Ran 4 tests ... OK`).

## Запуск через Docker Compose

```sh
docker compose up -d --build
```

При старте контейнера автоматически выполняются `migrate`, `collectstatic`
и запуск Gunicorn на порту 8000. SQLite-база хранится в именованном томе
`learning_log_data`, поэтому данные не теряются при пересоздании контейнера.

## Переменные окружения (.env)

Файл `.env` кладётся рядом с `compose.yaml` и **не загружается в git**.
Пример:

```dotenv
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=192.168.1.11,localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://192.168.1.11:20010
DJANGO_USE_HTTPS=False
SQLITE_PATH=/app/data/db.sqlite3
APP_BIND_IP=0.0.0.0
APP_PORT=20010
```

| Переменная | Назначение |
|---|---|
| `DJANGO_SECRET_KEY` | Секретный ключ Django (на сервере — свой длинный случайный) |
| `DJANGO_DEBUG` | `True` только для разработки, на сервере — `False` |
| `DJANGO_ALLOWED_HOSTS` | Хосты, которым разрешено обслуживать приложение, через запятую |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Полные origins (схема://адрес:порт) для CSRF-защиты |
| `DJANGO_USE_HTTPS` | `True`, если сайт доступен по HTTPS (ставит Secure-флаги на cookie) |
| `SQLITE_PATH` | Путь к файлу базы SQLite (в контейнере — `/app/data/db.sqlite3`) |
| `APP_BIND_IP` | Адрес, на котором публикуется порт контейнера |
| `APP_PORT` | Внешний порт для доступа к приложению |

В Docker образ `python:3.12-slim` использует ту же версию Python, что и локальное
виртуальное окружение `ll_env` (Python 3.12).
