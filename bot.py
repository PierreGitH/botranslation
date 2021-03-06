# bot.py
import os
from translation import get_translation

from dotenv import load_dotenv

# 1
from discord.ext import commands

translation_languages = {
    "π¬π§": "en",
    "π«π·": "fr",
    "πΊπΈ": "en",
    "πͺπΈ": "es",
}


async def translate_from_reaction(reaction, source="auto"):
    # await reaction.remove(user)
    # Targeted language for the translation is the reaction
    target = translation_languages[reaction.emoji]
    # Translate the message
    translated_text = get_translation(reaction.message.content, target=target, source=source)
    # Reply to the message with the translated text
    sent_message = await reaction.message.reply(translated_text)
    # Indicates the language by the same flag reaction from the bot
    await sent_message.add_reaction(reaction.emoji)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')


@bot.command(name='translate')
async def translate(ctx):
    valid_keys = ['source', 'target']
    lst_message = ctx.message.content.split(" ")
    params = {}
    for check_key in lst_message[1:]:
        command = check_key.split("=")
        if command[0] in valid_keys:
            params[command[0]] = command[1]
        else:
            break

    if 'source' in params.keys():
        source = params['source']
    else:
        source = "auto"

    if 'target' in params.keys():
        target = params['target']
    else:
        target = None

    if target is None:
        await ctx.send("ERROR, you must specify a targeted language for the translation")
    else:
        message = " ".join(lst_message[len(params.keys()) + 1:])
        translated_text = get_translation(message, target=target, source=source)
        await ctx.send(translated_text)


@bot.event
async def on_reaction_add(reaction, user):
    # Translate a message according to a reaction with a supported flag and the language is detected automatically
    if not user.bot and reaction.message.author != bot.user and reaction.emoji in translation_languages.keys():
        await translate_from_reaction(reaction, source="auto")

    # If the language detection failed, allow a user to react to the bot message with the flag corresponding to the
    # language of the initial message
    if not user.bot and reaction.message.author == bot.user and reaction.emoji in translation_languages.keys():
        # Modify the source language of the message
        source = translation_languages[reaction.emoji]
        # Get the initial message
        ref_message = reaction.message.reference.cached_message
        # Loop through the reaction that triggered previous translation and give a new translation with the correct
        # source
        for ref_reaction in ref_message.reactions:
            if not user.bot and ref_reaction.message.author != bot.user and ref_reaction.emoji in \
                    translation_languages.keys():
                await translate_from_reaction(ref_reaction, source=source)


bot.run(TOKEN)
