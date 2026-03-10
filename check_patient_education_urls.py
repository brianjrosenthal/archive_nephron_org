#!/usr/bin/env python3
"""
Check URLs from Patient Education section for availability
"""

import urllib.request
import urllib.error
import socket

# Patient Education section URLs
patient_education_links = [
    {
        "title": "Kidney Disease Education - NKDEP",
        "url": "http://www.nkdep.nih.gov/"
    },
    {
        "title": "National Kidney Foundation - Patient Resources",
        "url": "http://www.kidney.org/atoz/"
    },
    {
        "title": "American Kidney Fund - Patient Education",
        "url": "http://www.kidneyfund.org/kidney-health/"
    },
    {
        "title": "AAKP - Patient Resources",
        "url": "http://www.aakp.org/aakp-library/"
    },
    {
        "title": "Life Options - Rehabilitation Program",
        "url": "http://www.lifeoptions.org/"
    },
    {
        "title": "The Kidney School",
        "url": "http://www.kidneyschool.org/"
    },
    {
        "title": "Home Dialysis Central",
        "url": "http://www.homedialysis.org/"
    }
]

def check_url(url, timeout=10):
    """Check if URL is accessible"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        return True, response.getcode()
    except urllib.error.HTTPError as e:
        return False, e.code
    except urllib.error.URLError as e:
        return False, str(e.reason)
    except socket.timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

print("Checking Patient Education section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(patient_education_links, 1):
    print(f"[{i}/{len(patient_education_links)}] Checking: {link['title']}")
    print(f"    URL: {link['url']}")
    
    is_working, status = check_url(link['url'])
    
    if is_working:
        print(f"    ✓ Status: {status} (Working)")
        working.append(link)
    else:
        print(f"    ✗ Status: {status} (BROKEN)")
        broken.append({**link, 'error': status})
    
    print()

print("=" * 70)
print(f"\nSUMMARY:")
print(f"  Working links: {len(working)}")
print(f"  Broken links: {len(broken)}")

if broken:
    print(f"\n⚠️  BROKEN LINKS:")
    for link in broken:
        print(f"  - {link['title']}")
        print(f"    {link['url']}")
        print(f"    Error: {link['error']}")
        print()
