from typing import Any

from discord import Member, Guild, Client, Intents

from purgebot.src.Settings import Settings


class PurgeBotClient(Client):
    """
    This bot is designed to be run on a periodic schedule to kick all users meeting a specified condition.

    When started, the bot client scans all guilds in which it is a member and applies the KICK_CONDITION specified in
    Settings to each member of that guild. If the member meets the criteria for being kicked, the bot kicks them.

    After kicking all members meeting the condition, the bot posts an audit message to the channel with the
    AUDIT_LOG_CHANNEL_ID listing the members that were kicked.

    The bot then shuts down.
    """
    def __init__(self, kick_bot_settings: Settings, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self.settings = kick_bot_settings

    async def on_ready(self):
        print(f'Client {self.user} started')
        await self.kick_members_matching_condition()

        print(f'Closing client {self.user}')
        await self.close()

    async def kick_members_matching_condition(self):
        for guild in self.guilds:
            kicked_member_names = []
            for member in guild.members:
                if self.settings.KICK_CONDITION.member_should_be_kicked(member):
                    kicked_member_names.append(member.name)
                    await self.kick_member(member, guild)
            if kicked_member_names:
                try:
                    audit_log_message = '**Removed Users:**\n'
                    for name in kicked_member_names:
                        audit_log_message += f'* {name}\n'
                    await self.get_channel(self.settings.AUDIT_LOG_CHANNEL_ID).send(audit_log_message)
                except Exception as e:
                    print(f'Failed to send audit log message: {e}')

    async def kick_member(self, member: Member, guild: Guild):
        """Kicks the member and sends them a message notifying them."""
        try:
            await member.send(self.settings.KICK_MESSAGE.format(guild.name))
        except Exception as e:
            print(f'Failed to send message to user: {e}')
        await member.kick(reason=self.settings.KICK_REASON)
        print(f'Kicked {member.name}')
