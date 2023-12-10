from sqlalchemy import Column

from app.database.services.db_ctx import BaseRepo, ExpressionType, SQLAlchemyModel
from app.database.models import *


class OperatorRepo(BaseRepo[Operator]):
    model = Operator

    async def get_user(self, user_id: int) -> Operator:
        return await self.get_one(self.model.user_id == user_id)

    async def update_user(self, user_id: int, **kwargs) -> None:
        return await self.update(self.model.user_id == user_id, **kwargs)

    async def delete_user(self, user_id: int) -> list[Operator]:
        return await self.delete(self.model.user_id == user_id)

    async def get_all_operator(self):
        return await self.get_all()


class LeadRepo(BaseRepo[Lead]):
    model = Lead

    async def get_user(self, user_id: int) -> Lead:
        return await self.get_one(self.model.user_id == user_id)

    async def get_chat_id(self, link: str) -> int | None:
        current_user = await self.get_one(self.model.active_chat_link == link)
        if current_user:
            return current_user.active_chat_id
        else:
            return None

    async def get_waiting_user(self) -> list[Lead] | None:
        return await self.get_all(self.model.waiting_status == 'waiting')

    async def update_waiting_status(self, link: str, waiting_status: str) -> None:
        return await self.update(self.model.active_chat_link == link, waiting_status=waiting_status)

    async def update_user(self, user_id: int, **kwargs) -> None:
        return await self.update(self.model.user_id == user_id, **kwargs)

    async def delete_user(self, user_id: int) -> list[Lead]:
        return await self.delete(self.model.user_id == user_id)
