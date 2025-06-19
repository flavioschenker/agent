import json
from src.orchestration import make_plan
from src.agents import get_agent
from src.utils import load_text_file, load_json_file

table_schema = load_text_file("src/orchestration/dummy_schema.md")
#graph = make_plan()
graph = load_json_file("src/orchestration/dummy_plan.json")

print(json.dumps(graph, indent=4))

traversed = set()
progress = {}
# Orchestration loop, Graph traversal

for node in graph:
    id = node["node_id"]
    agent_name = node["agent"]
    task = node["task"]
    dependencies = node["dependencies"]
    input_references = node["input_data"]

    meets_dependencies = True
    for traversed_id in dependencies:
        if traversed_id not in traversed:
            meets_dependencies = False
            break
    
    if not meets_dependencies:
        continue

    try:
        agent = get_agent(agent_name)
    except ValueError as e:
        progress[id] = {
            "status": "failure",
            "result": str(e)
        }
        continue

    agent_result = agent(
        node_id=id,
        progress=progress,
        task=task,
        schema=table_schema,
        input_references=input_references
    )
    traversed.add(id)
    progress[id] = {
        "status": "successful",
        "result": agent_result
    }

print(json.dumps(progress, indent=4))
