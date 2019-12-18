import os, sys, asyncio, array
from flask import Flask, escape, request
from telethon import TelegramClient, functions
from telethon.sessions import MemorySession


loop = asyncio.get_event_loop()
app = Flask(__name__)

tg_api_hash = os.environ['API_HASH']
tg_app_id = os.environ['APP_ID']
messages_limit = 50

if tg_api_hash is None or tg_app_id is None:
    sys.exit()


def json(elems):
    result = '['
    for i, elem in enumerate(elems):
        result += elem.to_json() 
        result += ',' if i < len(elems) - 1 else ']'
    return result

def client(token):
    return TelegramClient(MemorySession(), tg_app_id, tg_api_hash).start(bot_token=token)

async def get_members(token, chat_id):
    c = await client(token)
    users = await c.get_participants(chat_id)
    return json(users)

async def get_messages(token, chat_id, to_message):
    from_message = to_message - messages_limit if to_message > messages_limit else 0
    ids = list(array.array('i',(i for i in range(from_message,to_message))))

    c = await client(token)
    res = await c(functions.channels.GetMessagesRequest(
        channel=chat_id,
        id=ids
    ))

    return json(res.messages)

@app.route('/messages')
def messages():
    token = request.args.get("token")
    chat = int(request.args.get("chat"))
    offset = int(request.args.get("to")) 
    return loop.run_until_complete(get_messages(token, chat, offset))

@app.route('/members')
def members():
    token = request.args.get("token")
    chat = int(request.args.get("chat"))

    return loop.run_until_complete(get_members(token, chat))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432)
