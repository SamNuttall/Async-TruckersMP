class RulesAttributes:
    rules = "rules"
    revision = "revision"


class Rules:
    """
    A class object representing TruckersMP rules.

    :ivar optional[str] rules:
    :ivar optional[int] revision:
    """
    def __init__(self, rules):
        a = RulesAttributes
        r = rules

        self.rules = r[a.rules]
        self.revision = r[a.revision]
