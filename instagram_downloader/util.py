import re
import json
import random
import requests
from .constants import *
from .exceptions import *


def __int_to_base(x: int, base: int) -> str:
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
    return "".join(digits)


def export_consumer_lib(target: str) -> str:
    response = requests.get(instagram_urls["target"].format(target), headers=headers).text
    script_url = re.search(consumer_lib_regex, response, re.M)
    if not script_url:
        raise RegexReworkException("ConsumerLibCommons")
    return requests.get("{}{}".format(instagram_urls["main"], script_url[1])).text


def generate_x_mid() -> str:
    return "".join([__int_to_base(random.randint(2**29, 2**32), 36) for _ in range(8)])


def export_required_headers(target: str, consumer_lib_commons: str) -> dict:
    window_shared_data = None
    required_headers = {
        "X-Mid": generate_x_mid(),
        "X-CSRFToken": None,
        "X-IG-App-ID": None,
        "X-ASBD-ID": None,
        "X-Web-Device-ID": None,
        "X-Instagram-AJAX": None,
        "Cookie": None
    }
    main_page = requests.get(instagram_urls["target"].format(target), headers=headers).text
    window_shared_data_match = re.search(window_shared_data_regex, main_page, re.M)

    if not window_shared_data_match:
        raise RegexReworkException("window._sharedData")
    window_shared_data = json.loads(window_shared_data_match[1])
    required_headers["X-CSRFToken"] = window_shared_data["config"]["csrf_token"]
    required_headers["X-Web-Device-ID"] = window_shared_data["device_id"]
    required_headers["X-Instagram-AJAX"] = window_shared_data["rollout_hash"]
    x_ig_app_id = re.search(x_ig_app_id_regex, consumer_lib_commons, re.M)
    if not x_ig_app_id:
        raise RegexReworkException("X-IG-App-ID")
    x_ig_app_id = x_ig_app_id[1]
    required_headers["X-IG-App-ID"] = x_ig_app_id
    x_asbd_id = re.search(x_asbd_id_regex, consumer_lib_commons, re.M)
    if not x_asbd_id:
        raise RegexReworkException("X-ASBD-ID")
    required_headers["X-ASBD-ID"] = x_asbd_id[1]
    required_headers["Cookie"] = "csrftoken={}; mid={}; ig_did={}".format(required_headers["X-CSRFToken"], required_headers["X-Mid"], required_headers["X-Web-Device-ID"])
    return required_headers


def export_query_hashes(consumer_lib_commons: str) -> list:
    query_hashes = dict(posts=None, stories=None)

    for kind, regex in query_kinds_regex.items():
        match = re.search(regex, consumer_lib_commons, re.M)
        if match:
            query_hashes[kind] = match[1]
    return query_hashes


def export_user_id(target: str, headers: dict) -> str:
    return requests.get(instagram_urls["target_json"].format(target), headers=headers).json()["graphql"]["user"]["id"]
