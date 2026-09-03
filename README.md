# yt.py

Search YouTube from the command line and play the top result — right in your terminal.

```bash
python yt.py "rickroll"
```

## Usage

| Command | What it does |
|---|---|
| `python yt.py "search words"` | Searches YouTube, plays the top result |
| `python yt.py "dQw4w9WgXcQ"` | Plays a video by ID |
| `python yt.py "https://youtu.be/dQw4w9WgXcQ"` | Plays a full URL |

No menus, no prompts, no setup. One command in, video out.

## How it plays

- **Terminal video** — if `mpv` is installed, the video renders right in your terminal (`--vo=tct`, low-res for smoothness)
- **Browser fallback** — if `mpv` can't be installed, it opens the video in your browser instead

Everything installs itself on first run:
- `yt-dlp` (search + streaming) → auto-installed via `pip` if missing
- `mpv` (terminal player) → auto-installed via `apt` if missing and sudo allows it

## Requirements

- Python 3.9+
- A terminal with truecolor support for best terminal playback

## Troubleshooting

```bash
# If playback or search breaks (YouTube changes often):
yt-dlp -U

# Test mpv directly:
mpv --vo=tct "https://youtu.be/dQw4w9WgXcQ"
```

> **Note:** terminal video quality depends on your terminal, not the code.

## License

MIT
