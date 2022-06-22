import time
import json
import requests
from .context import *
from .constants import *

class MediaItem:
    def __init__(self, urls: list, after: str = None):
        self.__urls = urls
        self.__after = after

    @property
    def urls(self):
        return self.__urls

    @property
    def after(self):
        return self.__after

    def __str__(self):
        return json.dumps(
            dict(
                urls=json.dumps(self.urls),
                after=self.after
            )
        )

class MediaExporter:
    def __init__(self, ctx: Context):
        self.__ctx = ctx

    @property
    def ctx(self):
        return self.__ctx

    @staticmethod
    def __handle_graph_image(node: dict) -> list:
        return node["display_resources"][-1]["src"]

    def __handle_graph_side_car(self, node: dict) -> list:
        links = node["edge_sidecar_to_children"]["edges"]

        for i in range(len(links)):
            links[i] = self.__handle_graph_image(links[i]["node"])
        return links

    def export(self, first: int = 12, after: str = None) -> MediaItem:
        media_item = None
        headers = self.ctx.headers
        query_hash = self.ctx.query_hashes["posts"]
        variables = dict(id=self.ctx.target_id, first=first, after=(after or ""))
        url = "{}?query_hash={}&variables={}".format(instagram_graphql_url, query_hash, json.dumps(variables).replace(' ', ''))
        print(url)
        response = requests.get(url, headers=headers).json()["data"]["user"]["edge_owner_to_timeline_media"]
        after = response["page_info"]["end_cursor"]
        links = []

        for edge in response["edges"]:
            node = edge["node"]
            node_type = node["__typename"]
            if node_type == "GraphImage":
                links.append(self.__handle_graph_image(node))
            elif node_type == "GraphSidecar":
                links.extend(self.__handle_graph_side_car(node))
            else:
                print("Unknowned node type : {}\n{}\n\n".format(node_type, json.dumps(node)))
        media_item = MediaItem(links, after)
        time.sleep(delay)
        return media_item

class MediaExporterV2:
    def __init__(self, ctx: Context):
        self.__ctx = ctx

    @property
    def ctx(self):
        return self.__ctx

    @staticmethod
    def __handle_candidate(node: dict) -> list:
        return node["image_versions2"]["candidates"][0]["url"]

    def __handle_carousel_media(self, node: dict) -> list:
        links = node["carousel_media"]

        for i in range(len(links)):
            links[i] = self.__handle_candidate(links[i])
        return links

    def __make_headers(self):
        headers = self.ctx.headers
        headers["Host"] = "i.instagram.com"
        return headers

    def export(self, first: int = 3, after: str = None) -> MediaItem:
        media_item = None
        headers = self.__make_headers()
        url = "https://i.instagram.com/api/v1/feed/user/{}/?count={}".format(self.ctx.target_id if after else "{}/username".format(self.ctx.target), first)
        if after:
            url += "&max_id={}".format(after)
        print(url, headers)
        response = requests.get(url, headers=headers, allow_redirects=False)
        try:
            response = json.loads(response.text)
        except:
            print(response.text)
            raise
        after = response["next_max_id"]
        links = []

        for node in response["items"]:
            if "carousel_media" in node:
                links.extend(self.__handle_carousel_media(node))
            elif "image_versions2" in node:
                links.append(self.__handle_candidate(node))
        media_item = MediaItem(links, after)
        time.sleep(delay)
        return media_item
