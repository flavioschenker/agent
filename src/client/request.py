import os
import requests
import dotenv
dotenv.load_dotenv()

def sync_request(messages, guided_json=None, tools=None):
    url = os.getenv("API_URL")
    endpoint = os.getenv("API_ENDPOINT")
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": os.getenv("MODEL"),
        "messages": messages,
        "temperature": 0.0, # Make it deterministic for tool calling
        "max_tokens": 2048,  # Adjust as needed
    }
    if guided_json:
        payload["guided_json"] = guided_json
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto" # "none","required"

    try:
        response = requests.post(
            f"{url}/{endpoint}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM: {e.response.text}")
        return None