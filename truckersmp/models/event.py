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

    :ivar Optional[List[Event]] featured: Events featured by TruckersMP
    :ivar Optional[List[Event]] today: Events that are starting today
    :ivar Optional[List[Event]] upcoming: Events that are starting soonest, but not today
    :ivar Optional[List[Event]] now: Events that are happening right now
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

    :ivar Optional[int] id: The event ID
    :ivar Optional[str] name: The name of the event
    :ivar Optional[str] slug: The event slug (present in the URL)
    :ivar Optional[str] game: The game which the event takes place on
    :ivar Optional[str] language: The primary language for the event
    :ivar Optional[str] start_at: The starting time of the event
    :ivar Optional[str] banner: An image URL of the event banner
    :ivar Optional[str] map: An image URL of the event map
    :ivar Optional[str] description: The event description
    :ivar Optional[str] rule: The event rules
    :ivar Optional[str] voice_link: A link to the event's communication platform (eg. Discord server)
    :ivar Optional[str] external_link: A link to the event's website (or listing)
    :ivar Optional[str] featured: If featured, equals "Featured"
    :ivar Optional[list] dlcs: List of DLCs required
    :ivar Optional[list] url: Link to the event on TruckersMP (only path)
    :ivar Optional[str] created_at: When the event was created
    :ivar Optional[str] updated_at: When the event was last updated
    :ivar EventType event_type: The type of event
    :ivar Server server: The server the event will take place on
    :ivar Departure departure: The departure location
    :ivar Arrive arrive: The desination location
    :ivar VTC vtc: The VTC the event is organised by
    :ivar User user: The user the event is organised by
    :ivar Attendances attendances: The users that plan to attend
    """

    class EventType:
        """
        A class object representing a type of event

        :ivar Optional[str] key:
        :ivar Optional[str] name: The name of the event type
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

        :ivar Optional[int] id: The ID of the event's server
        :ivar Optional[str] name: The name of the event's server
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

        :ivar Optional[str] location: The location in the departure city (eg. garage)
        :ivar Optional[str] city: The depature city name
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

        :ivar Optional[str] location: The location in the arrival city (eg. garage)
        :ivar Optional[str] city: The arrival city name
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

        :ivar Optional[int] id: The ID of the host VTC
        :ivar Optional[str] name: The name of the host VTC
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

        :ivar Optional[int] id: The ID of the host user
        :ivar Optional[str] name: The name of the host user
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

        :ivar Optional[int] confirmed: The number of users that have confirmed their attendance
        :ivar Optional[int] unsure: The number of users that are unsure if they can make it
        :ivar Optional[List[Attendee]] confirmed_users: List of confirmed users
        :ivar Optional[List[Attendee]] unsure__users: List of unsure users
        """

        class Attendee:
            """
            A class object representing an attendee (user) of an event

            :ivar Optional[int] id: The ID of the user
            :ivar Optional[str] username: The name of the user
            :ivar Optional[bool] following:
            :ivar Optional[str] created_at: When the user confirmed their attendance
            :ivar Optional[str] updated_at: When the user updated their attendance
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
