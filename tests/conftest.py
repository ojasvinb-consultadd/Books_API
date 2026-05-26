import pytest_asyncio

from app.DB.session import engine


# runs once for whole test session
@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup():

    yield

    # VERY IMPORTANT
    # closes all asyncpg connections cleanly
    await engine.dispose()