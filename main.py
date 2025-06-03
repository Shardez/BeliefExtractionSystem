from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from ollama import Client
import pandas as pd
from BES_Worfklows import detect_belief, extract_belief, process_message

ollama_base_url = "http://localhost:11434" # local
ollama_client = Client(host=ollama_base_url) 

# Enable / disable saving the analysis results to .csv file
save_csv = True

conversations_out_csv_filepath = './data/conversations_belief_analysis.csv'

# Initialize .csv file with the following column names
if save_csv:
    column_names = pd.DataFrame(columns = ['ref_conversation_id', 'ref_user_id', 'transaction_date', 
                                    'transaction_time', 'screen_name', 'message',
                                    'detection_reasoning_trace', 'belief_detected', 
                                    'analysis_reasoning_trace', 'belief','impact','dimension','category'])
    column_names.to_csv(conversations_out_csv_filepath, index=False)

# Specifies reasoning model and its parameters
reasoning_model_name = "qwen3:4b-q4_K_M"
reasoning_model_parameters = {"model_name": reasoning_model_name,
                    "temperature" : 0,
                    "top_p" : 0.95,
                    "top_k" : 50,
                    "min_p" : 0.1,
                    "think" : True
                    }

# Specifies model for structured output generation and its parameters
text_2_json_model_name = "Osmosis/Osmosis-Structure-0.6B"
text_2_json_model_parameters = {"model_name": text_2_json_model_name,
                    "temperature" : 0,
                    "top_p" : 0.95,
                    "top_k" : 50,
                    "min_p" : 0.1
                    }

app = FastAPI()

@app.post("/api/analyze_multiple_messages")
async def analyze_multiple_messages(request: Request):
    data = await request.json()
    response = []
    
    # Supplied JSON object can have multiple conversations with multiple messages
    for conversation in data:
        for message in conversation['messages_list']:
            # For each meassage get result of the analysis as a pandas dataframe with a single row
            df_row = process_message(message, reasoning_model_parameters, text_2_json_model_parameters, ollama_client)
            
            if save_csv:
                df_row.to_csv(conversations_out_csv_filepath, mode='a', index=False, header=False)

            # Convert the resulting pandas dataframe (with a single row) into JSON
            row_json = df_row.iloc[[0]].to_json(orient='records', index=False)
            response.append(row_json)

    return JSONResponse(content=response)

@app.post("/api/analyze_single_message")
async def analyze_single_message(request: Request):
    message = await request.json()
    
    # Get result of the analysis as a pandas dataframe with a single row
    df_row = process_message(message, reasoning_model_parameters, text_2_json_model_parameters, ollama_client)
    
    if save_csv:
        df_row.to_csv(conversations_out_csv_filepath, mode='a', index=False, header=False)

    # Convert the resulting pandas dataframe (with a single row) into JSON
    row_json = df_row.iloc[[0]].to_json(orient='records', index=False)
    
    return JSONResponse(content=row_json)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=11511)