import os
import json
from instagram_downloader import *

def main(ctx: Context = None, target: str = None):
    if ctx is None and not target:
        raise ValueError("Context and target can't be both None.")
    if ctx is None:
        ctx = Context(target)
        ctx.export()
    output = "urls.json"
    urls = []
    if os.path.exists(output):
        urls = json.load(open(output, 'r'))
    media_exporter = MediaExporter(ctx)
    after = "QVFBS3JZbFRocU9HVF80dmxlbzhmdzc1aHJheTczRGVlVVlLclZNbXhxRGdFbFA2SF9nWjhIaHFSWVBnaS16LVVJZlFTQzcxZFk4TVF2S3hrclNuR3lpVg=="
    while True:
        media_item = media_exporter.export(after=after)
        urls.extend(media_item.urls)
        json.dump(urls, open(output, "w+"))
        if after == media_item.after:
            break
        after = media_item.after
        if not after:
            break

if __name__ == "__main__":
    target = "kaguramiko__"
    ctx = Context()
    ctx.load(target)
    main(ctx)
