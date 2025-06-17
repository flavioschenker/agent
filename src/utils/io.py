import json

def load_text_file(path:str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            return content
    
    except FileNotFoundError:
        print(f"Error: The file at '{path}' was not found.")
        return ""
    
def load_json_file(path:str) -> dict | list:
    try:
        with open(path, "r", encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: The file at '{path}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file.")
        return {}
  