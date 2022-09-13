class EventsAttributes:
    featured = "featured"
    today = "today"
    now = "now"
    upcoming = "upcoming"


class EventAttributes:
    class EventType:
        key = "key"
        name = "name"

    class Server:
        id = "id"
        name = "name"

    class Depature:
        location = "location"
        city = "city"

    class Arrive:
        location = "location"
        city = "city"

    class VTC:
        id = "id"
        name = "name"

    class User:
        id = "id"
        username = "username"

    class Attendances:
        class Attendee:
            id = "id"
            username = "username"
            following = "following"
            created_at = "created_at"
            updated_at = "updated_at"

        confirmed = "confirmed"
        unsure = "unsure"
        confirmed_users = "confirmed_users"
        unsure_users = "unsure_users"

    id = "id"
    name = "name"
    slug = "slug"
    game = "game"
    language = "language"
    start_at = "start_at"
    banner = "banner"
    map = "map"
    description = "description"
    rule = "rule"
    voice_link = "voice_link"
    external_link = "external_link"
    featured = "featured"
    dlcs = "dlcs"
    url = "url"
    created_at = "created_at"
    updated_at = "updated_at"
    event_type = "event_type"
    server = "server"
    departure = "departure"
    arrive = "arrive"
    vtc = "vtc"
    user = "user"
    attendances = "attendances"


class Events:
    """
    A class object representing featured, todays, upcoming and now events.

    :ivar Optional[List[Event]] featured:
    :ivar Optional[List[Event]] today:
    :ivar Optional[List[Event]] upcoming:
    :ivar Optional[List[Event]] now:
    """
    def __init__(self, events):
        a = EventsAttributes
        e = events

        self.featured = e[a.featured]
        self.today = e[a.today]
        self.upcoming = e[a.upcoming]
        self.now = e[a.now]


class Event:
    """
    A class representing an event on TruckersMP

    :ivar Optional[int] id:
    :ivar Optional[str] name:
    :ivar Optional[str] slug:
    :ivar Optional[str] game:
    :ivar Optional[str] language:
    :ivar Optional[str] start_at:
    :ivar Optional[str] banner:
    :ivar Optional[str] map:
    :ivar Optional[str] description:
    :ivar Optional[str] rule:
    :ivar Optional[str] voice_link:
    :ivar Optional[str] external_link:
    :ivar Optional[str] featured:
    :ivar Optional[str] dlcs:
    :ivar Optional[list] url:
    :ivar Optional[str] created_at:
    :ivar Optional[str] updated_at:
    :ivar EventType event_type:
    :ivar Server server:
    :ivar Departure departure:
    :ivar Arrive arrive:
    :ivar VTC vtc:
    :ivar User user:
    :ivar Attendances attendances:
    """

    class EventType:
        """
        A class object representing a type of event

        :ivar Optional[str] key:
        :ivar Optional[str] name:
        """
        def __init__(self, event, attributes):
            e = event
            a = attributes
            t = a.EventType

            self.key = e[a.event_type][t.key]
            self.name = e[a.event_type][t.name]

    class Server:
        """
        A class object representing an event's server

        :ivar Optional[int] id:
        :ivar Optional[str] name:
        """
        def __init__(self, event, attributes):
            e = event
            a = attributes
            s = a.Server

            self.id = e[a.server][s.id]
            self.name = e[a.server][s.name]

    class Departure:
        """
        A class object representing an event's depature location

        :ivar Optional[str] location:
        :ivar Optional[str] city:
        """
        def __init__(self, event, attributes):
            e = event
            a = attributes
            d = a.Depature

            self.location = e[a.departure][d.location]
            self.city = e[a.departure][d.city]

    class Arrive:
        """
        A class object representing an event's destination

        :ivar Optional[str] location:
        :ivar Optional[str] city:
        """
        def __init__(self, event, attributes):
            e = event
            a = attributes
            ar = a.Arrive

            self.location = e[a.arrive][ar.location]
            self.city = e[a.arrive][ar.city]

    class VTC:
        """
        A class object representing an event's VTC

        :ivar Optional[int] id:
        :ivar Optional[str] name:
        """
        def __init__(self, event, attributes):
            e = event
            a = attributes
            vtc = a.VTC

            self.id = e[a.vtc][vtc.id]
            self.name = e[a.vtc][vtc.name]

    class User:
        """
        A class object representing the user (owner) of an event

        :ivar Optional[int] id:
        :ivar Optional[str] name:
        """
        def __init__(self, event, attributes):
            e = event
            a = attributes
            u = a.User

            self.id = e[a.user][u.id]
            self.username = e[a.user][u.username]

    class Attendances:
        """
        A class object representing attendance information of an event

        :ivar Optional[int] confirmed:
        :ivar Optional[List[Attendee]] unsure:
        """

        class Attendee:
            """
            A class object representing an attendee (user) of an event

            :ivar Optional[int] id:
            :ivar Optional[str] username:
            :ivar Optional[bool] following:
            :ivar Optional[str] created_at:
            :ivar Optional[str] updated_at:
            """
            def __init__(self, attendee, attributes):
                a = attendee
                at = attributes
                att = at.Attendances.Attendee

                self.id = a[att.id]
                self.username = a[att.username]
                self.following = a[att.following]
                self.created_at = a[att.created_at]
                self.updated_at = a[att.updated_at]

        def __init__(self, event, attributes):
            e = event
            a = attributes
            at = a.Attendances

            self.confirmed = e[a.attendances][at.confirmed]
            self.unsure = e[a.attendances][at.unsure]
            if at.confirmed_users in e[a.attendances]:
                confirmed_users = []
                for attendee in e[a.attendances][at.confirmed_users]:
                    confirmed_users.append(self.Attendee(attendee, a))
                self.confirmed_users = confirmed_users
            if at.unsure_users in e[a.attendances]:
                unsure_users = []
                for attendee in e[a.attendances][at.unsure_users]:
                    unsure_users.append(self.Attendee(attendee, a))
                self.unsure_users = unsure_users

    def __init__(self, event):
        a = EventAttributes
        e = event

        self.id = e[a.id]
        self.name = e[a.name]
        self.slug = e[a.slug]
        self.game = e[a.game]
        self.language = e[a.language]
        self.start_at = e[a.start_at]
        self.banner = e[a.banner]
        self.map = e[a.map]
        self.description = e[a.description]
        self.rule = e[a.rule]
        self.voice_link = e[a.voice_link]
        self.external_link = e[a.external_link]
        self.featured = e[a.featured]
        self.dlcs = e[a.dlcs]
        self.url = e[a.url]
        self.created_at = e[a.created_at]
        self.updated_at = e[a.updated_at]
        self.event_type = self.EventType(e, a)
        self.server = self.Server(e, a)
        self.departure = self.Departure(e, a)
        self.arrive = self.Arrive(e, a)
        self.vtc = self.VTC(e, a)
        self.user = self.User(e, a)
        self.attendances = self.Attendances(e, a)
