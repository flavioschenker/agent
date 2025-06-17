import requests
import json

API_BASE_URL = "http://localhost:8000/v1"
MODEL_NAME = "Qwen/Qwen3-0.6B"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location. Use Fahrenheit for US cities and Celsius for others.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA or London, UK",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature to use. Infer from location if possible. Defaults to Celsius for non-US locations and Fahrenheit for US locations.",
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time for a specified timezone or location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The timezone to get the time for (e.g., 'America/New_York', 'Europe/London'). If not provided, infer from location.",
                    },
                    "location": {
                        "type": "string",
                        "description": "An optional location to infer timezone from, e.g., 'Paris, France'.",
                    }
                },
                "required": [], # No required parameters, can infer from context
            },
        },
    },
]

# --- Function to interact with the LLM API ---
def call_llm_with_tools(messages, tools=None, tool_choice="auto"):
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.0, # Make it deterministic for tool calling
        "max_tokens": 512,  # Adjust as needed
        "tools": tools,
        "tool_choice": tool_choice # "auto", "none", or specific function call
    }

    try:
        response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM: {e.response.text}")
        return None

# --- Main Tool Calling Logic (Simplified) ---

def handle_tool_call(tool_call):
    """
    Simulates executing a tool and returns its output.
    In a real application, this would call actual functions.
    """
    function_name = tool_call["function"]["name"]
    arguments = json.loads(tool_call["function"]["arguments"]) # Arguments are always a JSON string

    print(f"\n--- Model requested tool: {function_name} with arguments: {arguments} ---")

    if function_name == "get_current_weather":
        location = arguments.get("location")
        unit = arguments.get("unit", "celsius") # Default to celsius if not provided by model

        # Simulate API call
        if "london" in location.lower():
            return f"The current weather in {location} is 15 degrees {unit} and partly cloudy."
        elif "uzwil" in location.lower():
            return f"The current weather in {location} is 18 degrees {unit} and sunny."
        elif "boston" in location.lower():
             return f"The current weather in {location} is 25 degrees {unit} and humid."
        else:
            return f"Sorry, I cannot get weather for {location}."

    elif function_name == "get_current_time":
        timezone = arguments.get("timezone")
        location = arguments.get("location")
        
        # Simulate current time
        # NOTE: In a real app, use a library like 'pytz' or 'zoneinfo'
        if timezone == "Europe/Zurich" or "uzwil" in location.lower() or "switzerland" in location.lower():
            return "The current time in Uzwil, Switzerland is 1:21 PM CEST (Monday, June 16, 2025)."
        elif timezone == "America/New_York" or "boston" in location.lower():
            return "The current time in Boston, USA is 7:21 AM EDT (Monday, June 16, 2025)."
        else:
            return "Cannot determine time for that location/timezone."
    else:
        return f"Unknown tool: {function_name}"

# --- Conversation Flow ---

conversation_history = [{"role": "system", "content": "JOJOJO"}]

# --- Example 1: User asks for weather, model calls tool ---
print("--- Conversation 1: Weather query ---")
user_query = "What's the weather like in Uzwil right now? Use Celsius."
conversation_history.append({"role": "user", "content": user_query})

response_json = call_llm_with_tools(conversation_history, tools=tools)
print(response_json)

if response_json:
    assistant_reply = response_json["choices"][0]["message"]
    
    if assistant_reply.get("tool_calls"):
        tool_calls_from_model = assistant_reply["tool_calls"]
        print(f"\nModel's initial reply (tool call): {json.dumps(assistant_reply, indent=2)}")

        # Execute each tool call
        for tool_call in tool_calls_from_model:
            tool_output = handle_tool_call(tool_call)
            
            # Add assistant's tool call and tool's output to history
            conversation_history.append(assistant_reply) # Append the tool_calls message
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call["id"], # Important: link output to the tool call
                "name": tool_call["function"]["name"],
                "content": tool_output
            })
            print(f"--- Tool Output ({tool_call['function']['name']}): {tool_output} ---\n")

        # Ask the model again with the tool output included in the history
        print("--- Sending tool output back to model for final response ---")
        final_response_json = call_llm_with_tools(conversation_history, tools=tools)
        if final_response_json:
            final_assistant_content = final_response_json["choices"][0]["message"]["content"]
            print(f"Final Assistant Response: {final_assistant_content}\n")
            conversation_history.append({"role": "assistant", "content": final_assistant_content})
    else:
        print(f"Assistant Response (no tool call): {assistant_reply['content']}\n")
        conversation_history.append({"role": "assistant", "content": assistant_reply['content']})
else:
    print("Failed to get response for Conversation 1.")

# Reset conversation history for the next example
conversation_history = []

# --- Example 2: User asks for time, model calls tool ---
print("\n--- Conversation 2: Time query ---")
user_query_2 = "What is the current time in Boston?"
conversation_history.append({"role": "user", "content": user_query_2})

response_json_2 = call_llm_with_tools(conversation_history, tools=tools)

if response_json_2:
    assistant_reply_2 = response_json_2["choices"][0]["message"]

    if assistant_reply_2.get("tool_calls"):
        tool_calls_from_model_2 = assistant_reply_2["tool_calls"]
        print(f"\nModel's initial reply (tool call): {json.dumps(assistant_reply_2, indent=2)}")

        for tool_call in tool_calls_from_model_2:
            tool_output_2 = handle_tool_call(tool_call)
            conversation_history.append(assistant_reply_2)
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": tool_call["function"]["name"],
                "content": tool_output_2
            })
            print(f"--- Tool Output ({tool_call['function']['name']}): {tool_output_2} ---\n")

        print("--- Sending tool output back to model for final response ---")
        final_response_json_2 = call_llm_with_tools(conversation_history, tools=tools)
        if final_response_json_2:
            final_assistant_content_2 = final_response_json_2["choices"][0]["message"]["content"]
            print(f"Final Assistant Response: {final_assistant_content_2}\n")
            conversation_history.append({"role": "assistant", "content": final_assistant_content_2})
    else:
        print(f"Assistant Response (no tool call): {assistant_reply_2['content']}\n")
        conversation_history.append({"role": "assistant", "content": assistant_reply_2['content']})
else:
    print("Failed to get response for Conversation 2.")

# --- Example 3: User query that doesn't need a tool ---
print("\n--- Conversation 3: General knowledge ---")
user_query_3 = "Tell me a short joke."
conversation_history = [{"role": "user", "content": user_query_3}] # Reset history for independent query

response_json_3 = call_llm_with_tools(conversation_history, tools=tools) # Still pass tools, model decides
print(response_json)


if response_json_3:
    assistant_reply_3 = response_json_3["choices"][0]["message"]
    if assistant_reply_3.get("tool_calls"):
        print("Unexpected tool call for a joke! (This should not happen)")
    else:
        print(f"Assistant Response (no tool call): {assistant_reply_3['content']}\n")
else:
    print("Failed to get response for Conversation 3.")