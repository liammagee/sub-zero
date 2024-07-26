from openai import OpenAI
from groq import Groq
import os
import pandas as pd
from dotenv import load_dotenv
import os
import glob
import re


# Load environment variables
load_dotenv()


# Set up OpenAI API
client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))
model="gpt-4o"
# Set up Groq / Llama API
# client = Groq(api_key=os.getenv('GROQ_API_KEY'))
# model="llama-3.1-8b-instant"

file1='synthesis-media_report-with-gpt4-o-part1.md'
file2='synthesis-media_report-with-gpt4-o-part2.md'

try:
    file_contents = []
    for md_file in [file1, file2]:
        with open(md_file, 'r') as file:
            file_contents.append(file.read())

    all_the_content = "\n\n".join(file_contents)
    # with open('combination_of_all_the_content.md', 'w') as file:
    #     file.write(all_the_content)
    # print("file created!!!!!")
except Exception as e:
    print(f"Error processing content: {e}")


def summary_with_gpt(content):
    sys_prompt = "You are a Professor of Media Studies at RMIT University. You are widely cited and highly sought-after commentator on media bias."
    #sys_prompt="You are a Director and script writer of a Broadway play production. You are highly renowned and celebrated for creating impactful, thought provoking plays about important issues. Leveraging the power of dialogue and storytelling, your characters often discuss conflicting perspectives creating a lasting impact for the audience."
    #sys_prompt = "You are a Director and script writer of a major Bollywood movie. You are highly renowned, and celebrated for using humour, sarcasm and satire in the dialogue in your movies to communicate complex and important issues. Leveraging the power of storytelling, your characters often discuss conflicting perspectives, that are illustrated through very humours interactions"
    #user_prompt = f"Compile a detailed media analysis report based on the notes compiled by two researchers (one left-wing, the other right-wing). Be impartial, systematic and comprehensive in your review. Use references to the articles (including titles and authors where possible) and quotes to substantiate your claims. Include a bibliography. The content that follows includes Markdown notes, where article titles are marked by `H1` headings.  \n\n'{content}'"
    #user_prompt = f"Compile a detailed media analysis report based on the notes compiled by four prespetives (one Techno_Optimist, one Luddite and one Neutral and one Global South Researcher). Be impartial, systematic and comprehensive in your review. Use references to the articles (including titles and authors where possible) and quotes to substantiate your claims. Include a bibliography. The content that follows includes Markdown notes, where article titles are marked by `H1` headings.  \n\n'{content}'"
    #user_prompt = f"Create a script of a play where four actor perspectives are presented in a dialogue format (one Techno_Optimist, one Luddite and one Neutral and one Global South Researcher). There should also be an impartial, systematic and comprehensive narrator of the play that sets the scenes and highlights important story points for the audience — breaking the fourth wall. The actors use references to articles (including titles and authors where possible) and quotes to substantiate their claims in the dialogue. Include a bibliography at the end referencing the sources from which the script is developed. The content that includes details about the scene, setting, actors, Markdown notes, where article titles are marked by H1 headings.  \n\n'{content}'"
    #user_prompt = f"Create a script of a movie where three actor perspectives are presented in a dialogue format (one Techno_Optimist, one Luddite and one Neutral and one Global South Researcher). There should also be an impartial, systematic and comprehensive narrator who is the protagonist, who is not part of the scene, but retelling what was happening to the audience. The narrator sets the scenes and highlights important story points for the audience — breaking the fourth wall. The rest of the actors use references to articles (including titles and authors where possible) and quotes to substantiate their claims in the dialogue. Include a bibliography at the end referencing the sources from which the script is developed. The content that includes details about the scene, setting, actors, Markdown notes, where article titles are marked by H1 headings.  \n\n'{content}'"
    #user_prompt = f"Compile a detailed media analysis report based on the notes compiled by four perspectives (one Techno_Optimist, one Luddite, one Global South, and one Neutral). Be impartial, systematic and comprehensive in your review. Provide an overview of all documents, summarizing and describing key points and perspectives. Substantiate your claims and analysis using titles, authors, and direct quotes where possible. Make it in the form of an executive summary, a suggested structure could be, introduction, findings, discussion, conclusion.  The content that includes details about the scene, setting, actors, Markdown notes, where article titles are marked by H1 headings.   \n\n'{content}'"
    #user_prompt = f"Compile a detailed media analysis report based on the notes compiled by four perspectives (one Techno_Optimist, one Luddite, one Global South, and one Neutral). Be impartial, systematic and comprehensive in your review. Provide an overview of all documents, summarizing and describing key points and perspectives. Substantiate your claims and analysis using titles, authors, and direct quotes where possible. Make it in the form of an executive summary, a suggested structure could be, introduction, findings, discussion, conclusion.  The content that includes details about the scene, setting, actors, Markdown notes, where article titles are marked by H1 headings.   \n\n'{content}'"
    #user_prompt = f"Compile a detailed media analysis report based on all the notes corresponding to 23 articles provided, by four perspectives (one Techno_Optimist, one Luddite, one Global South, and one Neutral). Be impartial, systematic and comprehensive in your review. Use references to the articles (including titles and authors) and quotes to substantiate your claims. Include a bibliography. The content that follows includes Markdown notes, where article titles are marked by H1 headings.  \n\n'{content}'"
    user_prompt =f"Considering the detailed media analysis report (whole document, not an aticle by article), compile a media analysis summary report.  Following should be only 4 titles in the summary 'Overall summary', 'Techno_Optimist perspective summary', 'Luddite perspective summary', 'Global South researcher perspective summary', and 'Neutral perspective summary'. Summarise them in epistemic terms. No need to iterate through each article title in writing. Substantiate your claims and analysis using titles, authors, and direct quotes where possible. Include a bibliography at the end referencing the sources from which the script is developed. \n\n'{content}'."
    #user_prompt = f"Compile a detailed media analysis report based on all the notes corresponding to 23 articles provided. For each article present a summary overview on ‘Critical perspective’. Be impartial, systematic and comprehensive in your review. Use references to the articles (including titles and authors) and quotes to substantiate your claims. Include a bibliography. The content that follows includes Markdown notes, where article titles are marked by H1 headings. Don't be lazy. create report considring all 23 articles.  \n\n'{content}'."

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response


synthesis = summary_with_gpt(all_the_content)
with open('combination_of_all_the_content.md', 'w') as file:
    file.write(all_the_content)
with open('summary-media_report-with-gpt4-o.md', 'w') as file:
    file.write(synthesis.choices[0].message.content)