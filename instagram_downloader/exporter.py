import time
import json
import random
import requests
from .context import *
from .constants import *
from .exceptions import *


def do_sleep(exporter):
    def wrapper(*args, **kwargs):
        time.sleep(delay + (random.randint(1, 2) + random.random()))
        return exporter(*args, **kwargs)
    return wrapper


class MediaItem:
    def __init__(self, urls: list, after: str = "", has_next: bool = True):
        self.__urls = urls
        self.__after = after
        self.__has_next = has_next

    @property
    def urls(self):
        return self.__urls

    @property
    def after(self):
        return self.__after

    @property
    def has_next(self):
        return self.__has_next

    def __str__(self):
        return json.dumps(
            dict(
                urls=json.dumps(self.urls),
                after=self.after,
                has_next=self.has_next
            )
        )


class MediaExporter:
    def __init__(self, ctx: Context):
        if ctx.exporter_version != 1:
            raise MediaExporterInvalidVersion(1, ctx.exporter_version)
        self.__ctx = ctx

    @property
    def ctx(self):
        return self.__ctx

    @staticmethod
    def __handle_graph_image(node: dict) -> str:
        return node["display_resources"][-1]["src"]

    @staticmethod
    def __handle_graph_video(node: dict) -> str:
        return node["video_url"]

    def __handle_graph_side_car(self, node: dict) -> list:
        return [self.__handle_graph_image(e["node"]) if e["node"]["__typename"] == "GraphImage" else self.__handle_graph_video(e["node"]) for e in node["edge_sidecar_to_children"]["edges"]]

    @do_sleep
    def export(self, first: int = 100, after: str = "") -> MediaItem:
        query_hash = self.ctx.query_hashes["posts"]
        variables = json.dumps(dict(id=self.ctx.target_id, first=first, after=after), separators=(',', ':'))
        response = requests.get(instagram_urls["graphql"].format(query_hash, variables), headers=self.ctx.headers)
        try:
            response = response.json()["data"]["user"]["edge_owner_to_timeline_media"]
        except json.decoder.JSONDecodeError:
            raise InstagramRateLimit(after)
        if "page_info" in response and "end_cursor" in response["page_info"]:
            after = response["page_info"]["end_cursor"]
            has_next = True
        else:
            after = None
            has_next = False
        links = []
        for edge in response["edges"]:
            node = edge["node"]
            node_type = node["__typename"]
            if node_type == "GraphImage":
                links.append(self.__handle_graph_image(node))
            elif node_type == "GraphVideo":
                links.append(self.__handle_graph_video(node))
            elif node_type == "GraphSidecar":
                links.extend(self.__handle_graph_side_car(node))
            else:
                print("Unknowned node type : {}\n{}\n\n".format(
                    node_type, json.dumps(node)))
        return MediaItem(links, after, has_next)


class MediaExporterV2:
    def __init__(self, ctx: Context):
        if ctx.exporter_version != 2:
            raise MediaExporterInvalidVersion(2, ctx.exporter_version)
        self.__ctx = ctx

    @property
    def ctx(self):
        return self.__ctx

    @staticmethod
    def __handle_candidate(node: dict) -> list:
        return node["image_versions2"]["candidates"][0]["url"]

    def __handle_carousel_media(self, node: dict) -> list:
        return [self.__handle_candidate(n) for n in node["carousel_media"]]

    def __make_headers(self):
        headers = self.ctx.headers
        headers["Host"] = "i.instagram.com"
        return headers

    @do_sleep
    def export(self, first: int = 100, after: str = "") -> MediaItem:
        """
        TODO : Find a way to get video URLs.
        """
        headers = self.__make_headers()
        url = instagram_urls["feed_api"].format(self.ctx.target, first)
        if after:
            url += "&max_id={}".format(after)
        response = requests.get(url, headers=headers, allow_redirects=False)
        try:
            response = response.json()
        except json.decoder.JSONDecodeError:
            raise InstagramRateLimit(after)
        if "next_max_id" in response:
            after = response["next_max_id"]
            has_next = True
        else:
            after = None
            has_next = False
        links = []
        for node in response["items"]:
            if "carousel_media" in node:
                links.extend(self.__handle_carousel_media(node))
            elif "image_versions2" in node:
                links.append(self.__handle_candidate(node))
            else:
                print("Unknowned node type :\n{}\n\n".format(json.dumps(node)))
        return MediaItem(links, after, has_next)
