import pandas as pd
from datetime import datetime

from BES_System_Prompts import DETECT_SELF_PERCEPTION_PROMPT, EXTRACT_SELF_PERCEPTION_PROMPT
from BES_Pydantic_Models import DetectBelief, ExtractBelief
from BES_Ollama import ollama_reason, ollama_text_2_json

def datetime_parser(timestamp):
    """Splits timestamp into date and time"""
    # Parse the timestamp (strip 'Z' for UTC)
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return dt.date(), dt.time()

def detect_belief(df_row, row_index, reasoning_model_parameters, text_2_json_model_parameters, ollama_client):
    """Analyzes conversational text to detect the presence of user beliefs related to mental resilience and self-perception.
    Returns belief_detected, which is true if such a belief is detected and false otherwise. Additionally, returns a reasoning trace.
    """
    detection_reasoning_trace = ""
    belief_detected = False

    ref_user_id = df_row.at[row_index, 'ref_user_id']

    if ref_user_id != 1:
        user_input = df_row.at[row_index, 'message']
        print('USER INPUT:', user_input)
        detection_reasoning_trace = ollama_reason(user_input, DETECT_SELF_PERCEPTION_PROMPT, reasoning_model_parameters, ollama_client)
        belief_status = ollama_text_2_json(detection_reasoning_trace, DetectBelief, text_2_json_model_parameters, ollama_client)
        print(belief_status)
        belief_detected = belief_status['belief_detected']

    return detection_reasoning_trace, belief_detected

def extract_belief(df_row, row_index, reasoning_model_parameters, text_2_json_model_parameters, ollama_client):
    """ Analyzes conversational text to identify, categorize, and evaluate user beliefs related to mental resilience and self-perception.
    Extracts and returns the belief, its impact ("positive" or "negative"), the dimension and category of the belief, along with the reasoning trace.
    """
    analysis_reasoning_trace = ""
    belief_analysis = { "belief": "",
                        "impact": "",
                        "dimension": "",
                        "category": ""}

    ref_user_id = df_row.at[row_index, 'ref_user_id']
    belief_detected = df_row.at[row_index, 'belief_detected']
    
    if ref_user_id != 1 and belief_detected:
        user_input = df_row.at[row_index, 'message']
        print('USER INPUT:', user_input)
        analysis_reasoning_trace = ollama_reason(user_input, EXTRACT_SELF_PERCEPTION_PROMPT, reasoning_model_parameters, ollama_client)
        belief_analysis = ollama_text_2_json(analysis_reasoning_trace, ExtractBelief, text_2_json_model_parameters, ollama_client)
        print(belief_analysis)

    return analysis_reasoning_trace, belief_analysis

def process_message(message, reasoning_model_parameters, text_2_json_model_parameters, ollama_client):
    """ Implements a sequential workflow that first checks whether the conversational text contains any user beliefs related to mental resilience and self-perception.
    If such beliefs are found, the algorithm proceeds to analyze the belief, determine its impact ("positive" or "negative"), and identify the dimension and category of the belief.
    """
    date, time = datetime_parser(timestamp = message['transaction_datetime_utc'])
    df_row = pd.DataFrame({'ref_conversation_id': [message['ref_conversation_id']], 
                            'ref_user_id': [message['ref_user_id']], 
                            'transaction_date': [date],
                            'transaction_time': [time],
                            'screen_name': [message['screen_name']],
                            'message': [message['message']],
                            'detection_reasoning_trace': [""],
                            'belief_detected':[False],
                            'analysis_reasoning_trace':[""],
                            'belief':[""],
                            'impact':[""],
                            'dimension':[""],
                            'category':[""]})
    
    detection_reasoning_trace, belief_detected = detect_belief(df_row, 0, reasoning_model_parameters, text_2_json_model_parameters, ollama_client)
    df_row['detection_reasoning_trace'] = [detection_reasoning_trace]
    df_row['belief_detected'] = [belief_detected]
    
    if belief_detected:
        analysis_reasoning_trace, belief_analysis = extract_belief(df_row, 0, reasoning_model_parameters, text_2_json_model_parameters, ollama_client)
        df_row['analysis_reasoning_trace'] = [analysis_reasoning_trace]
        df_row['belief'] = [belief_analysis['belief']]
        df_row['impact'] = [belief_analysis['impact']]
        df_row['dimension'] = [belief_analysis['dimension']]
        df_row['category'] = [belief_analysis['category']]
    
    return df_row