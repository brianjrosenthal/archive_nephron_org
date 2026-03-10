#!/usr/bin/env python3
"""
Check URLs from News Around the Web section for availability
"""

import urllib.request
import urllib.error
import socket

# News Around the Web section URLs
news_links = [
    {
        "title": "Renal & Urology News",
        "url": "http://www.renalandurologynews.com/"
    },
    {
        "title": "Nephrology Times",
        "url": "http://www.nephrologytimes.com/"
    },
    {
        "title": "Nephrology News & Issues",
        "url": "http://www.nephrologynews.com/"
    },
    {
        "title": "Google News - Kidney Disease",
        "url": "http://news.google.com/news?hl=en&ned=us&q=kidney+disease&btnG=Search+News"
    },
    {
        "title": "Reuters Health",
        "url": "http://www.reutershealth.com/"
    },
    {
        "title": "Medical News Today",
        "url": "http://www.medicalnewstoday.com/"
    },
    {
        "title": "ScienceDaily",
        "url": "http://www.sciencedaily.com/"
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

print("Checking News Around the Web section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(news_links, 1):
    print(f"[{i}/{len(news_links)}] Checking: {link['title']}")
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
