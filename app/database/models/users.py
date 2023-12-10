import sqlalchemy as sa
from app.database.models.base import TimedBaseModel


class Operator(TimedBaseModel):
    user_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=False, index=True)
    username = sa.Column(sa.VARCHAR(255), nullable=False)
    tag = sa.Column(sa.VARCHAR(30), nullable=True)
    active_chat_links = sa.Column(sa.VARCHAR, nullable=True)
    is_active = sa.Column(sa.VARCHAR, nullable=False, default='inactive')


class Lead(TimedBaseModel):
    user_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=False, index=True)
    username = sa.Column(sa.VARCHAR(255), nullable=False)
    tag = sa.Column(sa.VARCHAR(30), nullable=True)
    phone_number = sa.Column(sa.VARCHAR(30), nullable=False)
    operator_id = sa.Column(sa.BIGINT, nullable=True)
    waiting_status = sa.Column(sa.VARCHAR(30), nullable=True)
    active_chat_link = sa.Column(sa.VARCHAR, nullable=True)
    active_chat_id = sa.Column(sa.BIGINT, nullable=True)
