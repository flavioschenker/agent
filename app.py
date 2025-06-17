from src.orchestration import make_plan
from src.sql import execute_query
#from src.agents import get_agent

initial_plan = execute_query()

for step in initial_plan:
    agent_name = step["agent"]
    task = step["task"]

    #agent = get_agent(agent_name)