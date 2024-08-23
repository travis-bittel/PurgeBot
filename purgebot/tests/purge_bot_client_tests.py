from discord import Member
from unittest.mock import patch, PropertyMock, AsyncMock

import discord
import unittest

from unittest import IsolatedAsyncioTestCase

from purgebot.src.KickConditions import KickCondition
from purgebot.src.Settings import Settings
from purgebot.src.bot import PurgeBotClient

intents = discord.Intents.default()
intents.members = True


class TestKickCondition(KickCondition):
    def member_should_be_kicked(self, member: Member) -> bool:
        return True


class TestSettings(Settings):
    KICK_MESSAGE: str = 'Test kick message'
    KICK_REASON: str = 'Test kick reason'
    AUDIT_LOG_CHANNEL_ID: int = 1234

    exempt_role_ids = [1234]
    KICK_CONDITION: KickCondition = TestKickCondition()


class BotTestCase(unittest.TestCase):
    @patch('purgebot.src.bot.PurgeBotClient.kick_members_matching_condition')
    @patch('discord.client.Client.run')
    def test_calls_kick_members_matching_condition_on_ready(self, kick_members_matching_condition, client_run):
        client = PurgeBotClient(intents=intents, kick_bot_settings=TestSettings())
        client.run('SECRET TOKEN')
        self.assertTrue(kick_members_matching_condition.called)

    @patch('discord.client.Client.run')
    @patch('discord.client.Client.close')
    def test_shuts_down_after_performing_kicks(self, run, close):
        client = PurgeBotClient(intents=intents, kick_bot_settings=TestSettings())
        client.run('SECRET TOKEN')
        self.assertTrue(close.called)


class Test(IsolatedAsyncioTestCase):
    async def test_kick_members_matching_condition(self):
        mock_guild = AsyncMock()
        mock_member = AsyncMock()
        mock_guild.members = [mock_member]

        with patch('purgebot.src.bot.PurgeBotClient.guilds', new=PropertyMock(return_value=[mock_guild])):
            client = PurgeBotClient(intents=intents, kick_bot_settings=TestSettings())
            await client.kick_members_matching_condition()
            self.assertTrue(mock_member.send.called)
            self.assertTrue(mock_member.kick.called)


if __name__ == '__main__':
    unittest.main()
