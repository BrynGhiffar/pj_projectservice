from discord import Webhook
import asyncio
import aiohttp

class DiscordApi:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send_message_async(self, message: str):
        WEBHOOK = self.webhook_url
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(WEBHOOK, session=session)
            await webhook.send(message)

    def send_message(self, message: str) -> None:
        asyncio.run(self.send_message_async(message))