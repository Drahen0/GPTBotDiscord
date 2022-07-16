import aiohttp

from dataclasses import dataclass

PROMPT = """
Le texte suivant est une conversation entre les membres d'un serveur et un BOT.
Le BOT parle comme un robot et se fait passer pour un humain. Il n'arrive pas à cacher qu'il est un BOT.

{}
{}
BOT:"""


@dataclass
class Message:
    username: str
    content: str

    @property
    def text(self):
        return f"{self.username}: {self.content}"

    @property
    def prompt(self):
        return f" {self.username}:"


brain: list[tuple[Message, str]] = []


async def callopenai(api_key: str, message: Message):
    if len(brain) == 0:
        memory = f"{message.username}: Bonjour\BOT: Bonjour, comment puis-je t'aider ?"
    else:
        memory = "\n".join(
            f"{msg.text}\BOT: {response}" for msg, response in brain
        )

    users = [" BOT:", *(msg.prompt for msg, _ in brain)]
    users.append(message.prompt)

    print(PROMPT.format(memory, message.text))
    print(list(set(users)))

    data = {
        "model": "text-davinci-002",
        "prompt": PROMPT.format(memory, message.text),
        "temperature": 0.9,
        "max_tokens": 150,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.6,
        "stop": list(set(users)),
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    url = "https://api.openai.com/v1/completions"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=data) as resp:
            data = await resp.json()
            response = data["choices"][0]["text"]
            brain.append((message, response.strip()))

            if len(brain) > 5:
                brain.pop(0)

            return response
