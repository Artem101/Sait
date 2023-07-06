import markdown
import openai
from sqlalchemy.orm import sessionmaker

from Mydatabase.customization import engine
from Mydatabase.db_user import ChatGtp
from config import OPENAI_API_KEY


def textprocessing(content):
    context = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
    return context
session_factory = sessionmaker(bind=engine)
openai.api_key = OPENAI_API_KEY
model_engine = "gpt-3.5-turbo"
def chatgtp(text, user_id):
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[{"role": "system", "content": str(text)}]
    )

    output_text = response['choices'][0]['message']['content']
    with session_factory() as session:
        new_message_chat_gtp = ChatGtp(user_id=user_id, message_text=str(output_text), query=str(text))
        session.add(new_message_chat_gtp)
        session.commit()
    return output_text