# TeamBuilder

> Хакатон-проект команды geoguessr adeptus на **TulaHack 2026**

Веб-приложение для формирования сбалансированных команд. Платформа помогает участникам находить друг друга по навыкам и интересам, а организаторам — автоматически компоновать команды с помощью ИИ.

---

## Стек технологий

| Слой | Технологии |
|---|---|
| **Frontend** | Vue 3, JavaScript, CSS |
| **Backend** | Python, FastAPI, SQLAlchemy, Alembic |
| **База данных** | PostgreSQL 15 |
| **ИИ** | Google Gemini API |
| **Деплой** | Docker, Docker Compose |

---

## Структура проекта

```
tulahack-2026/
├── backend/           # FastAPI-приложение
│   ├── app/           # Исходный код
│   └── alembic/       # Миграции БД
├── frontend/          # Vue.js-приложение
├── task/              # Описание задания хакатона
├── docker-compose.yml
├── .env_example       # Пример переменных окружения
└── README.md
```

---

## Быстрый старт

### Требования

- [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/skylak33/tulahack-2026.git
cd tulahack-2026
```

### 2. Настроить переменные окружения

```bash
cp .env_example .env
```

Откройте `.env` и заполните необходимые значения:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=teambuilder
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=ваш-секретный-ключ
GEMINI_API_KEY=ваш-ключ-gemini-api
```

> Получить ключ Gemini API можно на [Google AI Studio](https://aistudio.google.com/).

### 3. Запустить приложение

```bash
docker compose up
```

После запуска:

- **Frontend** доступен на [http://localhost](http://localhost)
- **Backend API** доступен на [http://localhost:8000](http://localhost:8000)
- **Документация API** (Swagger) на [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Сервисы Docker Compose

| Сервис | Образ / Контекст | Порт |
|---|---|---|
| `db` | `postgres:15-alpine` | `5432` |
| `backend` | `./backend` | `8000` |
| `frontend` | `./frontend` | `80` |

---

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DB_USER` | Пользователь PostgreSQL | `postgres` |
| `DB_PASSWORD` | Пароль PostgreSQL | `postgres` |
| `DB_NAME` | Название базы данных | `teambuilder` |
| `DB_HOST` | Хост базы данных | `localhost` |
| `DB_PORT` | Порт базы данных | `5432` |
| `SECRET_KEY` | Секретный ключ для JWT | — |
| `GEMINI_API_KEY` | Ключ Google Gemini API | — |

---
