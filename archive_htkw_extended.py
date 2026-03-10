#!/usr/bin/env python3
"""
Extended archive for the "How the Kidney Works" section.
Downloads all r*_html pages that are linked from existing pages
but not yet downloaded. Then rewrites ALL links in htkw/ files.
"""

import os
import re
import urllib.request
import urllib.parse
import time

BASE_URL = "http://www.nephron.com/nephsites/htkw/"
ALT_BASE_URL = "http://www.nephron.org/nephsites/htkw/"

OUTPUT_DIR = "htkw"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")

# Pages we already have (src_key -> local_filename)
ALREADY_HAVE = {
    'r1_html': 'r1.html',
    'r8_html': 'r8.html',
    'r9_html': 'r9.html',
    'r10_html': 'r10.html',
    'r11_html': 'r11.html',
    'r12_html': 'r12.html',
    'r13_html': 'r13.html',
    'r14_html': 'r14.html',
    'r15_html': 'r15.html',
    'r16_html': 'r16.html',
    'r17_html': 'r17.html',
    'r32_html': 'r32.html',
    'r33_html': 'r33.html',
    'r52_html': 'r52.html',
    'ckd_pcp': 'ckd_pcp.html',
}

# Pages we need to download (found via link scan)
MISSING_PAGES = [
    'r18_html', 'r19_html', 'r20_html', 'r21_html', 'r22_html',
    'r23_html', 'r24_html', 'r25_html', 'r26_html', 'r28_html',
    'r29_html', 'r30_html', 'r31_html', 'r34_html', 'r35_html',
    'r36_html', 'r37_html', 'r38_html', 'r39_html', 'r40_html',
    'r41_html', 'r42_html', 'r43_html', 'r44_html', 'r45_html',
    'r46_html', 'r47_html', 'r48_html', 'r49_html', 'r50_html',
    'r51_html',
]


def src_key_to_local(src_key):
    """Convert r8_html -> r8.html or ckd_pcp -> ckd_pcp.html"""
    if src_key.endswith('_html'):
        return src_key[:-5] + '.html'
    return src_key + '.html'


def fetch_url(url, retries=2):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
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
        if src.startswith('data:'):
            continue
        if src.startswith('http://') or src.startswith('https://'):
            resolved.append(src)
        elif src.startswith('//'):
            resolved.append('http:' + src)
        else:
            resolved.append(urllib.parse.urljoin(page_url, src))
    return list(set(resolved))


def download_image(img_url, images_dir):
    parsed = urllib.parse.urlparse(img_url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return None
    filename = re.sub(r'[?#].*$', '', filename)
    local_path = os.path.join(images_dir, filename)
    if os.path.exists(local_path):
        return filename
    print(f"    Downloading image: {os.path.basename(img_url)}")
    data, _ = fetch_url(img_url)
    if data:
        with open(local_path, 'wb') as f:
            f.write(data)
        return filename
    return None


def build_full_url_map():
    """Build the complete map of all r*_html keys to local filenames."""
    url_map = dict(ALREADY_HAVE)
    for key in MISSING_PAGES:
        url_map[key] = src_key_to_local(key)
    # Also add r0_html even though it 404s, so links to it stay intact
    url_map['r0_html'] = 'r0.html'
    return url_map


def rewrite_html_links(html_text, page_url, image_map, url_map):
    """Rewrite all htkw r*_html links to local filenames and fix image paths."""

    # Rewrite img tags
    def rewrite_img(m):
        full_tag = m.group(0)
        src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag, re.IGNORECASE)
        if not src_match:
            return full_tag
        src = src_match.group(1)
        if src.startswith('data:'):
            return full_tag
        if src.startswith('http://') or src.startswith('https://'):
            abs_url = src
        elif src.startswith('//'):
            abs_url = 'http:' + src
        else:
            abs_url = urllib.parse.urljoin(page_url, src)
        if abs_url in image_map and image_map[abs_url]:
            local_name = image_map[abs_url]
            quote = '"' if '"' in src_match.group(0) else "'"
            return full_tag.replace(src_match.group(1), f'images/{local_name}')
        return full_tag

    html_text = re.sub(r'<img[^>]+>', rewrite_img, html_text, flags=re.IGNORECASE)

    # Rewrite htkw href links - match any URL pattern containing nephsites/htkw/
    def rewrite_htkw_href(m):
        href = m.group(1)
        # Extract the key at the end of the path
        key_match = re.search(r'(?:htkw/)([a-z0-9_]+)(?:/|$)', href)
        if key_match:
            key = key_match.group(1)
            if key in url_map:
                return f'href="{url_map[key]}"'
        return m.group(0)

    def rewrite_htkw_href_sq(m):
        href = m.group(1)
        key_match = re.search(r'(?:htkw/)([a-z0-9_]+)(?:/|$)', href)
        if key_match:
            key = key_match.group(1)
            if key in url_map:
                return f"href='{url_map[key]}'"
        return m.group(0)

    # Absolute URLs: http://www.nephron.com/nephsites/htkw/...
    html_text = re.sub(
        r'href="([^"]*nephsites/htkw/[^"]*)"',
        rewrite_htkw_href, html_text, flags=re.IGNORECASE
    )
    html_text = re.sub(
        r"href='([^']*nephsites/htkw/[^']*)'",
        rewrite_htkw_href_sq, html_text, flags=re.IGNORECASE
    )

    # Relative URLs starting with /nephsites/htkw/
    html_text = re.sub(
        r'href="(/nephsites/htkw/[^"]*)"',
        rewrite_htkw_href, html_text, flags=re.IGNORECASE
    )
    html_text = re.sub(
        r"href='(/nephsites/htkw/[^']*)'",
        rewrite_htkw_href_sq, html_text, flags=re.IGNORECASE
    )

    return html_text


def download_page(src_key, url_map):
    """Download a page, its images, and return (html_text, final_url, image_map) or None."""
    local_filename = url_map[src_key]
    output_path = os.path.join(OUTPUT_DIR, local_filename)

    # Try both base URLs
    url = BASE_URL + src_key
    data, final_url = fetch_url(url)
    if data is None:
        alt_url = ALT_BASE_URL + src_key
        print(f"  Trying alternate URL: {alt_url}")
        data, final_url = fetch_url(alt_url)

    if data is None:
        print(f"  SKIPPING: {src_key}")
        return None, None, None

    html_text = data.decode('utf-8', errors='replace')

    # Extract and download images
    img_urls = extract_images(html_text, final_url)
    image_map = {}
    for img_url in img_urls:
        ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.gif', '.png', '.svg', '.webp', '.ico'):
            continue
        local_name = download_image(img_url, IMAGES_DIR)
        if local_name:
            image_map[img_url] = local_name

    return html_text, final_url, image_map


def phase1_download_missing(url_map):
    """Download all missing pages."""
    print("=== Phase 1: Downloading Missing Pages ===\n")
    newly_downloaded = {}
    failed = []

    for src_key in MISSING_PAGES:
        local_filename = src_key_to_local(src_key)
        output_path = os.path.join(OUTPUT_DIR, local_filename)

        # Skip if already exists
        if os.path.exists(output_path):
            print(f"  Already exists: {local_filename}")
            newly_downloaded[src_key] = local_filename
            continue

        print(f"\nFetching: {src_key} -> {local_filename}")
        html_text, final_url, image_map = download_page(src_key, url_map)

        if html_text is None:
            failed.append(src_key)
            continue

        # Rewrite links (pass empty image_map for now, will redo in phase 2)
        html_text = rewrite_html_links(html_text, final_url, image_map, url_map)

        with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(html_text)
        print(f"  Saved: {output_path} ({len(html_text)} bytes)")
        newly_downloaded[src_key] = local_filename
        time.sleep(0.4)

    print(f"\nDownloaded: {len(newly_downloaded)} | Failed: {len(failed)}")
    if failed:
        print("Failed:", failed)
    return failed


def phase2_rewrite_existing(url_map):
    """Re-rewrite all existing htkw files to fix remaining links."""
    print("\n=== Phase 2: Rewriting Links in All Existing Files ===\n")

    html_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.html') and f != 'index.html']

    for filename in sorted(html_files):
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            html_text = f.read()

        # Count remaining htkw links before
        before_count = len(re.findall(r'nephsites/htkw/r\d+_html', html_text, re.IGNORECASE))
        before_count += len(re.findall(r'href=["\'][^"\']*nephsites/htkw/', html_text, re.IGNORECASE))

        # We need a plausible page_url for relative image resolution
        # Since we're just fixing links (not re-downloading images), pass empty image_map
        page_url = BASE_URL + filename.replace('.html', '_html')
        html_text = rewrite_html_links(html_text, page_url, {}, url_map)

        after_count = len(re.findall(r'nephsites/htkw/r\d+_html', html_text, re.IGNORECASE))
        after_count += len(re.findall(r'href=["\'][^"\']*nephsites/htkw/', html_text, re.IGNORECASE))

        with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
            f.write(html_text)

        if before_count > 0:
            print(f"  {filename}: rewrote {before_count - after_count} links ({after_count} remaining)")
        else:
            print(f"  {filename}: no htkw links found")


def update_index(url_map, failed_keys):
    """Update the htkw/index.html with the full list of pages."""
    # Build ordered list of all pages
    all_pages = []

    # First the navigation pages
    nav_order = [
        ('r1_html', 'How the Kidney Works'),
        ('r8_html', 'What the Kidneys Do'),
        ('r9_html', 'When Kidneys Fail'),
        ('r10_html', 'Chronic Kidney Disease'),
        ('r11_html', 'End Stage Renal Disease'),
        ('r33_html', 'CKD Curriculum'),
        ('r32_html', 'MDRD GFR'),
        ('r52_html', 'Self Assessment Quizes'),
        ('ckd_pcp', 'The PCP'),
        ('r12_html', 'Filter Waste Products'),
        ('r13_html', 'Regulate Fluids'),
        ('r14_html', 'Adjust Electrolytes & Acids'),
        ('r15_html', 'Activate Vitamin D'),
        ('r16_html', 'Build Red Blood Cells'),
        ('r17_html', 'Control Blood Pressure'),
    ]

    # Then add any additional downloaded pages, sorted by number
    known_keys = {k for k, _ in nav_order}
    extra_pages = []
    for key in sorted(url_map.keys()):
        if key not in known_keys and key not in failed_keys:
            local = url_map[key]
            if os.path.exists(os.path.join(OUTPUT_DIR, local)):
                extra_pages.append((key, local.replace('.html', '')))

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>How the Kidney Works - Chronic Kidney Disease</title>
<style>
body { font-family: Arial, Helvetica, sans-serif; color: #000066; background: #fff; margin: 20px; }
h1 { font-size: 24px; color: #000066; }
h2 { font-size: 18px; color: #000066; margin-top: 1.5em; }
.note { font-size: 12px; color: #666; font-style: italic; margin-bottom: 20px; }
ul { list-style-type: square; }
li { margin: 5px 0; }
a { color: #000066; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>How the Kidney Works — Chronic Kidney Disease</h1>
<p class="note">Archived from nephron.com</p>

<h2>Main Pages</h2>
<ul>
'''
    for key, title in nav_order:
        if key in failed_keys:
            html += f'  <li><span style="color:#999">{title} (not available)</span></li>\n'
        elif key in url_map and os.path.exists(os.path.join(OUTPUT_DIR, url_map[key])):
            html += f'  <li><a href="{url_map[key]}">{title}</a></li>\n'
        else:
            html += f'  <li><span style="color:#999">{title} (not available)</span></li>\n'

    if extra_pages:
        html += '</ul>\n\n<h2>Additional Pages</h2>\n<ul>\n'
        for key, label in extra_pages:
            local = url_map[key]
            html += f'  <li><a href="{local}">{label.upper()}</a></li>\n'

    html += '''</ul>

<p><a href="../patient_education/index.html">&larr; Back to Patient Education</a></p>
</body>
</html>
'''

    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, 'w') as f:
        f.write(html)
    print(f"\nUpdated index: {index_path}")


def main():
    print("=== Extended HTKW Archive ===\n")
    os.makedirs(IMAGES_DIR, exist_ok=True)

    url_map = build_full_url_map()

    failed_keys = set(phase1_download_missing(url_map))

    phase2_rewrite_existing(url_map)

    update_index(url_map, failed_keys)

    # Final count
    html_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.html') and f != 'index.html']
    images = os.listdir(IMAGES_DIR)
    print(f"\n=== Done ===")
    print(f"Total pages in htkw/: {len(html_files)}")
    print(f"Total images in htkw/images/: {len(images)}")

    # Check for any remaining broken htkw links
    remaining = []
    for filename in html_files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        matches = re.findall(r'nephsites/htkw/r\d+_html', content, re.IGNORECASE)
        if matches:
            remaining.append((filename, matches))

    if remaining:
        print(f"\nRemaining unresolved htkw links:")
        for fn, links in remaining:
            print(f"  {fn}: {links}")
    else:
        print("\nAll /nephsites/htkw/r*_html links resolved!")


if __name__ == "__main__":
    main()
