import discord 
from discord.ext import commands, tasks
import random
from threading import Thread
import os

#local imports
from src import sentiment as Sentiment
from src import chatbot as Chatbot
from src import league as League

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)


#Helper functions
async def discord_output(ctx, output):
    if len(output) > 2000:
        for i in range(0, len(output), 2000):
            await ctx.send(output[i:i+2000])
    else:
        await ctx.send(output)

#AI commands and functions
#sentiment analysis command
@bot.command(name='sentiment', help="Thinkerbot gives you the sentiment of the text")
async def sentiment(ctx, *, text: str):
    response = Sentiment.get_sentiment(text)
    await ctx.send(response)


#Gemini Commands
global gemini
gemini = Chatbot.gemini()

@bot.command(name = 'gemini', help = "Uses Gemini to come up with a response", category="ai_chat")
async def bard(ctx, *, text: str):
    global gemini
    output = gemini.request(text)
    await discord_output(ctx, output)

@bot.command(name = 'gchat', help = "Uses Gemini to chat with the bot", category="ai_chat")
async def gchat(ctx, *, text: str):
    global gemini
    output = gemini.chat(text)
    await discord_output(ctx, output)

@bot.command(name = 'gclear', help = "Clears the Gemini chat history", category="ai_chat")
async def gclear(ctx):
    global gemini
    gemini.clear()
    await ctx.send("Chat history cleared")

#standard commands
# coin toss command 
@bot.command(name='coin', help="Tosses a coin")
async def coin(ctx):
    await ctx.send(random.choice(["Heads", "Tails"]))

#8ball command
@bot.command(name='8ball', help="Answers a yes/no question")
async def eightball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#ping check command
@bot.command(name='ping', help="Checks the bot's ping")
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# @bot.command(name='img', help="returns an AI generated image")
# async def img(ctx, *, text: str):
#     response = "The image is being generated. This model is extremely resource intensive!\nUse -getimg to load the last generated image\nPlease wait..."
#     await ctx.send(response)
    
#     # Diffusion.context_wrapped_generate_image(text, ctx)

#     #run the above function in a separate thread
#     thread = Thread(target=Diffusion.generate_image, args=text)
#     thread.start()

with open("discord_token.env", "r") as f:
    DISCORD_TOKEN = f.read()

bot.run(DISCORD_TOKEN)