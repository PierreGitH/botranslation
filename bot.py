# bot.py
import os
import random
from translation import get_translation

import discord
from dotenv import load_dotenv

# 1
from discord.ext import commands


translation_languages = {
    "🇬🇧":"en",
    "🇫🇷":"fr",
    "🇺🇸":"en",
    "🇪🇸":"es",
}


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
    # get_translation("Ceci est un test", "en", source="auto")


@bot.event
async def on_reaction_add(reaction, user):
    # Steals your reaction by removing the original and adding it's own
    if not user.bot and reaction.message.author != bot.user and reaction.emoji in translation_languages.keys():
        # await reaction.remove(user)
        target = translation_languages[reaction.emoji]
        translated_text = get_translation(reaction.message.content, target=target, source="auto")
        sent_message = await reaction.message.reply(translated_text)
        await sent_message.add_reaction(reaction.emoji)

    if not user.bot and reaction.message.author == bot.user and reaction.emoji in translation_languages.keys():
        source = translation_languages[reaction.emoji]
        ref_message = reaction.message.reference.cached_message
        for ref_reaction in ref_message.reactions:
            if not user.bot and ref_message.author != bot.user and ref_reaction.emoji in translation_languages.keys():
                target = translation_languages[ref_reaction.emoji]
                translated_text = get_translation(ref_message.content, target=target, source=source)
                sent_message = await ref_message.reply(translated_text)
                await sent_message.add_reaction(ref_reaction.emoji)

bot.run(TOKEN)
