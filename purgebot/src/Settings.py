from purgebot.src.KickConditions import KickCondition, DoesNotHaveRoleKickCondition


class Settings:
    KICK_MESSAGE: str = ('You have been removed from {} as you are no longer a subscriber. Thank you for '
                         'your support! We hope you enjoyed your stay. You can always be re-invited after choosing '
                         'the tier that best fits you. If there was a problem, please let us know by contacting '
                         'admins/mods!')
    KICK_REASON: str = 'Kicked for not having a Patreon or other allowed role.'
    AUDIT_LOG_CHANNEL_ID: int = 1259178106493599774

    exempt_role_ids = [1259957158561185913, 1250842605655167077, 1250885105745006725, 1250842658398535742,
                       1261020095585583125, 1251278632479887540, 762142478110687302, 1258909892308107349,
                       1258917482710831149, 1250941261809061891, 1270395216527888448, 1271607035258998860]
    KICK_CONDITION: KickCondition = DoesNotHaveRoleKickCondition(exempt_role_ids)
