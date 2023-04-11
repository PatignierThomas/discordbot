import os


import discord
from dotenv import load_dotenv
import openai

# load the token of the bot
load_dotenv('discord_token.env')
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# load openai api_key and the organization id on openai website
load_dotenv('openai_token.env')
openai.api_key = os.getenv("OPENAI_TOKEN")
openai.organization = "org-u4Eh797mWW2nowGtkXGXU7Li"

# give permission to the bot
intents = discord.Intents(messages=True)
intents.message_content = True

client = discord.Client(intents=intents)

# allow to alter chatGPT response style
msg_system = "You are a helpful assistant."

# add line below to current_conv in order to make the bot act like specified in msg_system
# {"role": "system", "content": msg_system},

current_conv = []


def chatgpt_reply(conv):
    """ send the request to the API and return the response

    :param conv: necessary for conversation history and personalization
    :return: the reply of the API
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conv,
        max_tokens=400
        )

    return completion['choices'][0]['message']['content']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """ post the chatGPT reply on selected discord channel and disabled/enable conversation history

    :param message: the message send by the user on the channel
    :return:
    """
    # prevent bot from replying to itself
    if message.author == client.user:
        return
    # replace id with the server-specific channel ID
    if message.channel.id == 1093893004927963207:
        # comment both line below for letting chatGPT remember conversation history.
        # WARNING: Will consume more token per request the longer the history goes.
        msg = message.content
        msg = str(msg)
        current_conv.append({"role": "user", "content": msg})
        reply = chatgpt_reply(current_conv)
        current_conv.append({"role": "assistant", "content": reply})
        await message.reply(reply, mention_author=True)
        current_conv.remove({"role": "user", "content": msg})
        current_conv.remove({"role": "assistant", "content": reply})


client.run(DISCORD_TOKEN)
