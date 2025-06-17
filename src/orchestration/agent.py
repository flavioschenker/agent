from src.client import sync_request
from src.utils import load_text_file, load_json_file

def make_plan():
    system_prompt = load_text_file("src/orchestration/prompt_planning.md")
    user_prompt = load_text_file("src/orchestration/prompt_user.md")
    json_schema = load_json_file("src/orchestration/schema_planning.json")
    
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
        guided_json=json_schema
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
   

def revalidate_plan(orchestration_history):
    system_prompt = load_text_file("src/orchestration/prompt_revalidate.md")
    user_prompt = load_text_file("src/orchestration/prompt_user.md")
    json_schema = load_json_file("src/orchestration/schema_planning.json")
