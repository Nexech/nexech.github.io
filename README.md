# nexech.github.io

Static JSON feeds and assets read by the Nexech apps. Everything is served as-is by GitHub Pages from `main`;
pushing a change publishes it.

| Path | Purpose |
| --- | --- |
| `data/feature-flags.json` | Remote feature flags. |
| `data/wallpapers.json` | Wallpaper catalog for the v2 wallpaper picker. |
| `assets/wallpapers/` | Wallpaper images (`<id>.webp`) and 400 px thumbnails (`<id>_thumb.webp`). |
| `data/ai-models.json` | AI model catalog read by the Manage models page. |
| `assets/ai-models/<id>/<version>/` | Model files, split into parts of at most 90 MB (GitHub rejects larger files), with a `NOTICE.txt`. |
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

## Publishing an AI model

Run the publisher from the NextAppAndroid repository after validating the final model export.

```powershell
python tools/alicia/publish_model.py --site <this-checkout> release --id alicia_flash --title "Alicia - Voice Commands" --model <export.litertlm> --version 1.0.0 --contract 3
```

The publisher writes the download parts and `NOTICE.txt` under `assets/ai-models/<id>/<version>/` and adds the release
to `data/ai-models.json`. Keep earlier releases so compatible apps can resolve the newest version they support.
Publish each payload under a new version and set `contract`, `minAppVersionCode` and `versionFamilies` for its runtime
requirements. Nexech OS and Nexech Ads ship with the app. The catalog carries downloadable models.
