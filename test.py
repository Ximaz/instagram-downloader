import json
from instagram_downloader import *

def main(ctx: Context = None, target: str = None):
    if ctx is None and not target:
        raise ValueError("Context and target can't be both None.")
    if ctx is None:
        ctx = Context(target)
        ctx.export()
    urls = []
    media_exporter = MediaExporter(ctx)
    after = "QVFDZVJaRHNKZ2pGVDNDOUwxZF9MdjNSeFVZVVBZa01oNU9lLS1XTnhYWXpWWVhEX0V6RGV0LVZ1eWttV1ZQbnVBNkhaa1J3WThaeUFqU0RSaFBGdUJyWg=="
    while True:
        media_item = media_exporter.export(after=after)
        urls.extend(media_item.urls)
        json.dump(urls, open("urls.json", "w+"))
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
