# Bot

The [Bot](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/bot.py#L33) class represents a bot that can connect to the server.

## Inheritance

The [Bot](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/bot.py#L33) class inherits from [`Client`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib.docs/client.md) and `CommandsManager`.

## Fields

### `prefix`: `str`

The prefix of the bot.

### `commands`: `Dict[str, BotCommand]`

The commands of the bot.

## Methods

### `__init__(self, *, prefix: str, default_help_command: asyncio.coroutine =None, **kwargs)`

`prefix`: the prefix of the bot
`default_help_command`: if None, it creates a default help command otherwise it's ignored

### `add_command(self, func: Callable, name: str = None, aliases: List[str] = None)`

Adds a command to the bot.

### `command(*args, **kw)`

The `command` decorator is used to register a function as a command in the class.

Here's an example of how to use the `command` decorator:

```python
@bot.command(aliases=["hi", "hello", "hola"])
async def hello(ctx: Context):
    await ctx.send("Hello, I'm coolBot!")
```

In this example, the `hello` function is decorated with `@bot.command`, which registers it as a command with `aliases`, `aliases` parameter is used to specify additional names that can be used to trigger the command.

When the bot receives a message starting with the command prefix (in this case, "c."), followed by the command name (e.g., "c.hello"), the `hello` function will be called with a `Context` object as the argument. The `Context` object contains information about the context in which the command was executed, such as the bot, the author, and any arguments passed to the command.

> [!NOTE]
> command decorator is a wrapper of the add_command

### `add_command(function: Callable, name:str=None, description:str=None, **kw)`

see `command(*args, **kw)`

### `remove_command(name: Callable | str)`

remove command by name or function name

### `command_exist(name: str)`

check if a command existst with its name

### `run(self, token: str, logger_level: int = logging.INFO)`

Runs the bot.

## Example

```python
bot = Bot(prefix="!")

@bot.event
async def on_ready():
    print("logged in as", bot.username)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")


bot.run("my_token")
```

> [!WARNING]
> those aren't all the class methods, you can check the code for more information or methods
