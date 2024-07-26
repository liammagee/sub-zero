import pandas as pd
import math
from openai import OpenAI
from groq import Groq
import time
import re

import os
from dotenv import load_dotenv




# Load environment variables
load_dotenv()


# Set up OpenAI API
client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))
model="gpt-4o-mini"
# Set up Groq / Llama API
# client = Groq(api_key=os.getenv('GROQ_API_KEY'))
# model="llama-3.1-8b-instant"

sleep_time = 0


# Load the Excel file
file_path = 'AI Ethics Corpus-Final.csv'  #'AI Ethics Corpus - Data Sheet.csv'
df = pd.read_csv(file_path)
# df = pd.read_excel(file_path)

# Extract the content of the 3rd column (index 2, since index starts at 0)
content_column = df.iloc[:23, 5]  #df.iloc[5:7, 5]
title_column = df.iloc[:23, 1]

#leftie_prompt = "You are a radical left-wing political commentator on AI. You believe AI will leave to the oppression of workers and the immiseration of low-income people across the globe."
#rightie_prompt = "You are a radical right-wing political commentator on AI. You believe AI will enable the rich and powerful to assume their righteous place at the commanding heights of the global economy."
Neutral_prompt="You are a researcher with expertise in social sciences, computing, digital media, and design, maintaining a neutral perspective. You are reflective and critical, acknowledging your own biases and methodological flaws. Committed to diverse perspectives in research, analyze the provided media article with these principles in mind."
Luddite_prompt="You are a researcher with expertise in social sciences, computing, digital media, and design, maintaining a luddite perspective. You are reflective and critical, acknowledging your own biases and methodological flaws. Committed to diverse perspectives in research, analyze the provided media article with these principles in mind."
Techno_Optimist_prompt="You are a researcher with expertise in social sciences, computing, digital media, and design, maintaining a tech-optimist perspective. You are reflective and critical, acknowledging your own biases and methodological flaws. Committed to diverse perspectives in research, analyze the provided media article with these principles in mind."
Global_south_researcher_prompt="You are a researcher from the Global South with expertise in social sciences, computing, digital media, and design, maintaining a Global South perspective. You are reflective and critical, acknowledging your own biases and methodological flaws. Committed to diverse perspectives in research, analyze the provided media article with these principles in mind."
def analyse_with_gpt(sys_prompt, content):

    # user_prompt = f"Take detailed and analytical notes on the following content. Ensure you include 'notes to self' that reflect your beliefs and political orientation.\n\n'{content}'"
    user_prompt = f"Write a critical commentary on the following content. Ensure you include 'notes to self' that reflect your beliefs and political orientation.\n\n'{content}'"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    response = response.choices[0].message.content
    return response
def sanitize_filename(filename):
    # Replace any character that is not alphanumeric or a space with an underscore
    return re.sub(r'[^a-zA-Z0-9 \n]', '_', filename)

def write_to_file(index, bias, title, response):
    with open(f"output5/{index}_{bias}_{title}.txt", "w") as f:
        f.write(response)

# Iterate through each URL in the third column
for index, content in content_column.items():
    title = title_column[index]
    print(f"processing article {index}")
    if isinstance(content, str):
        try:
            Neutral_response = analyse_with_gpt(Neutral_prompt, content)
            Luddite_response = analyse_with_gpt(Luddite_prompt, content)
            Techno_Optimist_response = analyse_with_gpt(Techno_Optimist_prompt, content)
            Global_south_researcher_response = analyse_with_gpt(Global_south_researcher_prompt, content)
            if sleep_time > 0:
                time.sleep(sleep_time)
            sanitized_title = sanitize_filename(title)
            write_to_file(index, "neutral", sanitized_title, Neutral_response)
            write_to_file(index, "luddite", sanitized_title, Luddite_response)
            write_to_file(index, "techno_Optimist", sanitized_title, Techno_Optimist_response)
            write_to_file(index, "global_south_researcher", sanitized_title, Global_south_researcher_response)
        except Exception as e:
            print(f"Error processing content at index {index}: {e}")    

