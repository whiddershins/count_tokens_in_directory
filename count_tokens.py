import os
import tiktoken
# gotta install tiktoken first and maybe transformers too
# pip install tiktoken
# pip install transformers

# Configuration
DIRECTORY_PATH = "/path/to/your/file"  # Replace with the desired directory path
RECURSIVELY = True  # Set to False if recursive search is not needed
FILE_EXTENSIONS = ['.txt', '.md', '.ts']  # Add supported file extensions
ENCODER = 'cl100k_base'  # Replace with the desired encoder

# this list is from the openAI cookbook https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
# cl100k_base:	gpt-4, gpt-3.5-turbo, text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
# p50k_base:	Codex models, text-davinci-002, text-davinci-003
# r50k_base (or gpt2): 	GPT-3 models like davinci

# Initialize tokenizer
tokenizer = tiktoken.get_encoding(ENCODER)

def tokenize_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        tokens = tokenizer.encode(content)
        return len(tokens)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def process_directory(directory_path, recursively):
    token_counts = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                full_path = os.path.join(root, file)
                token_count = tokenize_file(full_path)
                token_counts[full_path] = token_count
        if not recursively:
            break
    return token_counts

# Process the directory and print results
results = process_directory(DIRECTORY_PATH, RECURSIVELY)

total_tokens = sum(results.values())

for file_path, count in results.items():
    print(f"{file_path}: {count} tokens")

print(f"Total tokens: {total_tokens}")

# Optionally, save results to a file in this directory
# with open('token_counts.txt', 'w') as out_file:
#     out_file.write(f"Total tokens: {total_tokens}\n\n")
#     for file_path, count in results.items():
#         out_file.write(f"{file_path}: {count} tokens\n")
