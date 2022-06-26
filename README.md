# Instagram Downloader
Instagram Downloader is an automated Python solution to let anyone **without an Instagram account** download the entire Instagram content of any public account. It's main purpose is to downloads posts, but as soon as possible, stories will be available too.

# Automation ?
Instagram works with many headers to prevent people doing this kind of project, and make their road as hard as possible. However, with some determination, I was able to find ways to get this kind of header an automated way. Let me explain.

### The ConsumerLibCommons.js
This file is located at ``https://instagram.com/static/build/es6/ConsumerLibCommons.js/SOME_HEXA.js``. I wont put the ``SOME_HEXA`` thing since it changes as soon as Instagram pushes an update. You just have to go to the main Instagram's page and search for this lib.

This lib contains everything related to the API. It will be very important for the next.

### Query hashes
Query hashes are strings that let Instagram's API what kind of resources the client tries to fetch. If it's stories, posts, and so on. It looks like this : ``69cba40317214236af40e7efa697781d``. This type of string can be found into the ``ConsumerLibCommons.js``. To find them, I had to apply some regex. It contains two of them : the posts one and the stories one. You can find the regex at ``instagram_downloader/constants.py``.

### Required headers
THe required headers are the thing Instagram looks at to tell if a request has to be server or not. The most important ones are ``X-Mid``, ``X-CSRFToken``, ``ig_did``'s cookie, ``X-IG-App-ID`` and ``X-ASBD-ID``.

``X-Mid``: It's a string that can be represented as a list of 8 elements. Each of them is an unsigned int written on 32 bits (2^32). Once you have 8 uint32 generated "randomly", they are all converted into base 36 (``0123456789abcdefghijklmnopqrstuvwxyz``) and then concatenated together. The way to generate this string comes from the ``ConsumerLibCommons.js`` but the string itself is not hard-coded.

``X-CSRFToken`` : When you go on Instagram, specifically in a user page, Instagram' server collect some of your data and place them into a json object called ``sharedData``. This data is then sent to the client and placed at ``window._sharedData``. Finally, you can found the ``csrf_token`` key, that contains the value of the header, at ``window._sharedData["config"]["csrf_token"]``. To get the ``sharedData`` object, I also had to use regex.

``ig_did``'s cookie: This is a string that tracks your device. It's a cookie you can see apear on several requests and is also placed into the ``sharedData`` at ``window._sharedData["device_id"]``.

``X-IG-App-ID`` and ``X-ASBD-ID`` : Their value are hard-coded in ``ConsumerLibCommons.js``. Regexes iare enough to get them.

# Setup
This is the step to follow in order to use this project :
```bash
git clone https://github.com/Ximaz/instagram-downloader
cd instagram-downloader
python3 -m pip install -r requirements.txt
```
Once done, you can edit the ``test.py`` to target someone and launch the script.

# Ratelimits
According to [Facebook GraphQL API Documentation](https://developers.facebook.com/docs/graph-api/overview/rate-limiting#applications), which is now related to the Instagram's Graph QL API, it has a ratelimit of 200 requests per hour for one user, which makes around 3 requests per minute, so almost a request for 20 seconds. Find the maths below :

```python
>>> 200 / 60       # 200 requests for 60 minutes.
3.3333333333333335 # 3 requests at lowest.
>>> 60 / 3         # 60 seconds divided by 3 requests.
20.0               # 20 seconds at highest.
```

In order to slow the process of getting marked as bot, the sleep delay gets incremented with a random number between 1 and 2 followed by a ``random.random`` call to get a floating number than emulates a humain delay.

In addition, knowing a computer isn't delaying the perfect way, I added 5 seconds more, which makes ``25 + random_delay`` seconds.

However, no information was found nowadays about the user page itself, the ``Context`` object was made to tackle this problem.

# Thanks
Thanks for reading, hope you liked the project and the way I describe the Instagram API's way to work. Please, leave a star before going. :)
