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


TEMPERATURE = 0.3
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = key)



assistant = client.beta.assistants.retrieve('asst_CHF9O43gRnpzwSo3f989QU2S')
print(assistant.name)


PROMPT_FIRST_PASS = """
Your research project involves going through testimony of the highly public Royal Commission on the Australian Government Robodebt scandal. 

The attached 'statements.txt' file contains a series of statements, one on each line, including the first line.

Produce a table of themes and scores for each statement. Include the text of the statement verbatim.

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

Scores should be in the range [0-100], depending on relevance. 0 means 'not relevant at all', 100 means 'extremely relevant'.

Be parsimonious with scores. Take your time and consider how relevant the themes are to each statement. Only apply scores to what you think are the most relevant themes.

Make sure to include each and every statement in the analysis.
"""



PROMPT_FIRST_PASS_FULL = """
Your research project involves going through testimony of the highly public Royal Commission on the Australian Government Robodebt scandal. 

The attached 'statements.txt' file contains a series of statements, one on each line, including the first line.

Produce a table of themes and scores for each statement. 

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

Scores should be in the range [0-100], depending on relevance. 0 means 'not relevant at all', 100 means 'extremely relevant'.

Be parsimonious with scores. Take your time and consider how relevant the themes are to each statement. Only apply scores to what you think are the most relevant themes.

Very important: Make sure to include each and every statement in the analysis.
"""

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

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

async def first_pass(thread, statements):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=PROMPT_FIRST_PASS_FULL
        , attachments=[{'file_id': statements.id, 'tools': [{'type': 'file_search'}]}]
    )

    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        temperature=TEMPERATURE
    )


async def second_pass(thread, statements):
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="""

The table you produced in the previous step is a good first pass. 

Bearing in mind your training as a qualitative researcher, do the same thing again, but this time take your time. 

Revise the scores if necessary. Be critical – if a statement appears to be couched in rhetoric of excuse-making, do not be concerned about applying a theme like 'Denial of Personal Responsibility'.

Consider being even more parsimonious with scores. Only apply scores to what you think are the most relevant themes.

After creating the entire table, include a comment about what you changed, and why.

Make sure to include all statements in the analysis.

"""
        
    )
    
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        max_prompt_tokens = 8000,
        max_completion_tokens = 8000,
        temperature=TEMPERATURE
    )



async def main():

    # Upload a file with an "assistants" purpose
    statements = client.files.create(
        file=open("data/statements.txt", "rb"),
        purpose='assistants'
    )

    thread = client.beta.threads.create()


    run = await first_pass(thread, statements)
    run = await wait_on_run(run, thread)
    
    run = await second_pass(thread, statements)
    run = await wait_on_run(run, thread)
    

    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order = "asc"
    )

    for index, message in enumerate(messages):
        print(message.id)
        print(message.created_at)
        print(message.status)
        if message.role == "assistant":
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