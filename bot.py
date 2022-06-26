import discord
from api import callopenai, Message

with open(".env", "r") as f:
    dotenv = dict(
        line.split("=")
        for line in f.read().splitlines(False)
        if not line.lstrip().startswith("#")
    )


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: discord.Message):
        print(f"Message from {message.author}: {message.content}")

        if message.author.bot:
            return

        channel: discord.TextChannel = message.channel
        async with channel.typing():
            answer = await callopenai(
                dotenv.get("GPT3_API_KEY"),
                Message(message.author.display_name, message.content),
            )
            await message.reply(answer)


client = MyClient(intents=discord.Intents.all())
client.run(dotenv.get("DISCORD_TOKEN", ""))
