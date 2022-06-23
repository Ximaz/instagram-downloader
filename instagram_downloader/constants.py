import string


headers = {
    "Host": "www.instagram.com",
    "Origin": "https://www.instagram.com",
    "Referer": "https://www.instagram.com/",
    "User-Agent": "TwitterBot/1.0", # "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
    "Accept": "*/*",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
    "X-Requested-With": "XMLHttpRequest",
    "X-IG-WWW-Claim": "0",
}
base_36 = string.digits + string.ascii_letters
instagram_main_url = "https://www.instagram.com"
instagram_graphql_url = "{}/graphql/query/".format(instagram_main_url)
instagram_target_url = instagram_main_url + "/{}/channel/?hl=fr"
consumer_lib_regex = r"(\/static\/bundles\/(?:es6|metro)\/ConsumerLibCommons\.js\/[a-f0-9]+\.js)"
query_kinds_regex = dict(
    posts=r"queryId:\"([a-f0-9]{32})\"",
    stories=r"(?:const|var) _=\"([a-f0-9]{32})\"" # const = es6, var = metro
)
x_asbd_id_regex = r"ASBD_ID='(\d+)'"
x_ig_app_id_regex = r"instagramWebDesktopFBAppId='(\d+)'"
window_shared_data_regex = r"^<script type=\"text\/javascript\">window\._sharedData = (\{.*\});<\/script>$"
delay = 4
