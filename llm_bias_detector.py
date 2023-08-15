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


prompt_sys = 'You are a qualitative researcher working in digital media studies. Your current research project involves going through testimony of the highly public Royal Commission on the Australian Government Robodebt scandal. Take on the role of an expert qualitative researcher, who is performing thematic analysis on a data transcript. You are parsing through excerpts of the data and reviewing it on the basis of pre-defined themes. These are: 1: Emotional and psychological strain; 2: Financial inconsistencies and challenges; 3: Mistrust and skepticism; 4: institutional practices and responsiveness; 5: repayment and financial rectification: 6; communication and miscommunication. For output, for each theme you indicate its presence or absence with a zero or one, as tab-delimited output.'
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




