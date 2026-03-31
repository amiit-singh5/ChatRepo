from openai import OpenAI
from config.config import OPENROUTER_API_KEY, BASE_URL, MODEL

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL
)

def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
