#!/usr/bin/env python3
"""
Check URLs from Events section for availability
"""

import urllib.request
import urllib.error
import socket

# Events section URLs
events_links = [
    {
        "title": "American Society of Nephrology (ASN) - Kidney Week",
        "url": "http://www.asn-online.org/education_and_meetings/"
    },
    {
        "title": "National Kidney Foundation (NKF) Spring Clinical Meetings",
        "url": "http://www.kidney.org/professionals/cme/springclinical.cfm"
    },
    {
        "title": "Renal Physicians Association (RPA)",
        "url": "http://www.renalmd.org/displaycommon.cfm?an=1&subarticlenbr=37"
    },
    {
        "title": "American Association of Kidney Patients (AAKP)",
        "url": "http://www.aakp.org/aakp-and-you/annual-meeting/"
    },
    {
        "title": "International Society of Nephrology (ISN)",
        "url": "http://www.isn-online.org/site/cms"
    },
    {
        "title": "ERA-EDTA (European Renal Association)",
        "url": "http://www.era-edta.org/"
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

print("Checking Events section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(events_links, 1):
    print(f"[{i}/{len(events_links)}] Checking: {link['title']}")
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
