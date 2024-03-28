import requests
from dotenv import load_dotenv
import os

load_dotenv()

def invoke(query: dict):
    url = 'https://app.tryhelix.ai/api/v1/sessions/chat'

    headers = {
        'Authorization': f"Bearer {os.getenv('HELIX_API_KEY')}",
        'Content-Type': 'application/json'
    }

    data = {
        "session_id": "4cea2694-bef6-4259-81e1-9a1e1d815b7e",
        "system": "you are an intelligent assistant that has knowledge about the ASME "
                  "B31.3 piping code"
                  f"Context: {query['context']}",
        "messages": [
            {
                "role": "user",
                "content": {
                    "content_type": "text",
                    "parts": [query['question']]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
