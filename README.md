Books CRUD API (на FastAPI)

Простое CRUD API для книг на FastAPI без фронтенда и БД

Требования:
- Python 3.11+

Установка(windows):
- python -m venv .venv
- .venv/Scripts/activate
- pip install -r requirements.txt

Запуск:
- uvicorn books_crud_api:app --reload

Приложение будет доступно на `http://127.0.0.1:8000`

Интерактивная документация:
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Эндпоинты:
- GET `/books` — список книг
- GET `/books/{book_id}` — книга по ID
- POST `/books` — создать книгу
- PUT `/books/{book_id}` — обновить книгу
- DELETE `/books/{book_id}` — удалить книгу

Примеры запросов (curl):
- curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"1984","author":"Джордж Оруэлл","year":1949}'

- curl http://127.0.0.1:8000/books

- curl -X PUT http://127.0.0.1:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"year":1948}'

- curl -X DELETE http://127.0.0.1:8000/books/1



