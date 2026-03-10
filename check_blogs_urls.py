#!/usr/bin/env python3
"""
Check URLs from Blogs section for availability
"""

import urllib.request
import urllib.error
import socket

# Blogs section URLs
blogs_links = [
    {
        "title": "Kidney Blog (kidneyblog.com)",
        "url": "http://kidneyblog.com"
    },
    {
        "title": "Bill Peckham - Dialysis from the Sharp End of the Needle",
        "url": "http://www.billpeckham.com/"
    },
    {
        "title": "Renal Fellow Blogspot",
        "url": "http://renalfellow.blogspot.com/"
    },
    {
        "title": "Brady Augustine - MedicaidFirstAid",
        "url": "http://www.medicaidfirstaid.com/"
    },
    {
        "title": "Blog - The Renal Unit",
        "url": "http://therenalunit.com/renalblogs.php"
    },
    {
        "title": "Kidney Notes",
        "url": "http://www.kidneynotes.com/"
    },
    {
        "title": "Uremic Frost",
        "url": "http://www.uremicfrost.com/"
    },
    {
        "title": "Clinical Cases - Nephrology",
        "url": "http://clinicalcases.org/2005/07/nephrology-cases.html/"
    },
    {
        "title": "Precious Body Fluids",
        "url": "http://www.pbfluids.com//"
    },
    {
        "title": "BFH - Blog for Health",
        "url": "http://profcentral.blogspot.com/"
    },
    {
        "title": "uKidney",
        "url": "http://www.ukidney.com"
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

print("Checking Blogs section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(blogs_links, 1):
    print(f"[{i}/{len(blogs_links)}] Checking: {link['title']}")
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
