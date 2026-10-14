# VPe04 — GitHub Actions, Docker и GitFlow

[![Build, test and publish](https://github.com/vtaranov/zerocoder-vpe04-github-actions/actions/workflows/deploy.yml/badge.svg)](https://github.com/vtaranov/zerocoder-vpe04-github-actions/actions/workflows/deploy.yml)

Домашнее задание урока VPe04 курса «Профессия вайб-кодер».
Простое Flask-приложение собирается в Docker-образ и публикуется в GitHub Container Registry при push в `main`.
**Пункт 3 — деплой на сервер через SSH-Action — исключён по условию задания.**

## Выполнение требований

| Пункт ДЗ | Реализация |
| --- | --- |
| 1. Простой Flask/FastAPI-проект | `app.py`, Flask, Gunicorn |
| 2. `.github/workflows/deploy.yml`, push в main, Docker и GHCR | Workflow собирает образ, проверяет API и публикует `latest` и `sha-<commit>` |
| 3. SSH-деплой (не требуется) | SSH-Action и job для серверного деплоя отсутствуют |
| 4. Проверка workflow | Результаты доступны во вкладке [Actions](https://github.com/vtaranov/zerocoder-vpe04-github-actions/actions) |
| 5. Проект на GitHub | Этот репозиторий |

## Приложение

- `GET /` — название проекта и список эндпоинтов.
- `GET /health` — `{ "status": "ok" }`.
- Неизвестный адрес — HTTP 404.

## Запуск через Docker

```bash
docker build -t vpe04-demo .
docker run --rm --name vpe04-demo -p 127.0.0.1:8000:8000 vpe04-demo
```

Приложение: <http://localhost:8000>. Проверка: <http://localhost:8000/health>.

```bash
docker run --rm vpe04-demo python -m unittest discover -s tests -v
python3 scripts/smoke_test.py
```

Для HTTP-проверки контейнер должен работать. В образе зависимости устанавливаются из `requirements.txt`; локальный Python нужен только для smoke test, использующего стандартную библиотеку.

## Как работает workflow

1. При push в `main` или `develop`, при PR в эти ветки, а также при ручном запуске GitHub Actions получает код.
2. Собирает Docker-образ из `Dockerfile`.
3. Запускает unit-тесты внутри образа и проверяет настоящий HTTP API в запущенном контейнере.
4. Только для `main` авторизуется в `ghcr.io` и отправляет **тот же проверенный образ** с тегами `latest` и `sha-<полный SHA коммита>`.
5. Выполняет `docker pull` опубликованного тега и записывает digest в Job Summary.

Публикация использует встроенный `GITHUB_TOKEN` с `packages: write` и `contents: read`, как в [документации GitHub](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images). Добавлять PAT, Docker Hub credentials или SSH secrets не требуется. Actions закреплены по SHA; версии Python-зависимостей указаны явно.

Пакет: [GitHub Container Registry](https://github.com/users/vtaranov/packages/container/package/zerocoder-vpe04-github-actions).
Имя образа: `ghcr.io/vtaranov/zerocoder-vpe04-github-actions`.
GitHub создаёт новые container packages приватными по умолчанию: ссылка на исходный репозиторий публична, а доступ к пакету регулируется отдельно в настройках GHCR.

## GitFlow

`main` содержит стабильную версию. Работа над новой функциональностью ведётся в `develop`, затем через Pull Request попадает в `main`. PR запускает сборку и тесты без публикации, а merge в `main` запускает публикацию образа. Для дальнейшей работы можно создавать `feature/*` от `develop`; для релизов и срочных исправлений — `release/*` и `hotfix/*`.

## Структура

```text
.github/workflows/deploy.yml  # сборка, тесты, публикация GHCR
app.py                        # Flask API
Dockerfile                    # Python + Gunicorn, непривилегированный пользователь
requirements.txt              # версии зависимостей
tests/test_app.py             # unit-тесты API
scripts/smoke_test.py          # проверка HTTP-сервера
```
