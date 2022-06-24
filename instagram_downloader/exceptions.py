class InstagramRateLimit(Exception):
    def __init__(self, after: str = ""):
        self.__after = after

    @property
    def after(self):
        return self.__after

    def __str__(self):
        return "Instagram ratelimited your IP address. The current cursor : {}".format(self.__after)

class ContextCorrupted(Exception):
    def __str__(self):
        return "The context was corrupted. Any kind of modification is prohibited."

class ContextInvalidExporterVersion(Exception):
    def __init__(self, exporter_version: int):
        self.__exporter_version = exporter_version

    @property
    def exporter_version(self):
        return self.__exporter_version

    def __str__(self):
        return "Invalid exporter version was provided : {}".format(self.exporter_version)

class MediaExporterInvalidVersion(Exception):
    def __init__(self, awaited_version: int, exporter_version: int):
        self.__awaited_version = awaited_version
        self.__exporter_version = exporter_version

    @property
    def awaited_version(self):
        return self.__awaited_version

    @property
    def exporter_version(self):
        return self.__exporter_version

    @property
    def __str__(self):
        return "Exporter version is {}. Exporter version found from Context : {}".format(self.awaited_version, self.exporter_version)

class RegexReworkException(Exception):
    def __init__(self, regex_name: str):
        self.__regex_name = regex_name

    @property
    def regex_name(self):
        return self.__regex_name

    def __str__(self):
        return "The regex for {} seems to be broken. It needs a rework.".format(self.regex_name)
