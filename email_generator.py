from groq import Groq
from prompt import create_email_prompt


MODEL_NAME = "openai/gpt-oss-120b"


def generate_email(
    api_key,
    recipient,
    purpose,
    topic,
    key_points,
    tone,
    length
):
    if not api_key:
        raise ValueError("Groq API key is missing.")

    client = Groq(api_key=api_key)

    prompt = create_email_prompt(
        recipient=recipient,
        purpose=purpose,
        topic=topic,
        key_points=key_points,
        tone=tone,
        length=length
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert professional email writing "
                    "assistant. Generate natural, clear, accurate, "
                    "and context-appropriate emails."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=800
    )

    generated_email = response.choices[0].message.content

    return generated_email.strip()
