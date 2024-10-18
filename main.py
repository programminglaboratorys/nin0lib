#!/usr/bin/env nix-shell
#!nix-shell -p python3 python3Packages.websockets -i python3

from nin0lib.bot import Bot, Context
from nin0lib import Roles
from secret import secret_key

bot = Bot(prefix="i.",username="iambot")

@bot.command(aliases=["hi", "hello", "hola"])
async def hello(ctx: Context, name: str = None):
    if name == None:
        await ctx.send(f"Hello, {ctx.username}!")
        return
    await ctx.send("Hello, I'm iambot!")

@bot.command(name="sum")
async def _sum(ctx: Context, *nums: str):
    if len(nums) < 2:
        await ctx.send("I need at least 2 numbers to sum!")
        return
    try:
        nums_sum = sum(map(lambda x: int(x[:6]), nums))
    except ValueError:
        await ctx.send("I need numbers only to sum!")
        return
    await ctx.send(f"The sum of {', '.join(nums[:3]) + (', ...' if len(nums) > 3 else '')} is {nums_sum}")

@bot.command()
async def say(ctx, *, text: str):
    if ctx.username == "ayunami2000" and ctx.role == "discord":
        await ctx.send(text)
        return
    await ctx.send("nuh uh")

@bot.command(aliases=["8ball", "fortune"])
async def eightball(ctx, *, question: str):
    """ Fortune cookie style answers """
    import random
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "No",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


bot.run(secret_key)