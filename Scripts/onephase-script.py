import os
import json
import re
import sys
import time
import openai
prompt_path = "PROMPT_PATH"
oneshot_results = f"RESULTS_DIRECTORY.JSON"
data_path = f"PATH_TO_CODENETMUT.JSON"

def chatgpt_interaction():
    with open('temporary-prompt.txt', 'r') as file:
        prompt = file.read()

    openai.api_type = "azure"
    openai.api_base = "YOUR_API_BASE"
    openai.api_version = "YOU_SELECTED_PREVIEW"
    deployment_name = "DEPLOYMENT_NAME"
    openai.api_key = "YOUR_API_KEY"
    response = openai.ChatCompletion.create(
        engine="DEPLOYMENT_NAME", # The deployment name you chose when you deployed the GPT-3.5-Turbo model.
        messages=[
            {"role": "system", "content": prompt}
        ],
        timeout=120
    )
    return response.choices[0]['message']['content']

def read_part_1_and_example():
    with open('./prompt.txt', 'r') as file:
        prompt1 = file.read()
    return prompt1

def extract_symbols(code):
    lines = code.split('\n')
    symbols = []
    for line in lines:
        match = re.match(r'^\s*([>!]+)', line)
        if match:
            symbols.append(match.group(1))
    return symbols

def remove_comments_and_blank_lines(code):
    # Remove single-line comments
    code = re.sub(r'#.*', '', code)
    # Remove multi-line comments
    code = re.sub(r"'''(.*?)'''", '', code, flags=re.DOTALL)
    code = re.sub(r'"""(.*?)"""', '', code, flags=re.DOTALL)
    # # Remove completely blank lines or contains only > or !
    lines = code.split('\n')
    clean_lines = [line for line in lines if line.strip() != '' and not re.match(r'^\s*[>!]+\s*$', line)]
    code = '\n'.join(clean_lines)

def insert_method_in_prompt(p1, code):
    s1 = p1 + '\n' + "CODE:" + '\n'
    s2 = s1 + code + '\n' 
    final_prompt = s2
    return final_prompt

i = 0
def zeroshot_script(index):
    while i==index:
        chatgpt_prompt = read_part_1_and_example()
        results_dict = {}
        try:
            with open(data_path, 'r') as json_file:  
                    data = json.load(json_file)
                    for key, item in data.items():
                        if int(item['id']) == i:
                                code_id = item["id"]
                                print(code_id)
                                raw_code = item["code"]
                                temp_text = chatgpt_prompt
                                prompt = insert_method_in_prompt(temp_text, str(raw_code))
                                with open(prompt_path, 'w') as file:
                                    file.write(prompt)
                                start_time = time.time()
                                response_text = chatgpt_interaction()
                                end_time = time.time()
                                time_taken = end_time - start_time
                                chatgpt_predictedcc_symbols = extract_symbols(response_text) #MIGHT CAUSE ISSUE
                                print('Predicted:',chatgpt_predictedcc_symbols)
                                results_dict[code_id] = {
                                    "ID": code_id,
                                    "Predicted": chatgpt_predictedcc_symbols,
                                    "Time": time_taken
                                }
        except (UnicodeDecodeError, UnicodeEncodeError) as e:
            print("UnicodeDecodeError")
        i+=1
