class UserMainMenu:
    start_chat: str = 'Start a chat with an operator'
    send_contact: str = 'Share contact'
    accept_invite: str = 'Join!'


class OperatorStartMenu:
    start_work: str = 'Get started'


class OperatorMainMenu:
    active_chats: str = 'Active chats'
    que_status: str = 'Queue status'
    stop_chat: str = 'End chat'
    finalize_work: str = 'Finish work'
    start_queue_chat: str = 'Start a chat with a user'


class Buttons:
    user_main_menu = UserMainMenu()
    operator_start_menu = OperatorStartMenu()
    operator_main_menu = OperatorMainMenu()
