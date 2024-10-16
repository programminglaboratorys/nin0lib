# commandkit

easy tool to parse string to commands and an easy tool to create commandlines

# nin0lib

create nin0chat bots with python!

## install

```cmd
pip install .
```

## example

```py
from nin0lib.bot import Bot, Context
from secret import secret_key

bot = Bot(prefix="c.",username="coolBot")

@bot.command(aliases=["hi", "hello", "hola"])
async def hello(ctx: Context):
    await ctx.send("Hello, I'm coolBot!")

@bot.command()
async def sum(ctx: Context, n1: int, n2: int):
    await ctx.send(f"The sum of {n1} and {n2} is {n1+n2}")

bot.run(secret_key)
```

> [!NOTE]
> replace secret_key with your key!
