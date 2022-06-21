import json
import requests
from .context import *
from .constants import *


def export_medias(ctx: Context, first: int = 12, after: str = None) -> dict:
    headers = ctx.headers
    query_hash = ctx.query_hashes["posts"]
    variables = dict(id=ctx.target_id, first=first, after=after)
    url = "{}?query_hash={}&variables={}".format(instagram_graphql_url, query_hash, json.dumps(variables))
    return json.dumps(requests.get(url, headers=headers).json()["data"]["user"]["edge_owner_to_timeline_media"]["edges"])
