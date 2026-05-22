from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))