from sqlalchemy.ext.asyncio import (create_async_engine, AsyncSession,async_sessionmaker)
from app.config.config import settings

engine = create_async_engine(settings.DB_URL,echo=False) ## this will connect to the db url specified in app/config/config

localsession = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_db():
    async with localsession() as session: ## context manager which automatically closes session after work is done
        yield session