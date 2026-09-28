#!/usr/bin/env python3
"""Set each blog post's featured image as its social-sharing (og:image) card.

The site has no build step, so every post carries its own <head>. This script
finds each post's featured image (the first /assets/blog/ image in the page),
and writes the og:image / twitter:card tags into the head, replacing any old
ones. Safe to re-run; run it after adding or re-imaging a post:

    python3 scripts/sync-blog-og.py          # update files
    python3 scripts/sync-blog-og.py --check  # list posts that are out of date
"""
import html
import re
import struct
import sys
from pathlib import Path

SITE = "https://freethinkersconsulting.com"
ROOT = Path(__file__).resolve().parent.parent
BEGIN = "  <!-- share-image:start (scripts/sync-blog-og.py) -->"
END = "  <!-- share-image:end -->"

FEATURED = re.compile(r'<img src="(/assets/blog/[^"]+)"')
OLD_TAGS = re.compile(
    r'^[ \t]*<meta (?:property="og:image[^"]*"|name="twitter:[^"]*")[^>]*>\n', re.M
)
BLOCK = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", re.S)


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2  # JPEG: walk segments to the first SOF marker
    while i < len(data):
        marker, length = data[i + 1], struct.unpack(">H", data[i + 2 : i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return w, h
        i += 2 + length
    raise ValueError(f"can't read size of {path}")


def share_block(src, alt):
    w, h = image_size(ROOT / src.lstrip("/"))
    url = SITE + src
    mime = "image/png" if src.endswith(".png") else "image/jpeg"
    return "\n".join([
        BEGIN,
        f'  <meta property="og:image" content="{url}" />',
        f'  <meta property="og:image:secure_url" content="{url}" />',
        f'  <meta property="og:image:type" content="{mime}" />',
        f'  <meta property="og:image:width" content="{w}" />',
        f'  <meta property="og:image:height" content="{h}" />',
        f'  <meta property="og:image:alt" content="{alt}" />',
        '  <meta name="twitter:card" content="summary_large_image" />',
        f'  <meta name="twitter:image" content="{url}" />',
        END,
        "",
    ])


def updated(page):
    text = page.read_text()
    if 'property="og:type" content="article"' not in text:
        return None
    m = FEATURED.search(text)
    if not m:
        return None
    alt = re.search(r'alt="([^"]*)"', text[m.start() : text.index(">", m.start())])
    alt = alt.group(1) if alt else html.escape(page.parent.name)
    head, body = text.split("</head>", 1)
    head = OLD_TAGS.sub("", BLOCK.sub("", head))
    anchor = re.search(r'^[ \t]*<meta property="og:site_name"[^>]*>\n', head, re.M)
    at = anchor.end() if anchor else head.rindex("\n") + 1
    head = head[:at] + share_block(m.group(1), alt) + head[at:]
    new = head + "</head>" + body
    return new if new != text else None


def main():
    check = "--check" in sys.argv
    changed = []
    for page in sorted(ROOT.glob("*/index.html")):
        new = updated(page)
        if new is None:
            continue
        changed.append(page.parent.name)
        if not check:
            page.write_text(new)
    verb = "out of date" if check else "updated"
    print(f"{len(changed)} post(s) {verb}" + "".join(f"\n  {c}" for c in changed))
    return 1 if check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
