from instagram_downloader import *

def main(ctx: Context = None, target: str = None):
    if ctx is None and not target:
        raise ValueError("Context and target can't be both None.")
    if ctx is None:
        ctx = Context(target)
        ctx.export()
    print(ctx)
    with open("urls.txt", "w+") as stream:
        stream.write('\n'.join(export_medias(ctx)))
    stream.close()

if __name__ == "__main__":
    target = "kaguramiko__"
    # ctx = Context()
    # ctx.load()
    main(None, target)
