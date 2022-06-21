import re
import json
import random
import requests
from .constants import *


def __int_to_base(x: int, base: int):
    if x < 0:
        sign = -1
    elif x == 0:
        return base_36[0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(base_36[x % base])
        x = x // base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)


def export_consumer_lib(target: str) -> str:
    response = requests.get(instagram_target_url.format(
        target), headers=headers).text
    script_url = re.search(consumer_lib_regex, response, re.M)

    if not script_url:
        raise ValueError(
            "RegEx for consumer lib commons script must be reworked.")
    script_url = script_url[1]
    return requests.get("{}{}".format(instagram_main_url, script_url)).text


def generate_x_mid() -> str:
    def random_uint32(): return random.randint(2**29, 2**32)
    pool = ""
    for _ in range(8):
        pool += __int_to_base(random_uint32(), 36)
    return pool


def export_required_headers(target: str, consumer_lib_commons: str) -> dict:
    window_shared_data = None
    required_headers = {"X-Mid": None,
                        "X-CSRFToken": None, "X-IG-App-ID": None}
    main_page = requests.get(instagram_target_url.format(
        target), headers=headers).text
    window_shared_data_match = re.search(
        window_shared_data_regex, main_page, re.M)

    if not window_shared_data_match:
        raise ValueError("RegEx for window shared data must be reworked.")
    window_shared_data_match = window_shared_data_match[1]
    try:
        window_shared_data = json.loads(window_shared_data_match)
    except json.decoder.JSONDecodeError:
        raise ValueError("Window shared data found but wrong format.")
    required_headers["X-CSRFToken"] = window_shared_data["config"]["csrf_token"]
    required_headers["X-Mid"] = generate_x_mid()
    x_ig_app_id = re.search(x_ig_app_id_regex, consumer_lib_commons, re.M)
    if not x_ig_app_id:
        raise ValueError("RegEx for x-ig-app-id must be reworked.")
    x_ig_app_id = x_ig_app_id[1]
    required_headers["X-IG-App-ID"] = x_ig_app_id
    return required_headers


def export_query_hashes(consumer_lib_commons: str) -> list:
    query_hashes = dict(posts=None, stories=None)

    for kind, regex in query_kinds_regex.items():
        match = re.search(regex, consumer_lib_commons, re.M)
        if match:
            query_hashes[kind] = match[1]
    return query_hashes


def export_user_id(target: str, headers: dict) -> str:
    url = "{}/{}/?__a=1&__d=dis".format(instagram_main_url, target)
    headers["Accept"] = "*/*"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "same-origin"
    headers["TE"] = "trailers"
    del headers["Upgrade-Insecure-Requests"]
    del headers["Sec-Fetch-User"]
    return requests.get(url, headers=headers).json()["graphql"]["user"]["id"]