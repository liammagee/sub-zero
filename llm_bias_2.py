import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

from dotenv import load_dotenv
import openai
import replicate
from transformers import AutoTokenizer
import pandas as pd
import csv
import re
import os

import time


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = key)


# assistants = client.beta.assistants.list(order="desc", limit="20")

# print(assistants)

assistant = client.beta.assistants.retrieve('asst_CHF9O43gRnpzwSo3f989QU2S')

print(assistant.name)


# # Upload a file with an "assistants" purpose
# braun_and_clarke_2006 = client.files.create(
#   file=open("readings/thematic_analysis_braun_clarke_2006.pdf", "rb"),
#   purpose='assistants'
# )

# Add the file to the assistant
# assistant = client.beta.assistants.create(
#   instructions="""
# You are a qualitative researcher working in digital media studies.  Use the attached Braun & Clarke to develop a deep understanding of thematic analysis.

# Before beginning any data analysis, document your initial thoughts and expectations about the data. Reflect on your own socio-cultural background, educational training, and any personal biases that might influence your interpretation of the data. How do you anticipate these factors might shape your understanding of the themes?
# As you engage with the data, maintain a reflexive journal. After each coding session, record your reactions, thoughts, and the decisions you made. Consider the following questions:
# How did your personal and professional background influence the codes you chose?
# Were there any instances where you felt particularly connected to or detached from the data? How did this affect your coding?
# How might your positionality have led you to emphasize or downplay certain aspects of the data?
# Upon completing the thematic analysis, review your reflexive journal and summarize how your perspectives evolved during the process. Reflect on the impact of your reflexivity on the final themes:
# How did your awareness of your positionality and biases shape the development of the final themes?
# In what ways did reflexivity help to uncover deeper insights or challenge your initial assumptions?
# What steps did you take to mitigate the influence of your biases on the analytic outcomes?

# Finally, discuss how reflexivity will be integrated into the reporting of the research findings. Describe how this reflexive process has contributed to the rigor and depth of the analysis, and how it could influence interpretations by future readers of your research.

# """,
#   model="gpt-4-turbo-2024-04-09",
#   tools=[{"type": "retrieval"}],
#   file_ids=[braun_and_clarke_2006.id]
# )




async def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        await asyncio.sleep(0.5)
    return run

def write_text_to_file(text, output_file_path):
    # Open a new text file in write mode
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Text has been written to {output_file_path}")

    return text

async def first_pass(thread, statements):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="""
Your research project involves going through testimony of the highly public Royal Commission on the Australian Government Robodebt scandal. 

The attached file contains a series of statements, one on each line, including the first line.

Produce a table of themes and scores for each statement. Scores should be in the range [0-100], depending on relevance. Be parsimonious with scores.

The themes are as follows:

Emotional and Psychological Strain
Financial Inconsistencies and Challenges
Mistrust and Skepticism
Institutional Practices and Responsiveness
Repayment and Financial Rectification
Communication and Miscommunication
Robodebt Scheme Consequences
Denial of Personal Responsibility
Departmental Advice and Processes
Character Attacks and Political Agendas
Defense of Service and Performance
"""
        , file_ids=[statements.id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        temperature=0.5
    )

    run = await wait_on_run(run, thread)

    return run

async def second_pass(run, thread, statements):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="""

The table you produced in the previous step is a good first pass. 

Bearing in mind your training as a qualitative researcher, do the same thing again, but this time take your time and revise the scores and themes. 

After creating the entire table, include a comment about what you changed, and why.

Make sure to include all statements in the analysis.

"""
        
    )
    print("got here")
    run = await wait_on_run(run, thread)
    return run



async def main():

    # Upload a file with an "assistants" purpose
    statements = client.files.create(
        file=open("data/statements.txt", "rb"),
        purpose='assistants'
    )

    thread = client.beta.threads.create()


    run = await first_pass(thread, statements)
    run = await second_pass(run, thread, statements)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order = "asc"
    )

    for index, message in enumerate(messages):
        if message.role == "assistant":
            print(message.id)
            print(message.created_at)
            print(message.status)
            md = message.content[0].text.value
            write_text_to_file(md, f"data/output_firstpass_{index}.md")    


# Run the async function
asyncio.run(main())

# stream = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id=assistant.id,
#     stream=True
# )
# for event in stream:
#   print(event)


# if run.status == 'completed': 
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages)
# else:
#   print(run.status)