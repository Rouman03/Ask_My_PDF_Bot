import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_answer(query, docs, chat_history=None):

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    history = ""

    if chat_history:

        for role, message in chat_history[-6:]:

            history += f"{role}: {message}\n"


    prompt = f"""
You are an advanced AI PDF assistant similar to ChatGPT.

Use the provided PDF context to answer intelligently.

Rules:
- Give detailed answers
- Explain clearly
- Use bullet points when useful
- Do not hallucinate
- If answer is unavailable, say so politely

CHAT HISTORY:
{history}

PDF CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    try:

        response = client.chat.completions.create(

            # SAFE WORKING MODEL
            model="openai/gpt-3.5-turbo",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.5,
            max_tokens=1000
        )

        if (
            response
            and response.choices
            and response.choices[0].message
        ):

            answer = response.choices[0].message.content

        else:

            answer = "No response generated."

    except Exception as e:

        answer = f"API Error: {str(e)}"

    return answer, docs