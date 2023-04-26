import openai
 
# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "ba9db13d298449afa4896f2746f105cd"
 
# Set the model and prompt
model_engine = "text-davinci-003"
Query = "Enter your Query here: "
print(Query)
name = input()  
prompt = name
 
# Set the maximum number of tokens to generate in the response
max_tokens = 4000
 
    # Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
 
# Print the response
print(completion.choices[0].text)