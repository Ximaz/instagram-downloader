import string


headers = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "X-IG-WWW-Claim": "0",
    "X-ASBD-ID": "198387"
}
base_36 = string.digits + string.ascii_letters
instagram_main_url = "https://www.instagram.com"
instagram_graphql_url = "{}/graphql/query/".format(instagram_main_url)
instagram_target_url = instagram_main_url + "/{}/channel/?hl=fr"
consumer_lib_regex = r"(\/static\/bundles\/es6\/ConsumerLibCommons\.js\/[a-f0-9]+\.js)"
query_kinds_regex = dict(
    posts=r"queryId:\"([a-f0-9]{32})\"", stories=r"const _=\"([a-f0-9]{32})\"")
x_ig_app_id_regex = r"instagramWebDesktopFBAppId='(\d+)'"
window_shared_data_regex = r"^<script type=\"text\/javascript\">window\._sharedData = ({.*});<\/script>$"
