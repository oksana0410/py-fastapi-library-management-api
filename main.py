from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


@app.get("/")
async def root():
    return {"greeting": "Hello world"}


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


# Books endpoints
@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    books = crud.get_books(db=db, skip=skip, limit=limit)
    return books


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    books = crud.get_books_by_author(db=db, author_id=author_id)
    return books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book