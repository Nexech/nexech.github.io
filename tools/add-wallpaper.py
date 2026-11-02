"""Add or update a wallpaper entry in data/wallpapers.json."""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_BYTES = 10 * 1024 * 1024
ID_PATTERN = re.compile(r"^[a-z0-9_]{1,64}$")
SIGNATURES = (b"RIFF", b"\x89PNG", b"\xff\xd8\xff")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id")
    parser.add_argument("image", type=Path)
    parser.add_argument("thumbnail", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--order", type=int, help="sort key; defaults to after the last entry")
    args = parser.parse_args()

    if not ID_PATTERN.match(args.id):
        return fail("id must match [a-z0-9_]{1,64}")
    for path in (args.image, args.thumbnail):
        data = path.read_bytes()
        if not data.startswith(SIGNATURES):
            return fail(f"{path} is not a WebP, PNG or JPEG image")
    size = args.image.stat().st_size
    if size > MAX_BYTES:
        return fail("image is larger than 10 MB")

    target = ROOT / "assets" / "wallpapers"
    target.mkdir(parents=True, exist_ok=True)
    image = target / f"{args.id}.webp"
    thumb = target / f"{args.id}_thumb.webp"
    for source, destination in ((args.image, image), (args.thumbnail, thumb)):
        if source.resolve() != destination.resolve():
            shutil.copyfile(source, destination)

    feed_path = ROOT / "data" / "wallpapers.json"
    feed = json.loads(feed_path.read_text(encoding="utf-8")) if feed_path.exists() else {"schemaVersion": 1, "wallpapers": []}
    entries = [e for e in feed["wallpapers"] if e["id"] != args.id]
    previous = next((e for e in feed["wallpapers"] if e["id"] == args.id), None)
    order = args.order if args.order is not None else (previous["order"] if previous else max((e["order"] for e in entries), default=0) + 10)
    entry = {
        "id": args.id,
        "title": args.title or (previous["title"] if previous else args.id.replace("_", " ").title()),
        "image": f"assets/wallpapers/{image.name}",
        "thumb": f"assets/wallpapers/{thumb.name}",
        "sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
        "bytes": image.stat().st_size,
        "order": order,
        "enabled": True,
    }
    feed["wallpapers"] = sorted(entries + [entry], key=lambda e: (e["order"], e["id"]))
    feed_path.write_text(json.dumps(feed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"{args.id}: {entry['bytes']} bytes, sha256 {entry['sha256']}")
    return 0


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
