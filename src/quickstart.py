import os
import requests
import json
import openai

openai.api_key = 'ba9db13d298449afa4896f2746f105cd'
openai.api_base =  'https://rakbank-openai-research.openai.azure.com/' # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the future

deployment_name='davinci' #This will correspond to the custom name you chose for your deployment when you deployed a model. 

# Send a completion call to generate an answer
Query = "Enter your Query here: "
print(Query)
start_phrase = input()
response = openai.Completion.create(engine=deployment_name, prompt=start_phrase, max_tokens=1000)
text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
print(text)

