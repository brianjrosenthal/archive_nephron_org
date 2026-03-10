#!/usr/bin/env python3
"""
Check URLs from Regulatory References section for availability
"""

import urllib.request
import urllib.error
import socket

# Regulatory References section URLs
regulatory_links = [
    {
        "title": "CMS (Centers for Medicare & Medicaid Services)",
        "url": "http://www.cms.gov/"
    },
    {
        "title": "ESRD Networks",
        "url": "http://www.esrdnetworks.org/"
    },
    {
        "title": "ESRD NCC (Network Coordinating Council)",
        "url": "http://www.esrdncc.org/"
    },
    {
        "title": "Conditions for Coverage",
        "url": "http://www.cms.gov/CFCsAndCoPs/06_ESRD.asp"
    },
    {
        "title": "OPTN (Organ Procurement and Transplantation Network)",
        "url": "http://optn.transplant.hrsa.gov/"
    },
    {
        "title": "FDA (Food and Drug Administration)",
        "url": "http://www.fda.gov/"
    },
    {
        "title": "CDC (Centers for Disease Control and Prevention)",
        "url": "http://www.cdc.gov/"
    },
    {
        "title": "OSHA (Occupational Safety and Health Administration)",
        "url": "http://www.osha.gov/"
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

print("Checking Regulatory References section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(regulatory_links, 1):
    print(f"[{i}/{len(regulatory_links)}] Checking: {link['title']}")
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
