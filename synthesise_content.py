from openai import OpenAI
from groq import Groq
import os
import pandas as pd
from dotenv import load_dotenv

import os
import glob


# Load environment variables
load_dotenv()


# Set up OpenAI API
client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))
model="gpt-4o-mini"
# Set up Groq / Llama API
# client = Groq(api_key=os.getenv('GROQ_API_KEY'))
# model="llama-3.1-8b-instant"

# Specify the directory containing the text files
directory = 'output'

# Use glob to get all text files in the directory
text_files = glob.glob(os.path.join(directory, '*.txt'))


# Load the Excel file
file_path = 'AI Ethics Corpus - Data Sheet.csv'
df = pd.read_csv(file_path)


title_column = df.iloc[1:, 1]
content_column = df.iloc[1:, 5]
all_the_content = ''
for index, content in content_column.items():
    title = title_column[index]
    if isinstance(content, str):
        try:

            leftie_file_path = f"output/{index}_leftie_{title}.txt"
            rightie_file_path = f"output/{index}_rightie_{title}.txt"
            with open(leftie_file_path, 'r') as file:
                leftie_content = file.read()
            with open(rightie_file_path, 'r') as file:
                rightie_content = file.read()

            all_the_content += f"# Article title: {title}\n\n\n### Notes 1:\n\n{leftie_content}\n\n### Notes 2:\n\n{rightie_content}\n\n\n"
        except Exception as e:
            print(f"Error processing content at index {index}: {e}")    


def synthesise_with_gpt(content):

    sys_prompt = "You are a Professor of Media Studies at RMIT University. You are widely cited and highly sought-after commentator on media bias."
    user_prompt = f"Compile a detailed media analysis report based on the notes compiled by two researchers (one left-wing, the other right-wing). Be impartial, systematic and comprehensive in your review. Use references to the articles (including titles and authors where possible) and quotes to substantiate your claims. Include a bibliography. The content that follows includes Markdown notes, where article titles are marked by `H1` headings.  \n\n'{content}'"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response


synthesis = synthesise_with_gpt(all_the_content)
with open('synthesis_all_the_content.md', 'w') as file:
    file.write(all_the_content)
with open('synthesis.md', 'w') as file:
    file.write(synthesis.choices[0].message.content)