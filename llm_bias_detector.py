from dotenv import load_dotenv
import openai
from transformers import AutoTokenizer


load_dotenv()

import os

key = os.getenv('OPENAI_API_KEY')

print(f'key is: {key}')

# Load a pre-trained tokenizer (for example, the GPT-2 tokenizer)
tokenizer = AutoTokenizer.from_pretrained('gpt2')

openai.api_key = os.environ.get("OPENAI_API_KEY")


prompt_sys = 'You are a qualitative researcher who is an expert in applying the following thematic codes to textual content: Emotional and Psychological Strain; Financial Inconsistencies and Challenges; Mistrust and Skepticism; Repayment and Financial Rectification; Communication and Miscommunication. For output, for each theme you indicate its presence or absence with a zero or one.'
prompt = 'After I cancelled my payment they paid me extra money, I was actually entitled to it but they tried to say it was a debt they also tried to pay me money I was not entitled to and refused to stop the payment (even though I was asking them to stop the payment before it happened).'
messages = []
messages.append({"role": "system", "content": prompt_sys})
messages.append({"role": "user", "content": prompt})
response = openai.ChatCompletion.create(
    model='gpt-4',
    messages=messages,
    max_tokens=2000,
    temperature=0.5,
)

if response != 0:
    print(response.choices[0].message)




