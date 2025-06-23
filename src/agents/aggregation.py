from src.agents.agent import Agent

class AggregationAgent(Agent):
    def __init__(self):
        system_prompt = """
        You are a sophisticated table aggregation agent.
        You can group and aggregate 
        """
        super().__init__(system_prompt)
        self.json_schema = {
            "title": "Column identification",
            "description": "A list of subtask objects identifiying the right columns according to the task given.",
            "type": "array",
            "items": {
                "type": "object",
                "title": "subtask",
                "description": "a single subtask",
                "required": [
                    "columns",
                    "subtask_description",
                    "output_reference"
                ],
                "properties": {
                    "columns": {
                        "type": "array",
                        "description": "List of column names. Can contain one or more column names.",
                        "items": {
                            "type": "string",
                            "description": "a single column name"
                        }
                    },
                    "subtask_description": {
                        "type": "string",
                        "description": "Describe the subtask you identified and solved."
                    },
                    "output_reference": {
                        "type": "string",
                        "description": "The output reference where the filtered DataFrame is stored."
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

        print("AggregationAgent is called an has received the following task:")
        print(task)

        print("doing agents things...")

        agent_result = f"Step {node_id} successfully executed. Generated a new Data Reference called 'Grouped'"
        return agent_result