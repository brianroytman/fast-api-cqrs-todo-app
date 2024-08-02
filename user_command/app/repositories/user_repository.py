from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User

class UserRepository:
    async def add(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User:
        result = await session.execute(select(User).filter_by(id=user_id))
        return result.scalars().first()

    async def update(self, session: AsyncSession, user_id: int, user_data: dict) -> User:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        for key, value in user_data.items():
            setattr(user, key, value)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete(self, session: AsyncSession, user_id: int) -> None:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        await session.delete(user)
        await session.commit()
