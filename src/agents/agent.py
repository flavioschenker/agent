from src.utils import api_request

class Agent():
    def __init__(
        self,
        system_prompt:str,
    ) -> None:
        self.system_prompt = system_prompt

    def __call__(
        self,
        node_id:str,
        progress:list,
        task:str,
        schema:str,
        input_references:list
    ) -> str:
        raise NotImplementedError("Call method needs to be implemented!")
    
    def think(
        self,
        user_prompt:str,
        json_schema:dict=None
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        print(json_schema)
        response = api_request(
            messages=messages,
            guided_json=json_schema
        )
        print(response)
        message = response["choices"][0]["message"]
        content = message["content"]
        #print(content)