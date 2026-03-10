#!/usr/bin/env python3
"""
Check URLs from Features section for availability
"""

import urllib.request
import urllib.error
import socket

# Features section URLs
features_links = [
    {
        "title": "NIH Patient Education Videos",
        "url": "http://www.nkdep.nih.gov/professionals/providereducation/index.htm"
    },
    {
        "title": "Participate in a Kidney Study",
        "url": "http://nephron.com/nephsites/nic/kidney_study"
    },
    {
        "title": "TouchCalc",
        "url": "http://touchcalc.com"
    },
    {
        "title": "Hemodialysis Mortality Predictor - Surprise Question",
        "url": "http://nephron.com/sq"
    },
    {
        "title": "Charlson Comorbidity Index",
        "url": "http://nephron.org/cci"
    },
    {
        "title": "MDRD GFR on your website",
        "url": "http://nephron.com/mdrd_gfr_yoursite"
    },
    {
        "title": "CYSTATIN C CALCULATOR",
        "url": "http://touchcalc.com/calculators/cystatin"
    },
    {
        "title": "Follow CDC on Twitter",
        "url": "http://twitter.com/cdcemergency"
    },
    {
        "title": "Headlines archive",
        "url": "http://nephron.org/nephsites/nic/headlines"
    },
    {
        "title": "What's new at ISHD?",
        "url": "http://www.ishd.net"
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

print("Checking Features section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(features_links, 1):
    print(f"[{i}/{len(features_links)}] Checking: {link['title']}")
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
