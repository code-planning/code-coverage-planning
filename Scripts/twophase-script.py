import os
import json
import re
import sys
import time
import openai

prompt_path = "PROMPT_PATH"
plan_prompt_path = "PLAN_PROMPT_PATH"
coverage_prompt_path = "COVERAGE_PROMPT_PATH"
oneshot_results = f"RESULTS_DIRECTORY.JSON"
data_path = f"PATH_TO_CODENETMUT.JSON"


def chatgpt_interaction(prompt_path):
    with open(prompt_path, 'r') as file:
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

def read_code():
    with open('./prompt.txt', 'r') as file:
        prompt1 = file.read()
    return prompt1

def read_code_and_plan():
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

def insert_code_in_prompt(p1, code):
    s1 = p1 + '\n' + "CODE:" + '\n'
    s2 = s1 + code + '\n' 
    final_prompt = s2
    return final_prompt

def insert_code_and_plan_in_prompt(p1, code, plan):
    s1 = p1 + '\n' + "CODE:" + '\n'
    s2 = s1 + code + '\n'
    s3 = s2 + '\n' + plan + '\n'
    final_prompt = s3
    return final_prompt

def add_line_numbers(code):
    lines = code.split('\n')
    formatted_code = ""
    for idx, line in enumerate(lines, start=1):
        formatted_code += f"Line {idx}: {line}\n"
    return formatted_code

i = 0
while i<19541:
    chatgpt_plan_prompt = read_code()
    chatgpt_coverage_prompt = read_code_and_plan()
    plan_results_dict = {}
    coverage_results_dict = {}
    try:
        with open(data_path, 'r') as json_file:  
                data = json.load(json_file)
                for key, item in data.items():
                    if int(item['id']) == i :
                            code_id = item["id"]
                            raw_code = item["code"]
                            serialized_code = add_line_numbers(raw_code)
                            temp_text1 = chatgpt_plan_prompt
                            prompt = insert_code_in_prompt(temp_text1, str(raw_code))
                            with open(prompt_path, 'w') as file:
                                file.write(prompt)
                            start_time = time.time()
                            response_text = chatgpt_interaction(plan_prompt_path)
                            end_time = time.time()
                            time_taken = end_time - start_time
                            plan_response_text = response_text
                            temp_text2 = chatgpt_coverage_prompt
                            prompt = insert_code_and_plan_in_prompt(temp_text2, str(raw_code), str(plan_response_text))
                            with open(coverage_prompt_path, 'w') as file:
                                file.write(prompt)
                            start_time = time.time()
                            response_text = chatgpt_interaction(coverage_prompt_path)
                            end_time = time.time()
                            time_taken = end_time - start_time
                            coverage_response_text = response_text
                            chatgpt_predictedcc_symbols = extract_symbols(coverage_response_text) #MIGHT CAUSE ISSUE
                            plan_results_dict[code_id] = {
                                "ID": code_id,
                                "Plan": plan_response_text,
                            }
                            coverage_results_dict[code_id] = {
                                "ID": code_id,
                                "Plan": plan_response_text,
                                "Code": coverage_response_text,
                                "Predicted": chatgpt_predictedcc_symbols,
                            }
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print("UnicodeDecodeError")
    with open('plan-results.json', 'a') as json_file:
        json.dump(plan_results_dict, json_file)
        json_file.write('\n')  # Add a newline for each entry
    with open('coverage-results.json', 'a') as json_file:
        json.dump(coverage_results_dict, json_file)
        json_file.write('\n')
    i+=1
