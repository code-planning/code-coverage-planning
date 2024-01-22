# Planning to Guide LLM for Code Coverage Prediction
Code coverage serves as a crucial metric to assess testing effectiveness, measuring the degree to which a test suite exercises different facets of the code, such as statements, branches, or paths. Despite its significance, coverage profilers necessitate access to the entire codebase, constraining their usefulness in situations where the code is incomplete or execution is not feasible, and even cost-prohibitive. While the utilization of Large Language Models (LLMs) for predicting code coverage has demonstrated success, challenges persist, particularly in achieving high accuracy due to the intricate, expansive space of multiple interdependent execution steps in a program. In this paper, we present CCPlan, a plan-based prompting approach
grounded in program semantics, which collaborates with LLMs to enhance code coverage prediction. To address the intricacies of predicting code coverage, CCPlan employs planning by discerning various types of statements in an execution flow. Planning empowers GPT to autonomously generate plans based on guided examples, and then CCPlan prompts the GPT model to predict code coverage (Action) based on the plan it generated (Reasoning). Our experiments evaluating CCPlan demonstrate high accuracy, achieving up to 55% in exact-match and 89% in statement-match. CCPlan performs relatively better than the baselines, achieving up to 33% and 19% relatively higher in those metrics. We also showed that due to highly accurate plans (90%), the GPT model predicts better code coverage. Moreover, we show CCPlan’s utility in correctly predicting the least covered statements as a downstream task.

### Install
This repository contains the source code for reproducing the results in our paper. Please start by cloning this repository:
```
https://github.com/code-planning/code-coverage-planning.git
```

### Dataset
The dataset used for the project was the CodeNetMut Test dataset. It can be downloaded as a .json file from the following OneDrive Folder - 
```
https://1drv.ms/u/s!AlEMxMpahF7qbDqCxJlp1_swkUE?e=Fgj0nu
```

### Scripts
We provide python scripts for reproducing our results in this work. There are 2 primary scripts - 
1. onephase-script.py - 
To run the single phase python script for either the one shot or few shot CCPlan prompting techniques, add your API_KEY and related fields in the chatgpt_interaction() function and include the file location for the prompt you want to use and run the script.

2. twophase.script.py - 
To run the dual phase python script for either the one shot or few shot CCPlan prompting techniques, add your API_KEY and related fields in the chatgpt_interaction() function and include the file locations for the 2 prompts  you want to use and run the script.

### Additional Information and requirements
For additional requirements and information regarding prompting GPT through API calls, please refer to the below guide provided by Microsoft for Azure OpenAI calls - 
```
https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?tabs=python&pivots=programming-language-chat-completions
```

### Results
The results for our project have been included in the "Results" folder. Each results.json file in this folder contains the GPT responses as well as the generates plans for each data example. 



