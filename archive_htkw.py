#!/usr/bin/env python3
"""
Archive the "How the Kidney Works" section from nephron.com.
Downloads all pages and their images into htkw/ directory.
"""

import os
import re
import urllib.request
import urllib.parse
import urllib.error
import time
import shutil
from html.parser import HTMLParser

# Pages to download (relative to htkw base URL)
BASE_URL = "http://www.nephron.com/nephsites/htkw/"
ALT_BASE_URL = "http://www.nephron.org/nephsites/htkw/"

PAGES = [
    ("r0_html", "r0.html", "Introduction"),
    ("r1_html", "r1.html", "How the Kidney Works"),
    ("r8_html", "r8.html", "What the Kidneys Do"),
    ("r9_html", "r9.html", "When Kidneys Fail"),
    ("r10_html", "r10.html", "Chronic Kidney Disease"),
    ("r11_html", "r11.html", "End Stage Renal Disease"),
    ("r33_html", "r33.html", "CKD Curriculum"),
    ("r32_html", "r32.html", "MDRD GFR"),
    ("r52_html", "r52.html", "Self Assessment Quizes"),
    ("ckd_pcp", "ckd_pcp.html", "The PCP"),
    ("r12_html", "r12.html", "Filter Waste Products"),
    ("r13_html", "r13.html", "Regulate Fluids"),
    ("r14_html", "r14.html", "Adjust Electrolytes & Acids"),
    ("r15_html", "r15.html", "Activate Vitamin D"),
    ("r16_html", "r16.html", "Build Red Blood Cells"),
    ("r17_html", "r17.html", "Control Blood Pressure"),
]

OUTPUT_DIR = "htkw"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")


def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)


def fetch_url(url, retries=2):
    """Fetch a URL and return (content_bytes, final_url). Returns (None, url) on failure."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
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
    """Extract all image src URLs from HTML."""
    # Find all img src attributes
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
    # Also find background images
    bg_srcs = re.findall(r'background(?:-image)?=["\']([^"\']+)["\']', html_text, re.IGNORECASE)
    bg_url = re.findall(r'url\(["\']?([^"\')\s]+)["\']?\)', html_text, re.IGNORECASE)
    
    all_srcs = img_srcs + bg_srcs + bg_url
    
    # Resolve relative URLs
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
    """Download an image and return the local filename, or None on failure."""
    # Get just the filename
    parsed = urllib.parse.urlparse(img_url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return None
    
    # Handle query strings in filename
    filename = re.sub(r'[?#].*$', '', filename)
    
    local_path = os.path.join(images_dir, filename)
    
    # Skip if already downloaded
    if os.path.exists(local_path):
        print(f"  Image already exists: {filename}")
        return filename
    
    print(f"  Downloading image: {img_url} -> {filename}")
    data, _ = fetch_url(img_url)
    if data:
        with open(local_path, 'wb') as f:
            f.write(data)
        return filename
    return None


def rewrite_html(html_text, page_url, image_map):
    """Rewrite HTML to use local paths."""
    
    # Rewrite image src attributes
    def replace_img_src(m):
        src = m.group(1)
        if src.startswith('data:'):
            return m.group(0)
        # Resolve the URL
        if src.startswith('http://') or src.startswith('https://'):
            abs_url = src
        elif src.startswith('//'):
            abs_url = 'http:' + src
        else:
            abs_url = urllib.parse.urljoin(page_url, src)
        
        if abs_url in image_map:
            local_name = image_map[abs_url]
            return m.group(0).replace(src, f'images/{local_name}')
        return m.group(0)
    
    # Replace img src
    html_text = re.sub(r'<img([^>]+)src=["\']([^"\']+)["\']', 
                       lambda m: rewrite_img(m, page_url, image_map), 
                       html_text, flags=re.IGNORECASE)
    
    # Rewrite navigation links pointing to htkw pages
    # Map from original URL fragments to local filenames
    htkw_url_map = {
        'r0_html': 'r0.html',
        'r1_html': 'r1.html',
        'r8_html': 'r8.html',
        'r9_html': 'r9.html',
        'r10_html': 'r10.html',
        'r11_html': 'r11.html',
        'r33_html': 'r33.html',
        'r32_html': 'r32.html',
        'r52_html': 'r52.html',
        'ckd_pcp': 'ckd_pcp.html',
        'r12_html': 'r12.html',
        'r13_html': 'r13.html',
        'r14_html': 'r14.html',
        'r15_html': 'r15.html',
        'r16_html': 'r16.html',
        'r17_html': 'r17.html',
    }
    
    # Rewrite htkw links in href attributes
    def replace_htkw_href(m):
        href = m.group(1) or m.group(2)
        quote = '"' if m.group(1) is not None else "'"
        
        for key, local in htkw_url_map.items():
            if key in href and 'htkw' in href:
                return f'href={quote}{local}{quote}'
        return m.group(0)
    
    html_text = re.sub(
        r'href="([^"]*(?:nephron\.com|nephron\.org)/nephsites/htkw/[^"]*)"',
        lambda m: rewrite_htkw_link(m, htkw_url_map, '"'),
        html_text, flags=re.IGNORECASE
    )
    html_text = re.sub(
        r"href='([^']*(?:nephron\.com|nephron\.org)/nephsites/htkw/[^']*)'",
        lambda m: rewrite_htkw_link(m, htkw_url_map, "'"),
        html_text, flags=re.IGNORECASE
    )
    # Also handle /nephsites/htkw/ relative links
    html_text = re.sub(
        r'href="(/nephsites/htkw/[^"]*)"',
        lambda m: rewrite_htkw_link_rel(m, htkw_url_map, '"'),
        html_text, flags=re.IGNORECASE
    )
    html_text = re.sub(
        r"href='(/nephsites/htkw/[^']*)'",
        lambda m: rewrite_htkw_link_rel(m, htkw_url_map, "'"),
        html_text, flags=re.IGNORECASE
    )
    
    return html_text


def rewrite_img(m, page_url, image_map):
    """Replace an img tag's src with the local path."""
    full_tag = m.group(0)
    # Find src in the tag
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
        return full_tag.replace(src, f'images/{local_name}')
    return full_tag


def rewrite_htkw_link(m, url_map, quote):
    """Rewrite an absolute htkw href to local filename."""
    href = m.group(1)
    for key, local in url_map.items():
        if href.endswith('/' + key) or href.endswith('/' + key + '/'):
            return f'href={quote}{local}{quote}'
    return m.group(0)


def rewrite_htkw_link_rel(m, url_map, quote):
    """Rewrite a relative /nephsites/htkw/xxx href to local filename."""
    href = m.group(1)
    for key, local in url_map.items():
        if href.endswith('/' + key) or href.endswith('/' + key + '/'):
            return f'href={quote}{local}{quote}'
    return m.group(0)


def process_page(src_key, local_filename, title):
    """Download a page and all its images."""
    # Try both base URLs
    url = BASE_URL + src_key
    print(f"\nFetching: {title} ({url})")
    
    data, final_url = fetch_url(url)
    if data is None:
        # Try alternate base URL
        alt_url = ALT_BASE_URL + src_key
        print(f"  Trying alternate URL: {alt_url}")
        data, final_url = fetch_url(alt_url)
    
    if data is None:
        print(f"  SKIPPING: Could not fetch {title}")
        return False
    
    html_text = data.decode('utf-8', errors='replace')
    
    # Extract and download images
    img_urls = extract_images(html_text, final_url)
    image_map = {}
    
    for img_url in img_urls:
        # Skip non-image-looking URLs
        ext = os.path.splitext(urllib.parse.urlparse(img_url).path)[1].lower()
        if ext not in ('.jpg', '.jpeg', '.gif', '.png', '.svg', '.webp', '.ico'):
            continue
        local_name = download_image(img_url, IMAGES_DIR)
        if local_name:
            image_map[img_url] = local_name
    
    # Rewrite HTML
    html_text = rewrite_html(html_text, final_url, image_map)
    
    # Save
    output_path = os.path.join(OUTPUT_DIR, local_filename)
    with open(output_path, 'w', encoding='utf-8', errors='replace') as f:
        f.write(html_text)
    
    print(f"  Saved: {output_path} ({len(html_text)} bytes, {len(image_map)} images)")
    return True


def create_index(successful_pages):
    """Create an index.html for the htkw section."""
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>How the Kidney Works - Chronic Kidney Disease</title>
<style>
body { font-family: Arial, Helvetica, sans-serif; color: #000066; background: #fff; margin: 20px; }
h1 { font-size: 24px; color: #000066; }
h2 { font-size: 18px; color: #000066; }
.note { font-size: 12px; color: #666; font-style: italic; margin-bottom: 20px; }
ul { list-style-type: square; }
li { margin: 6px 0; }
a { color: #000066; text-decoration: none; }
a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>How the Kidney Works — Chronic Kidney Disease</h1>
<p class="note">Archived from nephron.com</p>

<h2>Pages in this Section</h2>
<ul>
'''
    
    for src_key, local_filename, title in successful_pages:
        html += f'  <li><a href="{local_filename}">{title}</a></li>\n'
    
    html += '''</ul>

<p><a href="../patient_education/index.html">&larr; Back to Patient Education</a></p>
</body>
</html>
'''
    
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, 'w') as f:
        f.write(html)
    print(f"\nCreated index: {index_path}")


def main():
    print("=== Archiving How the Kidney Works (HTKW) ===\n")
    ensure_dirs()
    
    successful = []
    failed = []
    
    for src_key, local_filename, title in PAGES:
        success = process_page(src_key, local_filename, title)
        if success:
            successful.append((src_key, local_filename, title))
        else:
            failed.append((src_key, local_filename, title))
        time.sleep(0.5)  # Be polite
    
    create_index(successful)
    
    print("\n=== Summary ===")
    print(f"Successfully downloaded: {len(successful)} pages")
    print(f"Failed: {len(failed)} pages")
    
    if failed:
        print("\nFailed pages:")
        for src_key, local_filename, title in failed:
            print(f"  - {title} ({src_key})")
    
    # List downloaded images
    images = os.listdir(IMAGES_DIR)
    print(f"\nDownloaded {len(images)} images to {IMAGES_DIR}/")


if __name__ == "__main__":
    main()
