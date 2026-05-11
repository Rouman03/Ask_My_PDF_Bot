import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_answer(query, docs):

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a professional AI PDF assistant.

Answer ONLY from the provided context.

If the answer is not available in the context, say:
"I could not find that information in the uploaded document."

CONTEXT:
{context}

QUESTION:
{query}
"""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    citations = docs

    return answer, citations