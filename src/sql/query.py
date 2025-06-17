from src.client import sync_request
from src.utils import load_text_file, load_json_file

def execute_query():
    system_prompt = load_text_file("src/sql/prompt_system.md")
    user_prompt = load_text_file("src/sql/prompt_user.md")
    tools = load_json_file("src/sql/tool_definition.json")
    
    messages = [
        {
            "role":"system",
            "content": system_prompt
        },
        {
            "role":"user",
            "content": user_prompt
        }
    ]

    response = sync_request(
        messages=messages,
        tools=tools
    )
    message = response["choices"][0]["message"]
    role = message["role"]
    reasoning = message["reasoning_content"]
    content = message["content"]
    tool_calls = message["tool_calls"]

    print("Reasoning:")
    print(reasoning)
    print("Content:")
    print(content)    