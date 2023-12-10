from app.states.base import *


class ChatRepo(StatesGroup):
    StartDelChat = State()
    StartInitChat = State()
