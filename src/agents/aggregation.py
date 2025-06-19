from src.agents.agent import Agent

class AggregationAgent(Agent):
    def __init__(self):
        system_prompt = """
        You are a sophisticated table aggregation agent.
        You can group and aggregate 
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

        print("AggregationAgent is called an has received the following task:")
        print(task)

        print("doing agents things...")

        agent_result = f"Step {node_id} successfully executed. Generated a new Data Reference called 'Grouped'"
        return agent_result