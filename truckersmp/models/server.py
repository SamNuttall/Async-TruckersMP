class ServerAttributes:
    """Stores the attributes of a server"""
    id = "id"  # int
    game = "game"  # str
    ip = "ip"  # str
    port = "port"  # int
    name = "name"  # str
    short_name = "shortname"  # str
    id_prefix = "idprefix"  # str
    online = "online"  # bool
    players = "players"  # int
    queue = "queue"  # int
    max_players = "maxplayers"  # int
    map_id = "mapid"  # int
    display_order = "displayorder"  # int
    speed_limiter = "speedlimiter"  # int
    collisions = "collisions"  # bool
    cars_for_players = "carsforplayers"  # bool
    police_cars_for_players = "policecarsforplayers"  # bool
    afk_enabled = "afkenabled"  # bool
    event = "event"  # bool
    special_event = "specialEvent"  # bool
    promods = "promods"  # bool
    sync_delay = "syncdelay"  # int


class Server:
    """
    A class object representing a TruckersMP server

    :ivar Optional[int] id: The ID of the server
    :ivar Optional[str] game: The game of the server
    :ivar Optional[str] ip: The IP address of the server
    :ivar Optional[int] port: The port of the server
    :ivar Optional[str] name: The server name
    :ivar Optional[strr] short_name: The server's shortname
    :ivar Optional[str] id_prefix: A string that is inserted in front of an in-game user's ID.
    :ivar Optional[bool] online: Whether the server is online
    :ivar Optional[int] players: The number of players in the server
    :ivar Optional[int] queue: The number of players in the server's queue
    :ivar Optional[int] max_players: The maximum number of players allowed in the server
    :ivar Optional[int] map_id: The map ID of the server
    :ivar Optional[int] display_order: Where the server is displayed in the list
    :ivar Optional[int] speed_limiter: Whether the speed limiter is enabled
    :ivar Optional[str] collisions: Whether collisions are enabled
    :ivar Optional[str] cars_for_players: Whether players are allowed to drive cars
    :ivar Optional[str] afk_enabled: Whether AFK kick is enabled
    :ivar Optional[str] event: Whether this is an event server
    :ivar Optional[str] special_event: Whether this is a special event server
    :ivar Optional[str] promods: Whether Promods is enabled on this server
    :ivar Optional[int] sync_delay:
    """
    def __init__(self, server):
        a = ServerAttributes
        s = server

        self.id = s[a.id]
        self.game = s[a.game]
        self.ip = s[a.ip]
        self.port = s[a.port]
        self.name = s[a.name]
        self.short_name = s[a.short_name]
        self.id_prefix = s[a.id_prefix]
        self.online = s[a.online]
        self.players = s[a.players]
        self.queue = s[a.queue]
        self.max_players = s[a.max_players]
        self.map_id = s[a.map_id]
        self.display_order = s[a.display_order]
        self.speed_limiter = s[a.speed_limiter]
        self.collisions = s[a.collisions]
        self.cars_for_players = s[a.cars_for_players]
        self.afk_enabled = s[a.afk_enabled]
        self.event = s[a.event]
        self.special_event = s[a.special_event]
        self.promods = s[a.promods]
        self.sync_delay = s[a.sync_delay]
