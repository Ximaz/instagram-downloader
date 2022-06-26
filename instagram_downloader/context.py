import json
import zlib
from .util import *
from .constants import *
from .exceptions import *


class Context:
    def __init__(self, target: str, exporter_version: int = 2):
        """
        The exporter version can take 2 values :
        - 1 : The V1 exporter. It uses the GraphQL API to make requests with query hashes,
              and some variables stored in the URL as JSON. It's formated the following way :
              https://www.instagram.com/graphql/query/?query_hash=X&variables=X

        - 2 : The V2 exporter. It uses the Feed API to get content. The next cursor corresponds
              to a post ID, different from ``after`` from GraphQL variables. It's formated the
              following way :
              https://i.instagram.com/api/v1/feed/user/UID/?count=X&max_id=X
              It's the default exporter version since it does not require query hashes.

        The context is saved as JSON dict zipped with zlib into a file formated
        the following way :
        {TARGET}_{EXPORTER_VERSION}_ctx.raw

        """

        self.__target = target
        self.__exporter_version = None
        self.__target_id = None
        self.__consumer_lib_commons = None
        self.__query_hashes = None
        self.__required_headers = None
        self.__target_id = None

        self.__check_exporter_version(exporter_version)
        self.__exporter_version = exporter_version
        try:
            self.__load()
        except FileNotFoundError:
            self.__init()

    @staticmethod
    def __check_exporter_version(exporter_version: int):
        if exporter_version not in (1, 2):
            raise ContextInvalidExporterVersion(exporter_version)

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
    def exporter_version(self):
        return self.__exporter_version

    @property
    def headers(self):
        __headers = headers.copy()

        for name, value in self.required_headers.items():
            __headers[name.replace("_", "-")] = value
        __headers["Referer"] = instagram_urls["target"].format(self.target)
        return __headers

    @property
    def context_filename(self):
        return "{}_v{}_ctx.raw".format(self.target, self.exporter_version)

    def __propagate(self, context: dict):
        self.__target = context["target"]
        self.__target_id = context["target_id"]
        self.__check_exporter_version(context["exporter_version"])
        self.__exporter_version = context["exporter_version"]
        self.__query_hashes = json.loads(context["query_hashes"])
        self.__required_headers = json.loads(context["required_headers"])

    def __str__(self):
        return json.dumps(
            dict(
                target=self.target,
                target_id=self.target_id,
                exporter_version=self.exporter_version,
                query_hashes=json.dumps(self.query_hashes),
                required_headers=json.dumps(self.required_headers),
            )
        )

    def __export(self):
        with open(self.context_filename, "wb+") as stream:
            stream.write(zlib.compress(self.__str__().encode()))
        stream.close()

    def __load(self):
        data = None
        with open(self.context_filename, 'rb') as stream:
            data = stream.read()
        stream.close()
        try:
            data = zlib.decompress(data).decode()
        except zlib.error:
            raise ContextCorrupted
        self.__propagate(json.loads(data))

    def __init(self):
        self.__consumer_lib_commons = export_consumer_lib(self.target)
        self.__required_headers = export_required_headers(self.target, self.__consumer_lib_commons)
        if self.__exporter_version == 1:
            self.__query_hashes = export_query_hashes(self.__consumer_lib_commons)
            self.__target_id = export_user_id(self.target, self.headers.copy())
        self.__export()
