#!/usr/bin/env nix-shell
#!nix-shell -p python3 python3Packages.websockets -i python3

from nin0lib.bot import Bot, Context
from secret import secret_key

bot = Bot(prefix="c.",username="coolBot")

@bot.command(aliases=["hi", "hello", "hola"])
async def hello(ctx: Context):
    await ctx.send("Hello, I'm coolBot!")

@bot.command()
async def sum(ctx: Context, n1: str, n2: str):
    if len(n1) > 128 or len(n2) > 128:
        await ctx.send("The numbers are too big!")
        return
    try:
        n1 = int(n1)
        n2 = int(n2)
    except ValueError:
        await ctx.send("I need two numbers to sum!")
        return
    await ctx.send(f"The sum of {n1} and {n2} is {n1+n2}")

bot.run(secret_key)



"""
async def main():
    async with Client(username="coolBot", key=secret_key) as client:
        await client.send("Hello, World 2! :)")

if __name__ == "__main__":
    asyncio.run(main())
"""