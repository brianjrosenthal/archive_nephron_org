#!/usr/bin/env python3
"""
Audit all links in htkw/ files.
Find all href values pointing to /nephsites/* on nephron.com or nephron.org.
"""

import os
import re
import glob

files = sorted(glob.glob("htkw/*.html"))
nephsites_links = set()
all_external_links = set()

for f in files:
    with open(f, encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    
    # Find all href values
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    
    for href in hrefs:
        # Skip anchor-only links
        if href.startswith("#"):
            continue
        
        # Normalize relative /nephsites/ links
        if href.startswith("/nephsites/"):
            href = "http://www.nephron.org" + href
        
        # Check if it's a nephsites link
        if "nephron.com/nephsites/" in href or "nephron.org/nephsites/" in href:
            # Skip htkw links (already archived)
            if "/nephsites/htkw/" not in href:
                nephsites_links.add(href.strip())
        
        # Track all external links for reference
        if href.startswith("http"):
            all_external_links.add(href.strip())

print("=" * 70)
print("NEPHSITES LINKS (excluding htkw - candidates for archiving)")
print("=" * 70)
for link in sorted(nephsites_links):
    print(f"  {link}")

print(f"\nTotal nephsites links (non-htkw): {len(nephsites_links)}")

print("\n" + "=" * 70)
print("ALL EXTERNAL LINKS (for reference)")  
print("=" * 70)
for link in sorted(all_external_links):
    print(f"  {link}")

print(f"\nTotal external links: {len(all_external_links)}")
