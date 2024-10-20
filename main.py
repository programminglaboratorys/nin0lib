from nin0lib.bot import Bot, Context, create_context
from nin0lib import Roles, Message
from secret import secret_key

import aiohttp
import base64
import re


bot = Bot(prefix="i.",username="iambot")

@bot.command(aliases=["hi", "hello", "hola"])
async def hello(ctx: Context, name: str = None):
    if name == None:
        await ctx.send(f"Hello, {ctx.username}!")
        return
    await ctx.send(f"Hello, I'm {bot.username}!")

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
    await ctx.send(text)

@bot.command(aliases=["8ball", "fortune", "eightball"])
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
@bot.command(aliases=["sc", "source", "code"])
async def source_code(ctx , *_):
    await ctx.send("<https://github.com/programminglaboratorys/nin0lib>")

def find_crosspending_emoji(code, returncode):
    if not code:
        return ":warning:"
    if returncode == 0:  # No error
        return ":white_check_mark:"
    # Exception
    return ":x:"

def format_message(code, returncode):
    return find_crosspending_emoji(code, returncode) + \
        (f" Your 3.12 eval job has completed with return code {returncode}.")

async def special_eval(ctx, code):
    rq = {
        "args": ["main.py"],
	    "files": [
            {
                "path": "main.py",
                "content": base64.b64encode(code.encode()).decode()
            }
        ]
    }


    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8060/eval", json=rq) as resp:
            data = await resp.json()
            print("eval job by ", ctx.username, "executing code:", data)
            message = find_crosspending_emoji(code, data["returncode"]) + f" Your 3.12 eval job has completed with return code {data['returncode']}."
            message += "```"
            message += data["stdout"] if data["stdout"] else "[No output]"
            message += "```"
            await ctx.send(message)

@bot.command(name="eval")
async def _eval(ctx, *, code: str):
    code = code.strip("\n").strip("`")
    if (match:=re.match("py(thon)?\n", code)) is not None:
        code = code[match.span(0)[1]:]
        #code = "\n".join(code.split("\n")[1:])
    if not code.strip("\n"):
        await ctx.send("Please provide a code to eval")
        return

    if not re.search(  # Check if it's an expression
            r"^(return|import|for|while|def|class|"
            r"from|exit|[a-zA-Z0-9]+\s*=)", code, re.M) and len(
                code.split("\n")) == 1:
        code = "_ = " + code
    await special_eval(ctx, code)


bot.run(secret_key)