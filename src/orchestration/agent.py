import json
from src.utils import load_text_file, load_json_file, api_request

def make_plan() -> list:
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
    response = api_request(
        messages=messages,
        guided_json=json_schema
    )
    message = response["choices"][0]["message"]
    content = message["content"]
    json_plan = json.loads(content)
    graph = json_plan["plan"]
    return graph

def revalidate_plan(orchestration_history):
    system_prompt = load_text_file("src/orchestration/prompt_revalidate.md")
    user_prompt = load_text_file("src/orchestration/prompt_user.md")
    json_schema = load_json_file("src/orchestration/schema_planning.json")
