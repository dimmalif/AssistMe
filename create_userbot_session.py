from pyrogram import Client
#  tg- 2fr
api_id = 28983662
api_hash = 'a3814b767d9bfe2b87cb5e9aca76c33b'

app = Client('operator', api_id, api_hash)
app.start()
app.stop()
