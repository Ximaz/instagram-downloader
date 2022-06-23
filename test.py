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
    if os.path.exists(filename):
        urls = json.load(open(filename, 'r'))
    return urls

def main(ctx: Context, after: str = ""):
    output = "urls.json"
    urls = load_existing_urls(output)
    exporter = build_exporter(ctx)

    while True:
        try:
            media_item = exporter.export(first=12, after=after)
        except InstagramRateLimit as exception:
            print(exception)
            break
        urls.extend(media_item.urls)
        json.dump(urls, open(output, "w+"))
        if after == media_item.after:
            break
        after = media_item.after
        if not after:
            break

if __name__ == "__main__":
    target = "kaguramiko__"
    ctx = Context(target, 2)
    after = "2027720045492494327_8345035809"
    main(ctx, after)
