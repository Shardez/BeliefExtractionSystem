# Belief Extraction System

## Description
The purpose of this project is to develop a REST API endpoint to evaluate the content of conversations and
determine what the user believes about themselves or a topic.

## Installation
```git clone https://github.com/Shardez/BeliefExtractionSystem```

### Ollama
Download and install Ollama locally for your OS:
https://ollama.com/download/

Install the Ollama Python library
```
pip install ollama
```

Pull and run qwen3:4b-q4_K_M language model 
```
ollama run qwen3:4b-q4_K_M
```
Chat with qwen3:4b-q4_K_M model via terminal to confirm that everything is working properly and you are getting responses from the model.

Pull Osmosis-Structure-0.6B model  
```
ollama pull Osmosis/Osmosis-Structure-0.6B:latest
```

### FastAPI
```
pip install fastapi
```

### uvicorn
```
pip install uvicorn
```

### Pandas
```
pip install pandas
```

## Structure
BES_Worfklows.py - implements the following logic: Implements a sequential workflow that first checks whether the conversational text contains any user beliefs related to mental resilience and self-perception. If such beliefs are found, the algorithm proceeds to analyze the belief, determine its impact ("positive" or "negative"), and identify the dimension and category of the belief.

BES_Ollama.py - implements text processing functionality using Ollama as language inference engine.

BES_Pydantic_Models.py - stores Pydantic models which are used for structured output generation.

BES_System_Prompts.py - stores system prompts used for detection and analysis of user beliefs related to mental resilience and self-perception.

main.py - implements FastAPI server with two POST endpoints:
- "/api/analyze_single_message" - which analyzes a single message at a time
- "/api/analyze_multiple_messages" - which sequentially processes messages present in messages_list for each conversation present in the supplied JSON object.

The model parameters used for reasoning and structured output can be configured using "reasoning_model_parameters" and "text_2_json_model_parameters"  
In addition to sending the response back to the client app it also allows to save analysis results to .csv file using "save_csv" variable (enabled by default)  

/tests/analyze_single_message.py - implements a simple client application which emulates API requests. loads conversations from .json and sends individual messages one by one to "api/analyze_single_message" endpoint

/tests/analyze_multiple_message.py - implements a simple client application which emulates API requests. loads all conversations from .json and sends them all together to "/api/analyze_multiple_messages" endpoint

/data/conversations.json - contains example conversational data.  
/data/conversations_short.json – a shortened version of conversation.json, contains single conversation with only two messages..

## How to Run
1. Make sure Ollama is running - you can check by running the following command in the terminal
```
ollama list
```
2. Start FastAPI uvicorn server by running
```
python main.py
```
3. Run either of the test in /tests/ folder. Modify "conversations_json_filepath" variable to process either short of full version of conversation.json
