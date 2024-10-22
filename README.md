# commandkit

easy tool to parse string to commands and an easy tool to create commandlines

# nin0lib

create nin0chat bots with python!
simple and easy to setup library for https://chat.nin0.dev/

## install

```cmd
pip install .
```

## example

```py
from nin0lib.bot import Bot, Context

bot = Bot(prefix="c.")

@bot.event
async def on_ready():
    print("logged in as", bot.username) # logged in as coolBot

@bot.command(aliases=["hi", "hello", "hola"])
async def hello(ctx: Context):
    await ctx.send(f"Hello, I'm {bot.username}!")

@bot.command()
async def sum(ctx: Context, n1: int, n2: int):
    await ctx.send(f"The sum of {n1} and {n2} is {n1+n2}")

bot.run("token")
```

> [!NOTE]
> replace token with your bot token!

check the docs at [nin0.docs](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib.docs/README.md)
