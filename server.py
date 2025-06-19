from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

llm_args = {
    "model": model_name,
    "dtype": "auto",  # Automatically determines the optimal dtype (e.g., float16, bfloat16)
    "gpu_memory_utilization": 0.9, # Fraction of GPU memory to use. Adjust based on your GPU
}

print(f"Loading model: {model_name}...")
llm = LLM(**llm_args)
print("Model loaded successfully.")

tokenizer = AutoTokenizer.from_pretrained(model_name)

sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=512,  # Maximum number of new tokens to generate
    # stop=["<|im_end|>", "<|im_start|>", "im_end", "im_start"] # Qwen specific stop tokens
)

messages1 = [
    {"role": "system", "content": "You are a pandas dataframe agent. You can analye large tabular data with the help of tool calling."},
    {"role": "user", "content": "Write a Python function to calculate the factorial of a number recursively."}
]

messages2 = [
    {"role": "system", "content": "You are Qwen, a helpful coding assistant created by Alibaba Cloud. You excel at writing, debugging, and explaining code."},
    {"role": "user", "content": "Debug the following Python code:\n\ndef divide(a, b):\n    return a / b\n\nprint(divide(10, 0))"}
]

# Apply chat template to format the messages into a single string for the model
# `tokenize=False` means we get a string, not token IDs
# `add_generation_prompt=True` adds a token to signal the start of the assistant's response
formatted_prompt1 = tokenizer.apply_chat_template(messages1, tokenize=False, add_generation_prompt=True)
formatted_prompt2 = tokenizer.apply_chat_template(messages2, tokenize=False, add_generation_prompt=True)

prompts = [formatted_prompt1, formatted_prompt2]

# --- Generate Outputs ---
print("\nGenerating responses...")
outputs = llm.generate(prompts, sampling_params)

print(outputs)