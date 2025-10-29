from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from itertools import count


app = FastAPI(title="Books CRUD API")


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    year: Optional[int] = Field(default=None, ge=0, le=3000)
    # поле id генерируется автоматически


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    year: Optional[int] = Field(default=None, ge=0, le=3000)


class Book(BookBase):
    id: int


# простое хранилище в виде словаря
book_id_counter = count(start=1)
books_storage: Dict[int, Book] = {}


def get_next_book_id() -> int:
    return next(book_id_counter)


@app.get("/books", response_model=List[Book])
async def list_books() -> List[Book]:
    return list(books_storage.values()) 


@app.get("/books/{book_id}", response_model=Book) 
async def get_book(book_id: int) -> Book:
    book = books_storage.get(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return book


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate) -> Book:
    new_id = get_next_book_id()
    book = Book(id=new_id, **payload.model_dump())
    books_storage[new_id] = book
    return book


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, payload: BookUpdate) -> Book:
    existing = books_storage.get(book_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    update_data = payload.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=update_data)
    books_storage[book_id] = updated
    return updated


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    if book_id not in books_storage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    del books_storage[book_id]
    return None

# стартовые данные
books_storage[get_next_book_id()] = Book(id=1, title="Преступление и наказание", author="Фёдор Достоевский", year=1866)
books_storage[get_next_book_id()] = Book(id=2, title="Война и мир", author="Лев Толстой", year=1869)
books_storage[get_next_book_id()] = Book(id=3, title="Мастер и Маргарита", author="Михаил Булгаков", year=1967)