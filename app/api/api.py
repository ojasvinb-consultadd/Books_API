from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.DB.session import get_db
from app.DB.models import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter()




@router.get("/books")
async def get_all_books(db: AsyncSession = Depends(get_db)):
    smt = select(Book)
    result = await db.execute(smt)
    books = result.scalars().all()
    return books


@router.get("/books/{id}", response_model=BookResponse)
async def get_book(id: int, db: AsyncSession = Depends(get_db)):
    smt = select(Book).where(Book.id == id)
    result = await db.execute(smt)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(404, "Book not found")
    return book


@router.post("/books", response_model=list[BookResponse], status_code=status.HTTP_201_CREATED)
async def create_book(data: list[BookCreate], db: AsyncSession = Depends(get_db)):
    books = [Book(book_title=book.book_title, author=book.author) for book in data]
    db.add_all(books)
    await db.commit()
    for book in books:
        await db.refresh(book)
    return books


@router.patch("/books/{id}", response_model=BookResponse)
async def update_book(id: int, data: BookUpdate, db: AsyncSession = Depends(get_db)):
    smt = select(Book).where(Book.id == id)
    result = await db.execute(smt)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(404, "Book not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)
    await db.commit()
    await db.refresh(book)
    return book


@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, db: AsyncSession = Depends(get_db)):
    smt = select(Book).where(Book.id == id)
    result = await db.execute(smt)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(404, "Book not found")
    await db.delete(book)
    await db.commit()
