from discord import Member


class KickCondition:
    def member_should_be_kicked(self, member: Member) -> bool:
        pass


class DoesNotHaveRoleKickCondition(KickCondition):
    def __init__(self, exempt_role_ids: [int]):
        """
        :param exempt_role_ids: The user will not be kicked if they have any of the roles in this list
        """
        self.exempt_role_ids = exempt_role_ids

    def member_should_be_kicked(self, member: Member) -> bool:
        return not any(role.id in self.exempt_role_ids for role in member.roles)
