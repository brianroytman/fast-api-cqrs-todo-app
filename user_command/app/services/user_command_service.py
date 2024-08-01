import json
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schemas import UserCreateModel, UserUpdateModel
from models.user_model import User
from repositories.user_repository import UserRepository
from services.rabbitmq_service import RabbitMQService

class UserCommandService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.rabbitmq_service = RabbitMQService()

    async def connect_rabbitmq(self):
        await self.rabbitmq_service.connect()

    async def close_rabbitmq(self):
        await self.rabbitmq_service.close_connection()

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        user = await self.user_repository.add(session, new_user)
        await self.rabbitmq_service.publish_message('user_events', json.dumps({'type': 'UserCreated', 'data': user.to_dict()}))
        return user

    async def update_user(self, user_id: int, user_data: UserUpdateModel, session: AsyncSession) -> User:
        updated_user = await self.user_repository.update(session, user_id, user_data.model_dump())
        await self.rabbitmq_service.publish_message('user_events', json.dumps({'type': 'UserUpdated', 'data': updated_user.to_dict()}))
        return updated_user

    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        await self.user_repository.delete(session, user_id)
        await self.rabbitmq_service.publish_message('user_events', json.dumps({'type': 'UserDeleted', 'data': {'id': user_id}}))
