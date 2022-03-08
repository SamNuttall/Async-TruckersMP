class BanAttributes:
    expiration = "expiration"
    time_added = "timeAdded"
    active = "active"
    reason = "reason"
    admin_name = "adminName"
    admin_id = "adminID"


class Ban:
    """
    A class object representing a ban on TruckersMP.

    .. _models_Ban:

    :ivar Optional[str] expiration: The expiration datetime of the ban.
    :ivar Optional[str] time_added: The datetime that the ban was added.
    :ivar Optional[bool] active: Whether the ban is considered active.
    :ivar Optional[str] reason: The reason for the ban.
    :ivar Optional[str] admin_name: The name of the admin that created the ban.
    :ivar Optional[str] admin_id: The TruckersMP ID of the admin that created the ban.
    """
    def __init__(self, ban):
        a = BanAttributes
        b = ban

        self.expiration = b[a.expiration]
        self.time_added = b[a.time_added]
        self.active = b[a.active]
        self.reason = b[a.reason]
        self.admin_name = b[a.admin_name]
        self.admin_id = b[a.admin_id]
