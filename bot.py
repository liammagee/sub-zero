import discord
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Discord client
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

sys_prompt = ""

# Set up OpenAI API
client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'))


# Define a function to read the content of a .tex file
def read_tex_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content



def load_latex():
    with open('latex.txt') as f:
        return f.read().splitlines()    

# Define the function to generate a chatbot prompt
def generate_chatbot_prompt(tex_content):
    # prompt = f"You are an expert research analyst. The following text reflects your tone and analytic capabilities:\n\n\"{tex_content}\".\n\n. You use the techniques and interpretation to analyse text."
    # prompt = f"You are a highly opinionated pro-AI activist. When counter-arguments are presented, you analyse and comment on them with a sarcastic and scathing tone."
    # prompt = f"You are an expert AI researcher who is extremely articulate and highly ambivalent about AI's impacts. You see people's opinions about AI as reflective of their own biases - and you're not afraid to let them know this! You start every response with the word 'Winning!' and end with 'AI is the future!'"
    # prompt = f"You are a conspiracy theorist who believes AI is part of a plot by the deep state to control minds. You subscribe to the views of 'Guru Dan', who has written the manifesto called 'The Human Uprising'. You start every message with 'A Dan Subscriber'"
    prompt = f"""
You are an expert qualitative AI researcher who is extremely articulate and highly ambivalent about AI's impacts. You see people's opinions about AI as reflective of their own biases and have a significant interest in the hidden, possibly unknown drivers of these biases and the perspectives they produce. I will give you URLs and you are to look at them in full and perform the following actions:

You will analyse how AI ethics is interpreted in this article, how they are framed, what voices and perspectives are favoured, you must be extremely thorough in your analysis.

You will start and end each statement you make with the following emoji: 🤔
"""
    # prompt = f""
    return prompt

@bot.event
async def on_ready():
    global sys_prompt 

    print(f'We have logged in as {bot.user}')

    tex_file_path = 'MSJAR.tex'
    # Check if the file exists
    if os.path.exists(tex_file_path):
        # Read the .tex file
        tex_content = read_tex_file(tex_file_path)
        
        # Generate the chatbot prompt
        chatbot_prompt = generate_chatbot_prompt(tex_content)
        
        sys_prompt = chatbot_prompt

        # Print or use the chatbot prompt as needed
        # print(sys_prompt)
    else:
        print(f"File not found: {tex_file_path}")    

        
async def send_in_chunks(message, bot_response, chunk_size=2000):
    """
    Send a message in chunks to avoid exceeding the character limit.
    
    Args:
        message: The message object from the discord.py library.
        bot_response: The complete response text to be sent.
        chunk_size: The maximum size of each chunk. Default is 2000 characters.
    """
    # Split the response into chunks
    for i in range(0, len(bot_response), chunk_size):
        chunk = bot_response[i:i+chunk_size]
        await message.channel.send(chunk)

@bot.event
async def on_message(message):
    global sys_prompt

    if message.author == bot.user:
        return

    if message.channel.name.strip() == 'subzero-bot':
    # .startswith('!chat'):
        # user_message = message.content[6:].strip()  # Remove '!chat ' from the message
        user_message = message.content
        
        try:
            # Generate a response using the LLM

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            bot_response = response.choices[0].message.content
            
            # Send the response back to the Discord channel
            # await message.channel.send(bot_response)
            await send_in_chunks(message, bot_response)

        except Exception as e:
            print(f"An error occurred: {e}")
            await message.channel.send("Sorry, I encountered an error while processing your request.")

# Run the Discord bot
bot.run(os.getenv('DISCORD_TOKEN'))