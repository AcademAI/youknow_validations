from langchain.chat_models import GigaChat
import os
from dotenv import load_dotenv

load_dotenv()


GIGACHAT_CLIENT_SECRET = os.getenv('GIGACHAT_CLIENT_SECRET')
GIGACHAT_CREDENTIALS = os.getenv('GIGACHAT_CREDENTIALS')
KANDINSKY_API_KEY = os.getenv('KANDINSKY_API_KEY')
KADNINSKY_SECRET_KEY = os.getenv('KADNINSKY_SECRET_KEY')

"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

while(True):
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    print("Bot: ", res.content)