import json
import requests

url = "http://localhost:11511/api/analyze_single_message"

conversations_json_filepath = './data/conversations_short.json'
#conversations_json_filepath = './data/conversations.json'

output = []
with open(conversations_json_filepath, 'r') as file:
    data = json.load(file)
    for object in data:
        for message in object['messages_list']:
            #print(message)
            response = requests.post(url, json=message)
            print(response.status_code)
            if response.status_code == 200:
                json_response = json.loads(str(response.text))
                json_response = json.loads(json_response)

                item = json_response[0]
                output.append(item)
                print("RESPONSE |", 'belief_detected:', item['belief_detected'], "|", 
                        'belief:', item['belief'], "|", 'impact:', item['impact'], "|", 
                        'dimension:', item['dimension'], "|", 'category:', item['category'])

with open('./data/response_single_message.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4)
