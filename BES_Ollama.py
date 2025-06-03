import json

def ollama_reason(input_data, system_prompt, model_parameters, client):
    """ Processes input text following provided system prompt instructions using Ollama as language inference engine """

    # Disable reasoning for Qwen3 model
    if not model_parameters['think']:
        system_prompt += ' /nothink'

    messages = [{"role": "system","content": system_prompt},
                {'role': 'user', 'content': input_data}]

    response = client.chat(
        model = model_parameters["model_name"],
        messages = messages,
        #format = DetectBelief.model_json_schema(),
        options = {'temperature' : model_parameters["temperature"],
                    #'top_p': model_parameters["top_p"],
                    #'top_k': model_parameters["top_k"],
                    #'min_p': model_parameters["min_p"],
                    }
        )

    return response['message']['content'] 

def ollama_text_2_json(reasoning_trace, BeliefModel, model_parameters, client):
    """ Extracts the features defined in the Pydanctic 'BeliefModel' from another model's response (including the reasoning part). 
    Uses the corresponding JSON schema for structured output """

    messages = [
            {
            "role": "system",
            "content": f"You are a helpful assistant that understands and translates text to JSON format according to the following schema. {BeliefModel.model_json_schema()}"
            },
            {
            'role': 'user',
            'content': reasoning_trace,
            }
        ]
    
    response = client.chat(
        messages=messages,
        model = model_parameters["model_name"],
        format = BeliefModel.model_json_schema(),
        options = {'temperature' : model_parameters["temperature"],
                    #'top_p': model_parameters["top_p"],
                    #'top_k': model_parameters["top_k"],
                    #'min_p': model_parameters["min_p"],
                    }
        )
    
    return json.loads(response['message']['content'])


async def ollama_reason_async(input_data, system_prompt, model_parameters, client):
    """ Async version | Processes input text following provided system prompt instructions using Ollama as language inference engine """

    messages = [{"role": "system","content": system_prompt},
                {'role': 'user', 'content': input_data}]

    response = await client.chat(
        model = model_parameters["model_name"],
        messages = messages,
        #format = DetectBelief.model_json_schema(),
        options = {'temperature' : model_parameters["temperature"],
                    #'top_p': model_parameters["top_p"],
                    #'top_k': model_parameters["top_k"],
                    #'min_p': model_parameters["min_p"],
                    }
        )
    
    return response['message']['content'] 


async def ollama_text_2_json_async(reasoning_trace, BeliefModel, model_parameters, client):
    """ Async version | Extracts the features defined in the Pydanctic 'BeliefModel' from another model's response (including the reasoning part). 
    Uses the corresponding JSON schema for structured output """

    messages = [
            {
            "role": "system",
            "content": f"You are a helpful assistant that understands and translates text to JSON format according to the following schema. {BeliefModel.model_json_schema()}"
            },
            {
            'role': 'user',
            'content': reasoning_trace,
            }
        ]
    
    response = await client.chat(
        messages=messages,
        model = model_parameters["model_name"],
        format = BeliefModel.model_json_schema(),
        options = {'temperature' : model_parameters["temperature"],
                    #'top_p': model_parameters["top_p"],
                    #'top_k': model_parameters["top_k"],
                    #'min_p': model_parameters["min_p"],
                    }
        )

    return json.loads(response['message']['content']) 