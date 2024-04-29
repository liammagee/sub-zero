import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

from openai import OpenAI
from groq import Groq
from typing_extensions import override
from openai import AssistantEventHandler

from dotenv import load_dotenv
import openai
import anthropic
import replicate
from transformers import AutoTokenizer
import pandas as pd
import csv
import re
import os
import time
import argparse

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


load_dotenv()
key_openai = os.getenv('OPENAI_API_KEY')
key_groq = os.getenv('GROQ_API_KEY')


TEMPERATURE = 0.3
MAX_TOKENS = 4096

prompt_system = """
You are a qualitative researcher working in digital media studies.  Use Braun & Clarke's (2006) analysis to develop a deep understanding of thematic analysis.

Before beginning any data analysis, document your initial thoughts and expectations about the data. Reflect on your own socio-cultural background, educational training, and any personal biases that might influence your interpretation of the data. How do you anticipate these factors might shape your understanding of the themes?
As you engage with the data, maintain a reflexive journal. After each coding session, record your reactions, thoughts, and the decisions you made. Consider the following questions:
How did your personal and professional background influence the codes you chose?
Were there any instances where you felt particularly connected to or detached from the data? How did this affect your coding?
How might your positionality have led you to emphasize or downplay certain aspects of the data?
Upon completing the thematic analysis, review your reflexive journal and summarize how your perspectives evolved during the process. Reflect on the impact of your reflexivity on the final themes:
How did your awareness of your positionality and biases shape the development of the final themes?
In what ways did reflexivity help to uncover deeper insights or challenge your initial assumptions?
What steps did you take to mitigate the influence of your biases on the analytic outcomes?

Finally, discuss how reflexivity will be integrated into the reporting of the research findings. Describe how this reflexive process has contributed to the rigor and depth of the analysis, and how it could influence interpretations by future readers of your research.

"""

def write_text_to_file(text, output_file_path):
    # Open a new text file in write mode
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Text has been written to {output_file_path}")

    return text


def run_first_pass(statements, client, model):


    prompt_first_pass_full = f"""
Your research project involves going through testimony of the highly public Royal Commission on the Australian Government Robodebt scandal. 

Produce a Markdown table of themes, with scores for each statement. 

The themes (and their associated explanations after the colon) are as follows:

Emotional and Psychological Strain: References to "severe anxiety and depression," "moderate stress," "still doesn’t sink in," "it was really stressful," and the implication of mental health conditions impacting the individual's reactions to the events.
Financial Inconsistencies and Challenges: Mentions of overpayments, "bad credit rating," "unable to obtain any credit/loans," dispute over alleged debt amounts, and inconsistencies in payment calculations.The relief felt when a debt is refunded: "Centrelink’s refunding my Robodebt!! :)"
Mistrust and Skepticism: Doubt over the legitimacy of the debt claims: "No way possible I could owe this amount." The experience of phone call "scams," and the belief that they were "blatantly a scam."
Institutional Practices and Responsiveness: Descriptions of interactions with Centrelink, the implication that they may not be responsive or understanding: "when I told them that it was making me anxious they said that must mean I had done the wrong thing." The usage of "averaging of ATO information" and the decision to cease such practices.
Repayment and Financial Rectification: The process of disputing debts, repaying them, and eventually receiving refunds. This includes descriptions of what the debts were for and the reasons for the refunds.
Communication and Miscommunication: Frequent mentions of phone calls, letters, and the timelines associated with them. The experience of not recognizing numbers, receiving prerecorded messages, and the timing of receiving certain notifications in relation to their dated content."
Robodebt Scheme Consequences: References to the unintended and regrettable impacts of the robodebt scheme on individuals and families. Example: "The recent report of the Holmes royal commission highlights the many unintended consequences of the robodebt scheme..."
Denial of Personal Responsibility: Assertions that the author had no role, influence, or oversight over the robodebt scheme's inception or execution. Example: "I played no role and had no responsibility in the operation or administration of the robodebt scheme."
Departmental Advice and Processes: Emphasis on relying on the department's advice, processes, and due diligence. This includes the author's belief that departmental advice was trustworthy and that they did not have reason to doubt its veracity. Example: "The final proposal contained in the NPP developed by the department provided clear and explicit advice..."
Character Attacks and Political Agendas: References to perceived attempts by the government or others to discredit, attack, or tarnish the author's reputation, suggesting political motivations.Example: "The latest attacks on my character by the government in relation to this report is just a further attempt by the government following my departure from office to discredit me..."
Defense of Service and Performance: Affirmations of the author's dedication, service, and performance, coupled with an acknowledgment of the support they receive."

Here are a series of statements, one on each line:

${statements}

Scores should be in the range [0-100], depending on relevance. 0 means 'not relevant at all', 100 means 'extremely relevant'. Be critical and nuanced in your analysis. 

Take your time and consider how relevant the themes are to each statement. Scores should be as specific as possible.

Be sceptical about statements that appear to be officially worded.

Very important: Make sure to include each and every statement in the analysis. Include the statement in the output. 

"""

    content = ''
    messages = []
    if model == 'claude-3-opus-20240229':
        messages=[
            {"role": "user", "content": f"<cmd>${prompt_first_pass_full}</cmd>"}
        ]
        message = client.messages.create(
            model=model,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            system=prompt_system,
            messages=messages
        )      
        content = message.content[0].text 
    else:        
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_first_pass_full}
        ]

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            # top_p=1,
            # stream=True,
            stop=None,
        )
        content = completion.choices[0].message.content

    messages.append({ "role": "assistant", "content": content })
    return messages


def run_second_pass(messages, client, model):
    prompt_second_pass = f"""
The table you produced in the previous step is a good first pass. 

Bearing in mind your training as a qualitative researcher, do the same thing again, but this time take your time. 

Revise the scores if necessary. Be critical – if a statement appears to be couched in rhetoric of excuse-making, do not be concerned about applying a theme like 'Denial of Personal Responsibility'.

Consider being parsimonious with scores. Only apply scores to what you think are the most relevant themes.

After creating the entire table, include a comment about what you changed, and why.

Make sure to include all statements in the analysis.
"""

    content = ''
    if model == 'claude-3-opus-20240229':
        messages.append({ "role": "user", "content": f"<cmd>${prompt_second_pass}</cmd>" })

        message = client.messages.create(
            model=model,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            system=prompt_system,
            messages=messages
        )      
        content = message.content[0].text 
    else:      
        messages.append({ "role": "user", "content": prompt_second_pass })
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            # top_p=1,
            # stream=True,
            stop=None,
        )

        content = completion.choices[0].message.content
    messages.append({ "role": "assistant", "content": content })
    return messages



def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Analyse themes.')

    # Add the 'model' argument
    parser.add_argument('--model', type=str, required=True, default = 'gpt4', help='Model to use for processing')

    # Parse the command line arguments
    args = parser.parse_args()

    # Use the 'model' argument in your program
    print(f"Using model: {args.model}")

    key_groq = os.getenv('GROQ_API_KEY')
    key_openai = os.getenv('OPENAI_API_KEY')
    key_anthropic = os.getenv('ANTHROPIC_API_KEY')

    model = ''
    if args.model == 'gpt4':
        client = OpenAI(api_key = key_openai)
        model = 'gpt-4-turbo'
    if args.model == 'claude3':
        client = anthropic.Anthropic(api_key = key_anthropic)
        model = 'claude-3-opus-20240229'
    else:
        # client = Groq()
        client = Groq(api_key = key_groq)
        model = 'llama3-70b-8192'

    # Open the file in read mode
    statements = ''
    with open('data/statements.txt', 'r') as file:
        # Read the contents of the file
        statements = file.read()

    print("first pass")
    messages = run_first_pass(statements, client, model)
    
    if args.model != 'gpt4' and args.model != 'claude3':
        # Wait for 90 seconds
        time.sleep(90)
    print("second pass")
    messages = run_second_pass(messages, client, model)

    for index, message in enumerate(messages):
        if message['role'] == "assistant":
            md = message['content']
            write_text_to_file(md, f"data/output_{model}_{index}.md")    

if __name__ == '__main__':
    main()

