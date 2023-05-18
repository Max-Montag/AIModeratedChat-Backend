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
    all_messages = Message.objects.filter(
        chatroom=chatroom, processed_by_ai=False).order_by('timestamp')

    if not all_messages.filter(author=chatroom.participant1).exists() or not all_messages.filter(author=chatroom.participant2).exists():
        return

    combined_phrases = []
    previous_author = None
    current_phrase = ""

    for message in all_messages:
        if message.author == previous_author:
            current_phrase += " " + message.text
        else:
            if current_phrase:
                combined_phrases.append(current_phrase)
            current_phrase = f"{message.author.username}: {message.text}"

        previous_author = message.author
        message.processed_by_ai = True
        message.save()

    if current_phrase:
        combined_phrases.append(current_phrase)

    if combined_phrases:
        prompt = ' '.join(combined_phrases)

        bot_message_text = get_ai_response(prompt)
        bot_message_text_stripped = bot_message_text.strip().strip('.')

        # Only create a bot message if the response is not undefined (i.e. intervention is not required)
        if bot_message_text_stripped.lower().find("undefined") == -1:
            bot_message = Message.objects.create(
                chatroom=chatroom,
                text=bot_message_text,
                author=User.objects.get(username='Therapist'),
                processed_by_ai=True
            )
