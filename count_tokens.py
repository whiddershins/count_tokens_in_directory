#!/Users/sarthcalhoun/count_token_env/bin/python3
import os
import sys
import tiktoken
import json

# gotta install tiktoken first and maybe transformers too
# pip install tiktoken
# pip install transformers

# Configuration
RECURSIVELY = True  # Set to False if recursive search is not needed
FILE_EXTENSIONS = ['.txt', '.md', '.ts']  # Add supported file extensions
ENCODER = 'o200k_base'  # Replace with the desired encoder
# this list is from the openAI cookbook https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
# o200k_base    gpt-4o, gpt-4o-mini
# cl100k_base:  gpt-4, gpt-3.5-turbo, text-embedding-ada-002, text-embedding-3-small, text-embedding-3-large
# p50k_base:    Codex models, text-davinci-002, text-davinci-003
# r50k_base (or gpt2):  GPT-3 models like davinci

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

def main():
    # Check if a directory path was provided as an argument
    if len(sys.argv) < 2:
        print("Error: Please provide a directory path as an argument.")
        print("Usage: python3 script.py /path/to/directory")
        sys.exit(1)

    directory_path = sys.argv[1]
    
    # Verify the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
        sys.exit(1)

    # Process the directory and prepare results
    results = process_directory(directory_path, RECURSIVELY)
    total_tokens = sum(results.values())
    file_count = len(results)
    
    # Create a summary for notification
    summary = {
        "directory": directory_path,
        "file_count": file_count,
        "total_tokens": total_tokens,
        "encoder": ENCODER
    }
    
    # Print the summary as JSON for Automator to parse
    print(json.dumps(summary))
    
    # Print detailed results for terminal or log file
    for file_path, count in results.items():
        print(f"{file_path}: {count} tokens")
    
    # Optionally, save results to a file in the directory
    output_file = os.path.join(directory_path, 'token_counts.txt')
    with open(output_file, 'w') as out_file:
        out_file.write(f"Total tokens: {total_tokens} across {file_count} files\n\n")
        for file_path, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
            out_file.write(f"{file_path}: {count} tokens\n")
    
    # Return success code
    return 0

if __name__ == "__main__":
    main()