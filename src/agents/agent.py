class Agent():
    def __init__(
        self,
        system_prompt:str
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