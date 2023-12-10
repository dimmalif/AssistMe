# This telegram bot was created to distribute users between operators, etc. staff


## User functionality
When a user initiates a dialogue, he is asked to send his contact using a button and thus register.
After this, the user will either immediately receive a link to a chat with an operator (in a button), or will need to wait until someone is free.

## Operator functionality
Ability to start or end a work shift.
The operator will then be automatically invited to chat with the user as soon as the user requests a chat if they have less than six active chats.
If all operators have more than 6 active chats, then a message will be sent to everyone that such and such a person is in the queue.
At the end of the dialogue, you need to close the active chat through the bot.
You can independently activate a chat from the queue, view the status of the queue and see active chats now.

### Listen to chats
Message logging is implemented here. A folder with the user ID is created, into which a txt file with correspondence and additional files are placed
Logged: messages, modified messages, photos, emoji, voice messages

### A little more about the mechanics of work
This project uses the aiogram bot as the main user interface and the pyrogram bot account - a real telegram account managed by a bot.
Operators are added to the database manually. The most available operators are selected for the user, based on the number of active chats.
The operator must write at least once to the bot. The same goes for the bot account, plus add the bot account to your contacts.
An operator is added to the chat only when the user has created a chat and joined it.
If the user created a chat and did not go to it, then he will not be able to create another chat, only go to the created one. The bot account itself does not delete chats.
If the user created a chat a long time ago and wants to enter it, then the operator selected for it may be busy, in which case you need to restart the bot.

### Database tables
There are two tables:

     Lead - user table with fields:
         user_id
         username
         tag (@...)
         phone_number (+380..)
         operator_tag (which operator is consulting)
         waiting_status (can be: None - the person did not initialize the chat; waiting - if there were no available operators and the user was queued
                         create_chat - if the chat has been created; accepted - if the user created and went to the chat, finalize - if the chat is completed (only in this case the user will be able to completely re-create the chat))
         active_chat_link - link to the chat that the user initiated

     Operator - table of operators with fields:
         user_id
         username
         tag
         active_chat_links (list of all active chats, format 'x1, x2, ...')
         is_active (whether the operator has started working. Can be inactive, active)

### What can be added/corrected
1. Chats that the user initialized and did not delete - need to be deleted and the waiting_status changed (using APScheduler).
2. Regular automatic notification of operators about the status of the queue (using APScheduler).
3. You can make sure that as soon as a free operator appears, a chat is automatically created (using APScheduler).
4. You can use the aiogram bot which is in the chat for some additional user interface (Feedback, interaction with chat, etc.)
5. After the chat is completed, you can archive the correspondence, and possibly send it somewhere

## Main project tools
* Aiogram
* Pyrogram
* PostgreSQL + SQLAlchemy
* docker
