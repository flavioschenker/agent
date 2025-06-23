import os
import requests
import dotenv
dotenv.load_dotenv()

def api_request(messages, guided_json=None, tools=None):
    url = os.getenv("API_URL")
    endpoint = os.getenv("API_ENDPOINT")
    headers = {
        "Content-Type": "application/json",
        "Api-key": os.getenv("API_KEY"),
    }
    payload = {
        "model": os.getenv("MODEL"),
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 2048,
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
            json=payload,
            verify=False,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM: {e.response.text}")
        return None