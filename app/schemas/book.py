from pydantic import BaseModel

class BookCreate(BaseModel):
    book_title: str
    author: str


class BookResponse(BaseModel):
    id: int
    book_title: str
    author: str

    model_config = {
        "from_attributes" : True
    }

class BookUpdate(BaseModel):
    book_title: str | None = None
    author: str | None = None