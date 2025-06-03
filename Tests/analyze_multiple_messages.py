import json
import requests


url = "http://localhost:11511/api/analyze_multiple_messages"

conversations_json_filepath = './data/conversations_short.json'
#conversations_json_filepath = './data/conversations.json'

with open(conversations_json_filepath, 'r') as file:
    data = json.load(file)

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.status_code)

if response.status_code == 200:
    json_response = json.loads(str(response.text))
    print(json_response)