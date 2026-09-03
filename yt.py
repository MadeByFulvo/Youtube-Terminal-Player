"""yt.py — search YouTube from the command line and play the top result.
Usage:  python yt.py "rickroll"
        python yt.py "https://youtu.be/dQw4w9WgXcQ"
"""

import shutil
import subprocess
import sys

try:
    import yt_dlp
except ImportError:
    print("> installing yt-dlp ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-U", "yt-dlp"])

C = {"t": "\033[1;36m", "g": "\033[32m", "d": "\033[2m", "r": "\033[31m", "x": "\033[0m"}

def ensure_mpv():
    if shutil.which("mpv"):
        return True
    print("> mpv not found — trying to install it ...")
    try:
        subprocess.run(["sudo", "-n", "apt-get", "install", "-y", "-qq", "mpv"],
                       check=True, timeout=300)
    except Exception:
        return False
    return bool(shutil.which("mpv"))

def resolve(arg):
    """URL/ID in → use as-is. Anything else → search and take the top hit."""
    if arg.startswith(("http://", "https://")):
        return arg, None
    if len(arg) == 11:
        return f"https://youtu.be/{arg}", None
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True,
                           "extract_flat": "in_playlist"}) as ydl:
        data = ydl.extract_info(f"ytsearch1:{arg}", download=False)
    entry = (data.get("entries") or [None])[0]
    if not entry or not entry.get("id"):
        print(f"{C['r']}> no results for {arg!r}{C['x']}")
        sys.exit(1)
    return f"https://youtu.be/{entry['id']}", entry.get("title")

def play(url, title):
    print()
    print(f"{C['t']}# YouTube Player{C['x']}")
    if title:
        print(f"{C['d']}> {title}{C['x']}")
    print(f"{C['d']}> {url}{C['x']}")

    if ensure_mpv():
        print(f"{C['g']}▶ playing in terminal{C['x']}")
        rc = subprocess.run([
            "mpv", "--really-quiet", "--vo=tct", "--terminal=no",
            "--profile=sw-fast", "--framedrop=vo",
            "--ytdl-format=worst[height<=240]", url,
        ]).returncode
        if rc != 0:
            print(f"{C['r']}> mpv failed ({rc}) — run:  yt-dlp -U{C['x']}")
    else:
        print(f"{C['d']}> mpv unavailable — opening in your browser{C['x']}")
        import webbrowser
        webbrowser.open(url)

def main():
    if len(sys.argv) < 2:
        print(f'usage: python {sys.argv[0]} "search words"')
        sys.exit(1)
    url, title = resolve(" ".join(sys.argv[1:]))
    play(url, title)

if __name__ == "__main__":
    main()
