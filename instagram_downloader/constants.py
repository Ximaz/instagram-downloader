import string


"""
Headers to try to get to make ratelimited more delayed :
X-IG-WWW-Claim : possible value : hmac.AR0AbouJHrmcxB5qmK63cSap8R1sB28wynhILjXkHjfa9rG_
Cookies : possible value : "csrftoken=SiVOKBnuebNtr3OwQoHG0RnAWmCoMSJw; mid=YjdrngALAAF7q7d152TbJAvkD5m8; ig_did=35AE6F4E-9302-42FE-8179-577C6A0E826A; ds_user_id=34860308922; sessionid=34860308922%3AIB2gtwW5WNM4NY%3A16; datr=L1-gYsKLshDxe64ElQAZaIDg; shbid=\"18935\\05434860308922\\0541687797516:01f79031041c0061075b33a54e3e54101477701729e70153e949cd612d5f74e7bb4f6e33\"; shbts=\"1656261516\\05434860308922\\0541687797516:01f72b2123ffb77811ea145b92c01367746a8bfe48753b0f960a0612c1cb3f23f601efc7"; rur="RVA\05434860308922\0541687799708:01f76230e0f66c113c958d96d9817747e3516bda77bf6d21b42d64a4ef7a5381e14440f3\"" 
"""


headers = {
    "Host": "www.instagram.com",
    "Origin": "https://www.instagram.com",
    "Referer": "https://www.instagram.com/",
    "User-Agent": "TwitterBot/1.0",
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
instagram_urls = dict(
    main="https://www.instagram.com",
    graphql="https://www.instagram.com/graphql/query/?query_hash={}&variables={}",
    feed_api="https://i.instagram.com/api/v1/feed/user/{}/username/?count={}",
    target="https://www.instagram.com/{}/channel/?hl=fr",
    target_json="https://www.instagram.com/{}/?__a=1&__d=dis/"
)
base_36 = string.digits + string.ascii_letters
consumer_lib_regex = r"(\/static\/bundles\/(?:es6|metro)\/ConsumerLibCommons\.js\/[a-f0-9]+\.js)"
query_kinds_regex = dict(
    posts=r"queryId:\"([a-f0-9]{32})\"",
    stories=r"(?:const|var) _=\"([a-f0-9]{32})\"" # const = es6, var = metro
)
x_asbd_id_regex = r"ASBD_ID='(\d+)'"
x_ig_app_id_regex = r"instagramWebDesktopFBAppId='(\d+)'"
window_shared_data_regex = r"^<script type=\"text\/javascript\">window\._sharedData = (\{.*\});<\/script>$"
delay = 0
