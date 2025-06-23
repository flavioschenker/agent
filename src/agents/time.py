from src.agents.agent import Agent
from src.utils import load_text_file

class TimeIntelligenceAgent(Agent):
    def __init__(self):
        system_prompt = load_text_file("src/agents/system_prompt_time.md")
        super().__init__(system_prompt)
        self.json_schema = {
            "type": "object",
            "description": "A list of column names.",
            "properties": {
                "column_names": {
                    "type": "array",
                    "description": "A list of the selected column names.",
                    "items": {
                        "type": "string",
                        "description": "a single column name"
                    }
                }
            }
        }

    def __call__(
        self,
        node_id:str,
        progress:list,
        task:str,
        schema:str,
        input_references:list
    ) -> str:        

        print("TimeIntelligenceAgent is called an has received the following task:")
        print(task)

        user_prompt = f"""**TASK:** {task}

**COLUMN_LIST:** {schema}"""
        self.think(
            user_prompt,
            self.json_schema
        )

        agent_result = f"Generated a new Data Reference called 'Grouped'"
        return agent_result