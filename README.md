# AIModeratedChat - Backend

This repository contains the backend code for the AIModeratedChat. This application is designed to facilitate communication between users by providing a chat platform monitored by an AI moderator. The AI, powered by OpenAI's GPT-3, intervenes when necessary to improve the conversation.

---

### Technologies Used

- Django
- autopep8
- OpenAI API

---

### Getting Started

#### Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python and Django
- You have a `OPENAI_API_KEY`, `GPT_PROMPT`, and `MODEL_ID` to be included in your .env file

The `GPT_PROMPT` is the instruction given to the AI therapist. For example, it could be: "You are a couples therapist. Intervene and directly address the chat participants only when there is a significant communication problem where advice or support would be beneficial. In everyday conversations or when no advice is needed, respond with 'undefined'."

#### Installation and Setup

1. Clone the repository

```bash
git clone https://github.com/Max-Montag/AIModeratedChat-backend.git
```

2. Install Python packages

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and include your environment variables:

```bash
OPENAI_API_KEY=<your-openai-api-key>
GPT_PROMPT=<your-gpt-prompt>
MODEL_ID=<your-model-id>
```

4. Run the Django server:

```bash
python manage.py runserver
```

---

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

### Acknowledgements

- [OpenAI](https://openai.com/)
- [Django](https://www.djangoproject.com/)
- [autopep8](https://pypi.org/project/autopep8/)
