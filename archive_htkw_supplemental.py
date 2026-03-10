#!/usr/bin/env python3
"""
Download supplemental pages linked from htkw/ files:
  - nic/service.html  -> htkw/nic_service.html
  - quiz/ckd1_quiz    -> htkw/ckd1_quiz.html

Then rewrite links in all htkw/ files to point to local copies.
Also notes:
  - nephsites/diet        -> already in ../diet/
  - nephsites/nic/dorsum  -> already in ../patient_education/saving_veins.html
  - htkc/r27_html         -> 404, skip
"""

import os
import re
import urllib.request
import urllib.parse
import time
import glob

OUTPUT_DIR = "htkw"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

SUPPLEMENTAL_PAGES = [
    ("http://www.nephron.org/nephsites/nic/service.html",  "nic_service.html",  "Mission Statement"),
    ("http://www.nephron.org/nephsites/quiz/ckd1_quiz",    "ckd1_quiz.html",    "Chronic Kidney Disease Quiz"),
]

# Map from original URL patterns to local filenames (within htkw/)
LINK_MAP = {
    # Supplemental pages being downloaded
    "/nephsites/nic/service.html":                              "nic_service.html",
    "nephron.org/nephsites/nic/service.html":                   "nic_service.html",
    "links.nephron.com/nephsites/nic/service.html":             "nic_service.html",
    "/nephsites/quiz/ckd1_quiz":                                "ckd1_quiz.html",
    "nephron.org/nephsites/quiz/ckd1_quiz":                     "ckd1_quiz.html",
    # Already archived elsewhere - use relative paths from htkw/
    "/nephsites/diet":                                          "../diet/index.html",
    "nephron.org/nephsites/diet":                               "../diet/index.html",
    "/nephsites/nic/dorsum":                                    "../patient_education/saving_veins.html",
    "nephron.org/nephsites/nic/dorsum":                         "../patient_education/saving_veins.html",
    # 404 - leave as-is but we'll note it
}


def fetch_url(url, retries=2):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read(), resp.geturl()
        except Exception as e:
            if attempt < retries:
                print(f"  Retry {attempt+1} for {url}: {e}")
                time.sleep(1)
            else:
                print(f"  FAILED: {url}: {e}")
                return None, url
    return None, url


def extract_images(html_text, page_url):
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
    bg_url = re.findall(r'url\(["\']?([^"\')\s]+)["\']?\)', html_text, re.IGNORECASE)
    all_srcs = img_srcs + bg_url
    resolved = []
    for src in all_srcs:
        if src.startswith("data:"):
            continue
        if src.startswith("http://") or src.startswith("https://"):
            resolved.append(src)
        elif src.startswith("//"):
            resolved.append("http:" + src)
        else:
            resolved.append(urllib.parse.urljoin(page_url, src))
    return list(set(resolved))


def download_image(img_url):
    parsed = urllib.parse.urlparse(img_url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return None
    filename = re.sub(r"[?#].*$", "", filename)
    local_path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(local_path):
        return filename
    print(f"    Downloading image: {filename}")
    data, _ = fetch_url(img_url)
    if data:
        with open(local_path, "wb") as f:
            f.write(data)
        return filename
    return None


def rewrite_supplemental_links(html_text, page_url, image_map):
    """Rewrite img src to local and supplemental hrefs to local files."""

    # Rewrite img tags
    def rewrite_img(m):
        full_tag = m.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag, re.IGNORECASE)
        if not src_match:
            return full_tag
        src = src_match.group(1)
        if src.startswith("data:"):
            return full_tag
        if src.startswith("http://") or src.startswith("https://"):
            abs_url = src
        elif src.startswith("//"):
            abs_url = "http:" + src
        else:
            abs_url = urllib.parse.urljoin(page_url, src)
        if abs_url in image_map and image_map[abs_url]:
            return full_tag.replace(src, f"images/{image_map[abs_url]}")
        return full_tag

    html_text = re.sub(r"<img[^>]+>", rewrite_img, html_text, flags=re.IGNORECASE)

    # Rewrite supplemental links
    def rewrite_href(m):
        href = m.group(1)
        for pattern, local in LINK_MAP.items():
            if pattern in href:
                return f'href="{local}"'
        return m.group(0)

    html_text = re.sub(r'href="([^"]+)"', rewrite_href, html_text, flags=re.IGNORECASE)

    return html_text


def download_supplemental_page(url, local_filename, title):
    output_path = os.path.join(OUTPUT_DIR, local_filename)
    if os.path.exists(output_path):
        print(f"  Already exists: {local_filename}")
        return True

    print(f"\nFetching: {title}")
    print(f"  URL: {url}")
    data, final_url = fetch_url(url)
    if data is None:
        print(f"  SKIPPED")
        return False

    html_text = data.decode("utf-8", errors="replace")

    # Download images
    img_urls = extract_images(html_text, final_url)
    image_map = {}
    for img_url in img_urls:
        ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1].lower()
        if ext in (".jpg", ".jpeg", ".gif", ".png", ".svg", ".webp", ".ico"):
            local_name = download_image(img_url)
            if local_name:
                image_map[img_url] = local_name

    html_text = rewrite_supplemental_links(html_text, final_url, image_map)

    with open(output_path, "w", encoding="utf-8", errors="replace") as f:
        f.write(html_text)
    print(f"  Saved: {output_path} ({len(html_text)} bytes, {len(image_map)} images)")
    return True


def rewrite_all_htkw_files():
    """Rewrite supplemental links in all existing htkw/ files."""
    print("\n=== Rewriting supplemental links in all htkw/ files ===\n")

    html_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.html")))

    for filepath in html_files:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()

        updated = original

        # Apply LINK_MAP rewrites
        def rewrite_href(m):
            href = m.group(1)
            for pattern, local in LINK_MAP.items():
                if pattern in href:
                    return f'href="{local}"'
            return m.group(0)

        updated = re.sub(r'href="([^"]+)"', rewrite_href, updated, flags=re.IGNORECASE)

        if updated != original:
            with open(filepath, "w", encoding="utf-8", errors="replace") as f:
                f.write(updated)
            print(f"  Updated: {os.path.basename(filepath)}")
        else:
            print(f"  No changes: {os.path.basename(filepath)}")


def main():
    print("=== Downloading HTKW Supplemental Pages ===\n")
    os.makedirs(IMAGES_DIR, exist_ok=True)

    success = []
    for url, local_filename, title in SUPPLEMENTAL_PAGES:
        if download_supplemental_page(url, local_filename, title):
            success.append((local_filename, title))
        time.sleep(0.3)

    rewrite_all_htkw_files()

    print(f"\n=== Done ===")
    print(f"Downloaded {len(success)} supplemental pages")
    print("\nLink mapping applied:")
    for pattern, local in LINK_MAP.items():
        print(f"  {pattern!r} -> {local!r}")


if __name__ == "__main__":
    main()
