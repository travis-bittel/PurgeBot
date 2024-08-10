import boto3
import discord
from discord import Member, Guild

AUDIT_LOG_CHANNEL_ID = 1259178106493599774


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Client {self.user} started')

        for guild in self.guilds:
            kicked_member_names = []
            for member in guild.members:
                if member_should_be_kicked(member):
                    kicked_member_names.append(member.name)
                    await kick_member(member, guild)
            if kicked_member_names:
                try:
                    audit_log_message = '**Removed Users:**\n'
                    for name in kicked_member_names:
                        audit_log_message += f'* {name}\n'
                    await self.get_channel(AUDIT_LOG_CHANNEL_ID).send(audit_log_message)
                except Exception as e:
                    print(f'Failed to send audit log message: {e}')

        print(f'Closing client {self.user}')
        await self.close()


def member_should_be_kicked(member: Member) -> bool:
    """Returns true if the user should be purged, false otherwise"""
    exempt_role_ids = [1259957158561185913, 1250842605655167077, 1250885105745006725, 1250842658398535742,
                       1261020095585583125, 1251278632479887540, 762142478110687302, 1258909892308107349,
                       1258917482710831149, 1250941261809061891, 1270395216527888448, 1271607035258998860]
    return not any(role.id in exempt_role_ids for role in member.roles)


async def kick_member(member: Member, guild: Guild):
    """Kicks the member and sends them a message notifying them."""
    try:
        await member.send(f'You have been removed from {guild.name} as you are not longer a subscriber. '
                          'Please let us know if this is incorrect!')
    except Exception as e:
        print(f'Failed to send message to user: {e}')
    await member.kick(reason='Kicked for not having a Patreon or other allowed role.')
    print(f'Kicked {member.name}')


intents = discord.Intents.default()
intents.members = True

ssm_client = boto3.client('ssm')
discord_secret_token = ssm_client.get_parameter(Name='purgebot-discord-secret', WithDecryption=True)['Parameter']['Value']


def lambda_handler(event, context):
    discord_client = MyClient(intents=intents)
    discord_client.run(discord_secret_token)
