class VersionAttributes:
    class ETS2MPChecksum:
        dll = "dll"
        adb = "adb"

    class ATSMPChecksum:
        dll = "dll"
        adb = "adb"

    name = "name"
    numeric = "numeric"
    stage = "stage"
    time = "time"
    supported_game_version = "supported_game_version"
    supported_ats_game_version = "supported_ats_game_version"
    ets2mp_checksum = "ets2mp_checksum"
    atsmp_checksum = "atsmp_checksum"


class Version:
    """
    A class object to represent a TruckersMP version.

    :ivar Optional[str] name:
    :ivar Optional[str] numeric:
    :ivar Optional[str] stage:
    :ivar Optional[str] time:
    :ivar Optional[str] supported_game_version:
    :ivar Optional[str] supported_ats_version:
    :ivar :class:`ETS2MPChecksum <models.version.Version.ETS2MPChecksum>` ets2mp_checksum:
    :ivar :class:`ATSMPChecksum <models.version.Version.ATSMPChecksum>` atsmp_checksum:
    """
    class ETS2MPChecksum:
        """
        A class object to represent the ETS2MP Checksum in a version

        :ivar Optional[str] dll:
        :ivar Optional[str] adb:
        """
        def __init__(self, version, attributes):
            v = version
            a = attributes
            ac = a.ETS2MPChecksum

            self.dll = v[a.ets2mp_checksum][ac.dll]
            self.adb = v[a.ets2mp_checksum][ac.adb]

    class ATSMPChecksum:
        """
        A class object to represent the ATSMP Checksum in a version

        :ivar Optional[str] dll:
        :ivar Optional[str] adb:
        """
        def __init__(self, version, attributes):
            v = version
            a = attributes
            ac = a.ATSMPChecksum

            self.dll = v[a.atsmp_checksum][ac.dll]
            self.adb = v[a.atsmp_checksum][ac.adb]

    def __init__(self, version):
        a = VersionAttributes
        v = version

        self.name = v[a.name]
        self.numeric = v[a.numeric]
        self.stage = v[a.stage]
        self.time = v[a.time]
        self.supported_game_version = v[a.supported_game_version]
        self.supported_ats_version = v[a.supported_ats_game_version]
        self.ets2mp_checksum = self.ETS2MPChecksum(v, a)
        self.atsmp_checksum = self.ATSMPChecksum(v, a)
