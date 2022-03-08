class VTCsAttributes:
    recent = "recent"
    featured = "featured"
    featured_cover = "featured_cover"


class VTCAttributes:
    class Socials:
        twitter = "twitter"
        facebook = "facebook"
        twitch = "twitch"
        discord = "discord"
        youtube = "youtube"

    class Games:
        ats = "ats"
        ets = "ets"

    id = "id"
    name = "name"
    owner_id = "owner_id"
    owner_username = "owner_username"
    slogan = "slogan"
    tag = "tag"
    logo = "logo"
    cover = "cover"
    information = "information"
    rules = "rules"
    requirements = "requirements"
    website = "website"
    members_count = "members_count"
    recruitment = "recruitment"
    language = "language"
    verified = "verified"
    validated = "validated"
    created = "created"
    socials = "socials"
    games = "games"


class NewsPostAttributes:
    id = "id"
    title = "title"
    content_summary = "content_summary"
    content = "content"
    author_id = "author_id"
    author = "author"
    pinned = "pinned"
    updated_at = "updated_at"
    published_at = "published_at"


class RoleAttributes:
    id = "id"
    name = "name"
    order = "order"
    owner = "owner"
    created_at = "created_at"
    updated_at = "updated_at"


class MemberAttributes:
    id = "id"
    user_id = "user_id"
    username = "username"
    steam_id = "steam_id"
    role_id = "role_id"
    role = "role"
    join_date = "joinDate"


class VTCs:
    """
    A class object representing recent, featured and featured cover VTCs.

    :ivar Optional[List[:class:`VTC <models.vtc.VTC>`]] recent:
    :ivar Optional[List[:class:`VTC <models.vtc.VTC>`]] featured:
    :ivar Optional[List[:class:`VTC <models.vtc.VTC>`]] featured_cover:
    """
    def __init__(self, vtcs):
        a = VTCsAttributes

        self.recent = vtcs[a.recent]
        self.featured = vtcs[a.featured]
        self.featured_cover = vtcs[a.featured_cover]


class VTC:
    """
    A class object representing a VTC.

    :ivar Optional[int] id:
    :ivar Optional[str] name:
    :ivar Optional[int] owner_id:
    :ivar Optional[str] owner_username:
    :ivar Optional[str] slogan:
    :ivar Optional[str] tag:
    :ivar Optional[str] logo:
    :ivar Optional[str] cover:
    :ivar Optional[str] information:
    :ivar Optional[str] rules:
    :ivar Optional[str] requirements:
    :ivar Optional[str] website:
    :ivar Optional[int] members_count:
    :ivar Optional[str] recruitment:
    :ivar Optional[str] language:
    :ivar Optional[bool] verified:
    :ivar Optional[bool] validated:
    :ivar Optional[str] created:
    :ivar :class:`Socials <models.vtc.VTC.Socials>` socials:
    :ivar :class:`Games <models.vtc.VTC.Games>` games:
    """
    class Socials:
        """
        A class object respresenting a VTC's socials.

        :ivar Optional[str] twitter:
        :ivar Optional[str] facebook:
        :ivar Optional[str] twitch:
        :ivar Optional[str] discord:
        :ivar Optional[str] youtube:
        """
        def __init__(self, vtc, attributes):
            a = attributes
            s = a.Socials

            self.twitter = vtc[a.socials][s.twitter]
            self.facebook = vtc[a.socials][s.facebook]
            self.twitch = vtc[a.socials][s.twitch]
            self.discord = vtc[a.socials][s.discord]
            self.youtube = vtc[a.socials][s.youtube]

    class Games:
        """
        A class object representing a VTC's games.

        :ivar Optional[bool] ats:
        :ivar Optional[bool] ets:
        """
        def __init__(self, vtc, attributes):
            a = attributes
            g = a.Games

            self.ats = vtc[a.games][g.ats]
            self.ets = vtc[a.games][g.ets]

    def __init__(self, vtc):
        a = VTCAttributes

        self.id = vtc[a.id]
        self.name = vtc[a.name]
        self.owner_id = vtc[a.owner_id]
        self.owner_username = vtc[a.owner_username]
        self.slogan = vtc[a.slogan]
        self.tag = vtc[a.tag]
        self.logo = vtc[a.logo] if a.logo in vtc else None
        self.cover = vtc[a.cover] if a.cover in vtc else None
        self.information = vtc[a.information] if a.information in vtc else None
        self.rules = vtc[a.rules] if a.rules in vtc else None
        self.requirements = vtc[a.requirements] if a.requirements in vtc else None
        self.website = vtc[a.website]
        self.members_count = vtc[a.members_count]
        self.recruitment = vtc[a.recruitment]
        self.language = vtc[a.language]
        self.verified = vtc[a.verified]
        self.validated = vtc[a.validated]
        self.created = vtc[a.created]
        self.socials = self.Socials(vtc, a)
        self.games = self.Games(vtc, a)


class NewsPost:
    """
    A class representing a VTC news post.

    :ivar Optional[int] id:
    :ivar Optional[str] title:
    :ivar Optional[str] content_summary:
    :ivar Optional[str] content:
    :ivar Optional[int] author_id:
    :ivar Optional[str] author:
    :ivar Optional[bool] pinned:
    :ivar Optional[str] updated_at:
    :ivar Optional[str] published_at:
    """
    def __init__(self, news_post):
        a = NewsPostAttributes
        p = news_post

        self.id = p[a.id]
        self.title = p[a.title]
        self.content_summary = p[a.content_summary]
        self.content = p[a.content] if a.content in p else None
        self.author_id = p[a.author_id]
        self.author = p[a.author]
        self.pinned = p[a.pinned]
        self.updated_at = p[a.updated_at]
        self.published_at = p[a.published_at]


class Role:
    """
    A class object representing a VTC role.

    :ivar Optional[int] id:
    :ivar Optional[str] name:
    :ivar Optional[int] order:
    :ivar Optional[bool] owner: Whether the role is the owner role (highest rank)
    :ivar Optional[str] created_at:
    :ivar Optional[str] updated_at:
    """
    def __init__(self, role):
        a = RoleAttributes
        r = role

        self.id = r[a.id]
        self.name = r[a.name]
        self.order = r[a.order]
        self.owner = r[a.owner]
        self.created_at = r[a.created_at]
        self.updated_at = r[a.updated_at]


class Member:
    """
    A class object representing a VTC Member.

    :ivar Optional[int] id:
    :ivar Optional[int] user_id:
    :ivar Optional[str] username:
    :ivar Optional[int] steam_id:
    :ivar Optional[int] role_id:
    :ivar Optional[str] role:
    :ivar Optional[str] join_date:
    """
    def __init__(self, member):
        a = MemberAttributes
        m = member

        self.id = m[a.id]
        self.user_id = m[a.user_id]
        self.username = m[a.username]
        self.steam_id = m[a.steam_id]
        self.role_id = m[a.role_id]
        self.role = m[a.role]
        self.join_date = m[a.join_date]
