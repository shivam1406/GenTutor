import os
import requests

def summarize_text(text: str) -> str:
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        print("🔑 OpenRouter Key in function:", api_key)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/shivam1406/GenTutor",
            "X-Title": "GenTutor"
        }

        payload = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [
                {"role": "system", "content": "You're a helpful tutor. Summarize this educational content."},
                {"role": "user", "content": text}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error from OpenRouter: {str(e)}"