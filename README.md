# Organization API

REST API приложение для справочника организаций, зданий и видов деятельности.

## Технологии

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker

## Установка и запуск

### Через Docker (рекомендуется)

1. Клонируйте репозиторий
2. Запустите контейнеры:

```bash
docker compose up --build
```

Приложение будет доступно по адресу: <http://localhost:8000>

Документация API: <http://localhost:8000/docs>

### Локальный запуск

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` с настройками базы данных

3. Примените миграции:

```bash
alembic upgrade head
```

4. Запустите сервер:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

Все запросы требуют заголовок `X-API-Key` с валидным ключом.

### Организации

- `GET /organizations/{organization_id}` - получить организацию по ID
- `GET /organizations/?building_id={id}` - список организаций в здании
- `GET /organizations/?activity_id={id}` - список организаций по виду деятельности (с вложенными)
- `GET /organizations/?name={name}` - поиск по названию
- `GET /organizations/?latitude={lat}&longitude={lon}&radius_km={radius}` - поиск в радиусе
- `GET /organizations/?lat1={lat1}&lon1={lon1}&lat2={lat2}&lon2={lon2}` - поиск в прямоугольной области

### Здания

- `GET /buildings/` - список всех зданий

### Виды деятельности

- `GET /activities/` - список всех видов деятельности

## Тестовые данные

При первом запуске автоматически создаются тестовые данные с организациями, зданиями и видами деятельности.

Для теста API доступен скрипт bash `test_api.sh`

```bash
./test_api.sh
```
