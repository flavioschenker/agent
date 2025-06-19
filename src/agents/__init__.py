from src.agents.agent import Agent
from src.agents.aggregation import AggregationAgent
from src.agents.time import TimeIntelligenceAgent

def get_agent(name:str) -> Agent:
    if name == "AggregationAgent":
        return AggregationAgent()
    
    elif name == "TimeIntelligenceAgent":
        return TimeIntelligenceAgent()
    
    else:
        raise ValueError(f"Agent {name} is not supported or implemented. Try to call another Agent. Supported are: 'TimeIntelligenceAgent', 'AggregationAgent'.")