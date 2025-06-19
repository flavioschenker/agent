from src.agents.agent import Agent

class TimeIntelligenceAgent(Agent):
    def __init__(self):
        system_prompt = """
        You are a sophisticated time filter agent.
        You can identify time data and extract the right time columns from a dataset.
        """
        super().__init__(system_prompt)
        self.json_schema = {

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

        print("doing agents things...")

        agent_result = f"Step {node_id} successfully executed. Generated a new Data Reference called 'Grouped'"
        return agent_result