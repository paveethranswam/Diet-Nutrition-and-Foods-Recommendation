import os
import openai

# Load API key
openai.api_key = "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"

prompt = "Say this is a test"
         
response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=7)

print(response.choices[0].text)