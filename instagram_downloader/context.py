import json
from .util import *
from .constants import *


class Context:
    def __init__(self, target: str = None):
        self.__target = target
        self.__target_id = None
        self.__consumer_lib_commons = None
        self.__query_hashes = None
        self.__required_headers = None
        self.__target_id = None

        # No error raised to be able to use ``load`` function.
        if self.__target:
            self.__consumer_lib_commons = export_consumer_lib(target)
            self.__query_hashes = export_query_hashes(self.__consumer_lib_commons)
            self.__required_headers = export_required_headers(target, self.__consumer_lib_commons)
            self.__target_id = export_user_id(self.target, self.headers.copy())

    @property
    def target(self):
        return self.__target

    @property
    def query_hashes(self):
        return self.__query_hashes

    @property
    def required_headers(self):
        return self.__required_headers

    @property
    def target_id(self):
        return self.__target_id

    @property
    def headers(self):
        __headers = headers.copy()

        for name, value in self.required_headers.items():
            __headers[name.replace("_", "-")] = value
        __headers["Referer"] = instagram_target_url.format(self.target)
        return __headers

    @property
    def __dict__(self):
        return {
            "target": self.target,
            "query_hashes": json.dumps(self.query_hashes),
            "required_headers": json.dumps(self.required_headers),
            "target_id": self.target_id,
        }

    def __propagate(self, context: dict):
        self.__target = context["target"]
        self.__query_hashes = json.loads(context["query_hashes"])
        self.__required_headers = json.loads(context["required_headers"])
        self.__target_id = context["target_id"]

    def __str__(self):
        return json.dumps(self.__dict__)

    def export(self):
        output = self.target + "_ctx.json"

        with open(output, "w+") as stream:
            stream.write(self.__str__())
        stream.close()

    def load(self, target: str):
        self.__propagate(json.load(open(target + "_ctx.json", 'r')))
