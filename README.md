# nexech.github.io

Static JSON feeds and assets read by the Nexech apps. Everything is served as-is by GitHub Pages from `main`;
pushing a change publishes it.

| Path | Purpose |
| --- | --- |
| `data/feature-flags.json` | Remote feature flags. |
| `data/wallpapers.json` | Wallpaper catalog for the v2 wallpaper picker. |
| `assets/wallpapers/` | Wallpaper images (`<id>.webp`) and 400 px thumbnails (`<id>_thumb.webp`). |
| `tools/add-wallpaper.py` | Adds or updates a catalog entry from a local image. |

## Adding a wallpaper

1. Prepare a WebP (or PNG/JPEG) image up to 3840 x 2160 and 10 MB, and a small thumbnail (about 400 px).
2. Run `python tools/add-wallpaper.py <id> <image> <thumbnail> --title "Sunset"`. The `id` uses `a-z`, `0-9` and `_`
   and never changes once published (a user's selection is stored as `dl:<id>`). The script copies both files into
   `assets/wallpapers/`, computes `sha256` and `bytes`, and appends the entry to `data/wallpapers.json`.
3. Commit and push to `main`. Every v2 app shows the wallpaper the next time the picker opens.

To hide a wallpaper set `"enabled": false` on its entry; devices that already downloaded it keep the file. Do not
reuse an id for a different image: the app trusts the digest in the feed but keeps previously downloaded files.
Changing the image of an existing id requires a new id.

The feed is unsigned on purpose, so changes apply immediately. Keep write access to this repository restricted.
