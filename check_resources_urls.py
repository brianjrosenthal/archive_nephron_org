#!/usr/bin/env python3
"""
Check URLs from Resources section for availability
"""

import urllib.request
import urllib.error
import socket

# Resources section URLs
resources_links = [
    {
        "title": "Kidney Disease Education",
        "url": "http://www.nkdep.nih.gov/"
    },
    {
        "title": "National Kidney Foundation",
        "url": "http://www.kidney.org/"
    },
    {
        "title": "American Society of Nephrology",
        "url": "http://www.asn-online.org/"
    },
    {
        "title": "National Institute of Diabetes and Digestive and Kidney Diseases",
        "url": "http://www2.niddk.nih.gov/"
    },
    {
        "title": "Renal Physicians Association",
        "url": "http://www.renalmd.org/"
    },
    {
        "title": "American Association of Kidney Patients",
        "url": "http://www.aakp.org/"
    },
    {
        "title": "Nephrology Channel",
        "url": "http://www.healthcommunities.com/kidney-disease/overview-of-kidney-disease.shtml"
    },
    {
        "title": "Medscape Nephrology",
        "url": "http://www.medscape.com/nephrology"
    },
    {
        "title": "eMedicine Nephrology",
        "url": "http://emedicine.medscape.com/nephrology"
    },
    {
        "title": "Kidney Atlas",
        "url": "http://www.kidneyatlas.org/"
    },
    {
        "title": "American Kidney Fund",
        "url": "http://www.kidneyfund.org/"
    },
    {
        "title": "The Kidney School",
        "url": "http://www.kidneyschool.org/"
    },
    {
        "title": "Life Options",
        "url": "http://www.lifeoptions.org/"
    },
    {
        "title": "The Kidney Information Clearinghouse",
        "url": "http://kidney.niddk.nih.gov/"
    },
    {
        "title": "Kidney Patient Guide",
        "url": "http://www.kidneypatientguide.org.uk/"
    },
    {
        "title": "PKD Foundation",
        "url": "http://www.pkdcure.org/"
    },
    {
        "title": "IgA Nephropathy Support Network",
        "url": "http://www.igan.org/"
    },
    {
        "title": "Renal Support Network",
        "url": "http://www.rsnhope.org/"
    },
    {
        "title": "Home Dialysis Central",
        "url": "http://www.homedialysis.org/"
    },
    {
        "title": "International Society for Peritoneal Dialysis",
        "url": "http://www.ispd.org/"
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

print("Checking Resources section URLs...\n")
print("=" * 70)

working = []
broken = []

for i, link in enumerate(resources_links, 1):
    print(f"[{i}/{len(resources_links)}] Checking: {link['title']}")
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
