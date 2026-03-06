import openai
from googletrans import Translator
openai.api_key = "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"
translator = Translator()

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response['choices'][0]['message']['content'])