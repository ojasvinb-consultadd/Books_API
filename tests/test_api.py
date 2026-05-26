import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture
async def client():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        yield client


async def test_get_books(client):

    response = await client.get("/books")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "booklist,response_code",
    [
        (
            [
                {
                    "book_title": "Atomic Habits",
                    "author": "James Clear",
                }
            ],
            201,
        ),
        (
            [
                {
                    "book_title": "Deep Work",
                    "author": "Cal Newport",
                },
                {
                    "book_title": "Clean Code",
                    "author": "Robert Martin",
                },
            ],
            201,
        ),
        (
            [],
            422,
        ),
        (
            [
                {
                    "book_title": "Missing Author",
                }
            ],
            422,
        ),
        (
            [
                {
                    "author": "Someone",
                }
            ],
            422,
        ),
        (
            [
                {
                    "book_title": 123,
                    "author": True,
                }
            ],
            422,
        ),
        (
            [
                {
                    "book_title": "",
                    "author": "",
                }
            ],
            201,  
        ),
    ],
)
async def test_create_books(
    client,
    booklist,
    response_code,
):

    response = await client.post(
        "/books",
        json=booklist,
    )

    assert response.status_code == response_code


async def test_patch_book(client):
    temp = await client.post(
        "/books",
        json=[
                {
                    "book_title": "",
                    "author": "",
                }
            ]
        )
    
    id = temp.json()[0]["id"]
    response = await client.patch(f"books/{id}", json={"author":"hello"})


    assert response.status_code == 200

    await client.delete(f"books/{id}")

async def test_delete_books(client):
    temp = await client.post(
        "/books",
        json=[
                {
                    "book_title": "",
                    "author": "",
                }
            ]
        )
    
    id = temp.json()[0]["id"]
    response = await client.delete(f"books/{id}")

    assert response.status_code == 204