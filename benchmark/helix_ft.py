import requests
import os

conversation_history = []

def invoke(query: dict):
    url = 'https://app.tryhelix.ai/api/v1/sessions/chat'

    conversation_history.append(query['question'])
    if len(conversation_history) > 5:
        conversation_history.pop(0)
    print(f"===> Helix: {conversation_history}")

    headers = {
        'Authorization': f"Bearer {os.getenv('HELIX_API_KEY')}",
        'Content-Type': 'application/json'
    }
    history = "\n".join(conversation_history)

    data = {
        "session_id": "4cea2694-bef6-4259-81e1-9a1e1d815b7e",
        "system": "You are an intelligent assistant that has knowledge about the ASME "
                  "B31.3 piping code."
                  "Only answer questions related to the ASME code. "
                  f"CONVERSATION HISTORY: {history}"
                  f"RELEVANT CONTEXT: {query['context']}",
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
