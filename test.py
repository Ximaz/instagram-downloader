import os
import json
from instagram_downloader import *

def main(target: str, after: str = ""):
    urls = []
    ctx = Context(target, 2)
    output = "urls.json"
    if os.path.exists(output):
        urls = json.load(open(output, 'r'))
    if ctx.exporter_version == 1:
        media_exporter = MediaExporter(ctx)
    elif ctx.exporter_version == 2:
        media_exporter = MediaExporterV2(ctx)
    else:
        raise ContextCorrupted
    while True:
        try:
            media_item = media_exporter.export(first=12, after=after)
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
    after = "2384062639388294108_8345035809"
    main("kaguramiko__", after)
