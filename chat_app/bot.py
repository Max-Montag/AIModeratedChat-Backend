import os
import openai
from dotenv import load_dotenv
from .models import ChatRoom, Message
from django.contrib.auth.models import User

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_ai_response(prompt):
    print("PROMPT:")
    print(prompt)
    response = openai.ChatCompletion.create(
        model=os.getenv('MODEL_ID'),
        messages=[
            {"role": "system", "content": os.getenv('GPT_PROMPT')},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1
    )
    print("RESPONSE:")
    print(response)
    return response['choices'][0]['message']['content']


def create_bot_message(chatroom_id):
    chatroom = ChatRoom.objects.get(id=chatroom_id)
    last_messages_user1 = Message.objects.filter(
        chatroom=chatroom, author=chatroom.participant1, processed_by_ai=False).order_by('-timestamp')
    last_messages_user2 = Message.objects.filter(
        chatroom=chatroom, author=chatroom.participant2, processed_by_ai=False).order_by('-timestamp')

    text_user1 = ' '.join([msg.text for msg in last_messages_user1])
    text_user2 = ' '.join([msg.text for msg in last_messages_user2])

    prompt = f"{chatroom.participant1.username}: {text_user1} {chatroom.participant2.username}: {text_user2}"

    bot_message_text = get_ai_response(prompt)

    bot_message_text_stripped = bot_message_text.strip().strip('.')

    # Only create a bot message if the response is not undefined (i.e. intervention is not required)
    if bot_message_text_stripped.lower().find("undefined") == -1:
        bot_message = Message.objects.create(
            chatroom=chatroom,
            text=bot_message_text,
            author=User.objects.get(id=5)
        )

    last_messages_user1.update(processed_by_ai=True)
    last_messages_user2.update(processed_by_ai=True)
