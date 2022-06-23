class InstagramRateLimit(Exception):
    def __init__(self, after: str = None):
        self.__after = after

    @property
    def after(self):
        return self.__after

    def __str__(self):
        return "Instagram ratelimited your IP address. The current cursor : {}".format(self.__after)
