#!/usr/bin/env python3
"""
Check URLs from General References section for availability
"""

import urllib.request
import urllib.error
import socket

# General References section URLs
general_links = [
    {
        "title": "Medline Plus",
        "url": "http://www.nlm.nih.gov/medlineplus/"
    },
    {
        "title": "PubMed",
        "url": "http://www.ncbi.nlm.nih.gov/entrez/query.fcgi"
    },
    {
        "title": "Google Scholar",
        "url": "http://scholar.google.com/"
    },
    {
        "title": "Wikipedia",
        "url": "http://www.wikipedia.org/"
    },
    {
        "title": "WebMD",
        "url": "http://www.webmd.com/"
    },
    {
        "title": "eMedicine",
        "url": "http://www.emedicine.com/"
    },
    {
        "title": "MedlinePlus Drug Information",
        "url": "http://www.nlm.nih.gov/medlineplus/druginformation.html"
    },
    {
        "title": "RxList",
        "url": "http://www.rxlist.com/"
    },
    {
        "title": "Drugs.com",
        "url": "http://www.drugs.com/"
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

print("Checking General References section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(general_links, 1):
    print(f"[{i}/{len(general_links)}] Checking: {link['title']}")
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
