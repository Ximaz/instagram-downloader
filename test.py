import os
import json
from instagram_downloader import *

def main(target: str, after: str = ""):
    urls = []
    ctx = Context(target)
    output = "urls.json"
    if os.path.exists(output):
        urls = json.load(open(output, 'r'))
    if ctx.exporter_version == 1:
        media_exporter = MediaExporter()
    elif ctx.exporter_version == 2:
        media_exporter = MediaExporterV2(ctx)
    else:
        raise ValueError("Context was alterated.")
    while True:
        media_item = media_exporter.export(first=12, after=after)
        urls.extend(media_item.urls)
        json.dump(urls, open(output, "w+"))
        if after == media_item.after:
            break
        after = media_item.after
        if not after:
            break

if __name__ == "__main__":
    after = "QVFCQ0hJVG9RVTNabFozTXRiMkJJNUppenJqeF9CckhnMmdFbzA3OHdlSVVQb3Juc2NIdnR1WmVSWF9Yd0R2dzdUeDExTlhOXzI3YXJhZnBjSUVCaHJmYg=="
    main("kaguramiko__", after)
