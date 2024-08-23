import boto3
import discord

from purgebot.src.Settings import Settings
from purgebot.src.bot import PurgeBotClient

intents = discord.Intents.default()
intents.members = True

ssm_client = boto3.client('ssm')
discord_secret_token \
    = ssm_client.get_parameter(Name='purgebot-discord-secret', WithDecryption=True)['Parameter']['Value']


def lambda_handler(event, context):
    discord_client = PurgeBotClient(intents=intents, kick_bot_settings=Settings())
    discord_client.run(discord_secret_token)
