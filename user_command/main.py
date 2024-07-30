import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, sessionmaker
from sqlalchemy.orm import sessionmaker
from models.user_model import Base
from schemas.user_schemas import UserCreateModel, UserUpdateModel
from services.user_command_service import UserCommandService

DATABASE_URL = "postgresql+asyncpg://postgres:password@write-db:5432/command_db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()
user_command_service = UserCommandService()

@app.lifespan("startup")
async def startup_event():
    await user_command_service.connect_rabbitmq()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.lifespan("shutdown")
async def shutdown_event():
    await user_command_service.close_rabbitmq()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.post("/users/")
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    return await user_command_service.create_user(user_data, session)

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdateModel, session: AsyncSession = Depends(get_session)):
    return await user_command_service.update_user(user_id, user_data, session)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await user_command_service.delete_user(user_id, session)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
