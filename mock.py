import pandas as pd
import numpy as np
import io
import sys
from typing import List, Dict, Any, Callable

# --- 1. SETUP: CREATE A LARGE SAMPLE DATAFRAME ---
# This simulates the real-world scenario where the DataFrame is too large
# to be passed directly to the LLM.

def create_large_dataframe(num_rows=1_000_000):
    """Generates a sample large DataFrame for demonstration."""
    print(f"Creating a sample DataFrame with {num_rows:,} rows...")
    data = {
        'transaction_id': [f'txn_{i}' for i in range(num_rows)],
        'timestamp': pd.to_datetime(pd.date_range(start='2023-01-01', periods=num_rows, freq='T')),
        'customer_id': np.random.randint(1000, 2000, size=num_rows),
        'product_category': np.random.choice(['electronics', 'clothing', 'groceries', 'home_goods', 'toys'], size=num_rows),
        'amount': np.random.uniform(5.0, 500.0, size=num_rows).round(2),
        'is_fraud': np.random.choice([0, 1], size=num_rows, p=[0.99, 0.01]) # 1% fraud rate
    }
    df = pd.DataFrame(data)
    # Introduce some missing values to make it more realistic
    df.loc[df.sample(frac=0.05).index, 'amount'] = np.nan
    print("Sample DataFrame created.")
    return df

# --- 2. TOOL DEFINITIONS ---
# These are the functions the LLM agent can choose to call.
# Each tool operates on the DataFrame and returns a string summary of its result.
# The LLM never receives the DataFrame object itself, only the string outputs.

def get_dataframe_info(df: pd.DataFrame) -> str:
    """
    Returns the output of df.info() as a string.
    Provides a high-level overview of the DataFrame, including columns, data types, and memory usage.
    """
    print("AGENT ACTION: Calling get_dataframe_info")
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

def get_dataframe_head(df: pd.DataFrame, n: int = 5) -> str:
    """
    Returns the first n rows of the DataFrame as a string.
    Lets the agent inspect the actual data and schema.
    """
    print(f"AGENT ACTION: Calling get_dataframe_head with n={n}")
    return df.head(n).to_string()

def get_column_summary(df: pd.DataFrame, column_name: str) -> str:
    """
    Provides a descriptive summary of a single column.
    For numerical columns, it returns df[column].describe().
    For categorical columns, it returns value_counts().
    """
    print(f"AGENT ACTION: Calling get_column_summary for column '{column_name}'")
    if column_name not in df.columns:
        return f"Error: Column '{column_name}' not found in the DataFrame."
    
    col = df[column_name]
    if pd.api.types.is_numeric_dtype(col):
        summary = f"--- Summary for numerical column '{column_name}' ---\n"
        summary += col.describe().to_string()
    else:
        summary = f"--- Summary for categorical column '{column_name}' ---\n"
        # Only show top 10 value counts for brevity
        summary += col.value_counts().head(10).to_string()
        if len(col.unique()) > 10:
            summary += f"\n... and {len(col.unique()) - 10} more unique values."
            
    # Check for missing values
    missing_count = col.isnull().sum()
    if missing_count > 0:
        summary += f"\n\nMissing Values: {missing_count} ({missing_count / len(df):.2%})"
        
    return summary

def execute_python_code(df: pd.DataFrame, code: str) -> Dict[str, Any]:
    """
    Executes a snippet of Python code on the DataFrame.
    This is the most powerful and flexible tool. The code snippet can perform
    filtering, aggregation, feature engineering, etc.

    SECURITY WARNING: In a real system, this function is extremely dangerous
    as it allows arbitrary code execution. It should be run in a sandboxed
    environment to prevent malicious actions.

    The function returns the modified DataFrame and any print outputs.
    """
    print(f"AGENT ACTION: Calling execute_python_code with code:\n---\n{code}\n---")
    local_vars = {'df': df.copy()} # Use a copy to avoid modifying the original state accidentally
    
    # Capture print outputs from the executed code
    buffer = io.StringIO()
    sys.stdout = buffer
    
    try:
        exec(code, {'pd': pd, 'np': np}, local_vars)
        output = buffer.getvalue()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        # The modified DataFrame is now in local_vars['df']
        modified_df = local_vars.get('df', df)
        
        result_summary = "Code executed successfully."
        if output:
            result_summary += f"\nCaptured output:\n{output}"
        else:
            result_summary += "\nNo output was printed."
            
        # Provide a summary of what changed
        if len(df) != len(modified_df):
            result_summary += f"\nRow count changed from {len(df)} to {len(modified_df)}."
        changed_cols = df.columns.symmetric_difference(modified_df.columns)
        if not changed_cols.empty:
            result_summary += f"\nColumns changed: {list(changed_cols)}"

        return {"result_summary": result_summary, "new_df": modified_df}

    except Exception as e:
        sys.stdout = sys.__stdout__
        return {"error": f"Error executing code: {e}"}

def answer_question(answer: str) -> str:
    """
    A final tool for the agent to call when it has analyzed the data
    and is ready to provide the final answer to the user's query.
    This signals the end of the workflow.
    """
    print(f"AGENT ACTION: Calling answer_question with answer: {answer}")
    return answer

# --- 3. ORCHESTRATION & STATE MANAGEMENT ---

class AgenticWorkflow:
    """Manages the state and orchestrates the agent's interaction with the tools."""

    def __init__(self, df: pd.DataFrame, query: str, max_iterations: int = 10):
        self.df = df
        self.query = query
        self.max_iterations = max_iterations
        self.scratchpad = [] # Stores the history of (action, observation) tuples
        self.tools = {
            "get_dataframe_info": get_dataframe_info,
            "get_dataframe_head": get_dataframe_head,
            "get_column_summary": get_column_summary,
            "execute_python_code": execute_python_code,
            "answer_question": answer_question,
        }

    def _get_full_prompt(self) -> str:
        """Constructs the prompt for the LLM based on the current state."""
        tool_descriptions = "\n".join([f"- `{name}`: {func.__doc__.strip()}" for name, func in self.tools.items()])
        
        prompt = f"""You are a world-class data analyst agent. Your goal is to answer the following user query:
'{self.query}'

You have access to a large pandas DataFrame that you cannot see directly. To analyze it, you can use the following tools:
{tool_descriptions}

Your thought process should be a series of tool calls. For each step, think about what you need to know and choose the best tool.

You must respond with a single tool call in JSON format, like this:
{{"tool_name": "name_of_tool", "args": {{"arg1": "value1", "arg2": "value2"}}}}

History of your previous actions and their results (scratchpad):
{self.scratchpad if self.scratchpad else 'No actions taken yet.'}

Based on the history, what is the next logical step to answer the query? Provide the single next tool call in the specified JSON format.
"""
        return prompt

    def _mock_llm_call(self, prompt: str) -> Dict[str, Any]:
        """
        MOCKS a call to an LLM. In a real system, this would be an API call
        to a model like Gemini. Here, we simulate the LLM's reasoning process
        based on the scratchpad content to demonstrate the workflow.
        """
        print("\n" + "="*50)
        print("AGENT PROMPT (What the LLM would see)")
        print("="*50)
        print(prompt)
        print("="*50 + "\n")

        # --- Simulated Reasoning Logic ---
        if not self.scratchpad:
            # First step is always to get an overview.
            return {"tool_name": "get_dataframe_info", "args": {}}
        
        last_action, last_observation = self.scratchpad[-1]
        
        if last_action.get("tool_name") == "get_dataframe_info":
            # After getting info, look at the first few rows.
            return {"tool_name": "get_dataframe_head", "args": {"n": 5}}

        if "highest transaction amount" in self.query.lower():
            if "summary for numerical column 'amount'" not in str(last_observation):
                 # We need to analyze the 'amount' column.
                 return {"tool_name": "get_column_summary", "args": {"column_name": "amount"}}
            else:
                 # We have the summary. Now find the actual row.
                 code = "print(df.loc[df['amount'].idxmax()].to_string())"
                 return {"tool_name": "execute_python_code", "args": {"code": code}}
        
        if last_action.get("tool_name") == "execute_python_code" and "idxmax" in last_action['args']['code']:
            # The last action found the row, now we can answer.
            answer = f"The transaction with the highest amount is:\n{last_observation['result_summary']}"
            return {"tool_name": "answer_question", "args": {"answer": answer}}
        
        # Default fallback if no other logic matches
        return {"tool_name": "answer_question", "args": {"answer": "Agent could not determine the next step."}}

    def run(self) -> str:
        """Executes the agentic workflow loop."""
        for i in range(self.max_iterations):
            print(f"\n--- ITERATION {i+1} ---")
            
            # 1. Generate the prompt for the LLM
            prompt = self._get_full_prompt()
            
            # 2. Get the next action from the (mocked) LLM
            action = self._mock_llm_call(prompt)
            print(f"LLM decided action: {action}")
            
            # 3. Execute the chosen tool
            tool_name = action.get("tool_name")
            tool_args = action.get("args", {})
            
            if tool_name not in self.tools:
                observation = f"Error: Tool '{tool_name}' not found."
            else:
                try:
                    tool_func = self.tools[tool_name]
                    # The main dataframe is passed implicitly to tools that need it
                    if tool_name in ["get_dataframe_info", "get_dataframe_head", "get_column_summary", "execute_python_code"]:
                        observation = tool_func(self.df, **tool_args)
                    else:
                        observation = tool_func(**tool_args)

                    # If exec_code modified the df, update our state
                    if tool_name == "execute_python_code" and "new_df" in observation:
                        self.df = observation["new_df"]

                except Exception as e:
                    observation = f"Error during tool execution: {e}"

            # 4. Check for termination condition
            if tool_name == "answer_question":
                print("\nWorkflow finished.")
                return observation # The final answer
                
            # 5. Update scratchpad and continue loop
            self.scratchpad.append((action, observation))
            print(f"Action result/observation added to scratchpad.")

        return "Agent stopped after reaching max iterations."

# --- 4. MAIN EXECUTION ---

if __name__ == "__main__":
    # 1. Load the data
    df_large = create_large_dataframe(num_rows=500_000)
    
    # 2. Define the user query
    user_query = "Which transaction had the highest transaction amount, and what are its details?"
    
    # 3. Initialize and run the agentic workflow
    workflow = AgenticWorkflow(df=df_large, query=user_query)
    final_answer = workflow.run()
    
    # 4. Print the final result
    print("\n" + "#"*30)
    print("      FINAL AGENT ANSWER")
    print("#"*30)
    print(final_answer)

