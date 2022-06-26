import os
import json
from instagram_downloader import *

def build_exporter(ctx: Context):
    if ctx.exporter_version == 1:
        return MediaExporter(ctx)
    elif ctx.exporter_version == 2:
        return MediaExporterV2(ctx)
    else:
        raise ContextCorrupted

def load_existing_urls(filename: str):
    urls = []
    if os.path.exists(filename):
        urls = json.load(open(filename, 'r'))
    return urls

def main(ctx: Context, after: str = ""):
    output = "urls.json"
    urls = load_existing_urls(output)
    exporter = build_exporter(ctx)

    while True:
        print("New request (current cursor: {}) !".format(after))
        try:
            media_item = exporter.export(first=100, after=after)
        except InstagramRateLimit as exception:
            print(exception)
            break
        urls.extend(media_item.urls)
        json.dump(urls, open(output, "w+"))
        if after == media_item.after:
            break
        if not media_item.has_next:
            break
        after = media_item.after
        if not after:
            break

if __name__ == "__main__":
    after = "" # May be used in case the script breaks
    target = "TARGET"
    ctx = Context(target, 2)
    main(ctx, after)
