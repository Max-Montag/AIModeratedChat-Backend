import os
import openai
from dotenv import load_dotenv
from .models import Message

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
              "role": "system",
                "content": "Du bist ein Paartherapeut.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    return response['choices'][0]['message']['content']


def create_bot_message(original_message):
    bot_message_text = get_ai_response(original_message.text)
    bot_message = Message.objects.create(
        chatroom=original_message.chatroom,
        text=bot_message_text,
        author=None
    )
