class PlayerAttributes:
    class Patreon:
        is_patron = "isPatron"
        active = "active"
        color = "color"
        tier_id = "tierId"
        current_pledge = "currentPledge"
        lifetime_pledge = "lifetimePledge"
        next_pledge = "nextPledge"
        hidden = "hidden"

    class Permissions:
        is_staff = "isStaff"
        is_upper_staff = "isUpperStaff"
        is_game_admin = "isGameAdmin"
        show_detailed_on_web_maps = "showDetailedOnWebMaps"

    class VTC:
        id = "id"
        name = "name"
        tag = "tag"
        in_vtc = "inVTC"
        member_id = "memberID"

    id = "id"  # int
    name = "name"  # str
    avatar = "avatar"  # str
    small_avatar = "smallAvatar"  # str
    join_date = "joinDate"  # str
    steam_id_64 = "steamID64"  # int
    steam_id = "steamID"
    discord_id = "discordSnowflake"
    display_vtc_history = "displayVTCHistory"
    group_name = "groupName"
    group_color = "groupColor"
    group_id = "groupID"
    banned = "banned"
    banned_until = "bannedUntil"
    ban_count = "bansCount"
    display_bans = "displayBans"
    patreon = "patreon"
    permissions = "permissions"
    vtc = "vtc"


class Player:
    """
    A class object representing a TruckersMP player (user)

    :ivar Optional[int ] id:
    :ivar Optional[str] name:
    :ivar Optional[str] avatar:
    :ivar Optional[str] small_avatar:
    :ivar Optional[str] join_date:
    :ivar Optional[int] steam_id_64:
    :ivar Optional[str] steam_id:
    :ivar Optional[str] discord_id:
    :ivar Optional[bool] display_vtc_history:
    :ivar Optional[str] group_name:
    :ivar Optional[str] group_color:
    :ivar Optional[str] group_colour:
    :ivar Optional[int] group_id:
    :ivar Optional[bool] banned:
    :ivar Optional[str] banned_until:
    :ivar Optional[int] ban_count:
    :ivar Optional[bool] display_bans:
    :ivar Patreon patreon:
    :ivar Permissions permissions:
    :ivar VTC vtc:
    """

    class Patreon:
        """
        A class object representing Patreon information about a player

        :ivar Optional[bool] is_patron:
        :ivar Optional[bool] active:
        :ivar Optional[str] color:
        :ivar Optional[int] tier_id:
        :ivar Optional[int] current_pledge:
        :ivar Optional[int] lifetime_pledge:
        :ivar Optional[int] next_pledge:
        :ivar Optional[bool] hidden:
        """
        def __init__(self, player, attributes):
            pl = player
            a = attributes
            p = a.Patreon

            self.is_patron = pl[a.patreon][p.is_patron]
            self.active = pl[a.patreon][p.active]
            self.color = pl[a.patreon][p.color]
            self.tier_id = pl[a.patreon][p.tier_id]
            self.current_pledge = pl[a.patreon][p.current_pledge]
            self.lifetime_pledge = pl[a.patreon][p.lifetime_pledge]
            self.next_pledge = pl[a.patreon][p.next_pledge]
            self.hidden = pl[a.patreon][p.hidden]

    class Permissions:
        """
        A class object representing the permissions of a player

        :ivar Optional[bool] is_staff:
        :ivar Optional[bool] is_upper_staff:
        :ivar Optional[bool] is_game_admin:
        :ivar Optional[bool] show_detailed_on_maps:
        """
        def __init__(self, player, attributes):
            pl = player
            a = attributes
            p = a.Permissions

            self.is_staff = pl[a.permissions][p.is_staff]
            self.is_upper_staff = pl[a.permissions][p.is_upper_staff]
            self.is_game_admin = pl[a.permissions][p.is_game_admin]
            self.show_detailed_on_maps = pl[a.permissions][p.show_detailed_on_web_maps]

    class VTC:
        """
        A class object representing the VTC of a player

        :ivar Optional[int] id:
        :ivar Optional[str] name:
        :ivar Optional[str] tag:
        :ivar Optional[bool] in_vtc:
        :ivar Optional[int] member_id:
        """
        def __init__(self, player, attributes):
            pl = player
            a = attributes
            vtc = a.VTC

            self.id = pl[a.vtc][vtc.id]
            self.name = pl[a.vtc][vtc.name]
            self.tag = pl[a.vtc][vtc.tag]
            self.in_vtc = pl[a.vtc][vtc.in_vtc]
            self.member_id = pl[a.vtc][vtc.member_id]

    def __init__(self, player):
        a = PlayerAttributes
        p = player

        self.id = p[a.id]
        self.name = p[a.name]
        self.avatar = p[a.avatar]
        self.small_avatar = p[a.small_avatar]
        self.join_date = p[a.join_date]
        self.steam_id_64 = p[a.steam_id_64]
        self.steam_id = p[a.steam_id]
        self.discord_id = p[a.discord_id]
        self.display_vtc_history = p[a.display_vtc_history]
        self.group_name = p[a.group_name]
        self.group_color = p[a.group_color]
        self.group_colour = p[a.group_color]
        self.group_id = p[a.group_id]
        self.banned = p[a.banned]
        self.banned_until = p[a.banned_until]
        self.ban_count = p[a.ban_count]
        self.display_bans = p[a.display_bans]
        self.patreon = self.Patreon(p, a)
        self.permissions = self.Permissions(p, a)
        self.vtc = self.VTC(p, a)
