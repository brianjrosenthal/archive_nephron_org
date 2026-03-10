#!/usr/bin/env python3
"""
Standardize the 10 main HTKW pages:
- Simplified left nav (10 items only)
- Consistent navy (#000088) background
- No white backgrounds on visited/hover link states that hide text
- Extract main content from existing pages and rewrap in standard template
"""

import os
import re

OUTPUT_DIR = "htkw"

# The 10 pages to standardize
PAGES = [
    ("r0.html",       "Introduction"),
    ("r1.html",       "How the Kidney Works"),
    ("r8.html",       "What the Kidneys Do"),
    ("r9.html",       "When Kidneys Fail"),
    ("r10.html",      "Chronic Kidney Disease"),
    ("r11.html",      "End Stage Renal Disease"),
    ("r33.html",      "CKD Curriculum"),
    ("r32.html",      "MDRD GFR"),
    ("r52.html",      "Self-Assessment Quizzes"),
    ("ckd_pcp.html",  "The PCP"),
]

# Standardized left nav (simplified to 10 items)
LEFT_NAV = """<div class="leftlink">
        <h2 class="leftlink">CHRONIC<br>KIDNEY<br>DISEASE</h2>
        <a class="leftlink" href="r0.html">Introduction</a>
        <a class="leftlink" href="r1.html">How the Kidney Works</a>
        <a class="leftlink" href="r8.html">What the Kidneys Do</a>
        <a class="leftlink" href="r9.html">When Kidneys Fail</a>
        <a class="leftlink" href="r10.html">Chronic Kidney Disease</a>
        <a class="leftlink" href="r11.html">End Stage Renal Disease</a>
        <a class="leftlink" href="r33.html">CKD Curriculum</a>
        <a class="leftlink" href="r32.html">MDRD GFR</a>
        <a class="leftlink" href="r52.html">Self-Assessment Quizzes</a>
        <a class="leftlink" href="ckd_pcp.html">The PCP</a>
</div>"""

# Standardized CSS block
STANDARD_CSS = """<style type="text/css">

body {
    font-family: arial, helvetica, sans-serif, verdana;
    background-color: #000088;
    color: white;
    margin: 0;
    padding: 0;
}

* { font-family: arial, helvetica, sans-serif, verdana; font-size: 12px; color: white; font-weight: normal; }

/* Override body text for left nav area */
.leftlink, a.leftlink {
    display: block;
    width: 130px;
    text-decoration: none;
    text-align: left;
    margin: 0px;
    padding: 3px 2px;
    font-size: 11px;
    color: #000066;
    background-color: #d3cece;
    border: 0px;
    font-family: Arial, Helvetica, sans-serif;
}
h2.leftlink {
    font-size: 13px;
    font-weight: bold;
    color: #000066;
    background-color: #d3cece;
    margin: 0;
    padding: 4px 2px;
}
a.leftlink:hover {
    background-color: #000066;
    color: #d3cece;
    text-decoration: none;
}
a.leftlink:visited {
    color: #000066;
    background-color: #d3cece;
    text-decoration: none;
}

/* Main content area */
div#htkwmain {
    display: block;
    background-color: #000088;
    color: white;
    margin: 0px;
}

p, li, ul, ol {
    font-family: helvetica, arial, sans-serif;
    font-size: 14px;
    color: white;
    text-align: left;
}

h1 { font-size: 30px; font-weight: bold; color: white; }
h2 { font-size: 24px; font-weight: bold; color: white; }
h3 { font-size: 20px; font-weight: bold; color: yellow; }
h4 { font-size: 16px; font-weight: bold; color: white; }

ul { list-style-type: square; }
ol { list-style-type: decimal; }

a { color: #aaddff; text-decoration: none; }
a:hover { color: white; text-decoration: underline; }
a:visited { color: #aaddff; }

/* TOC / content links */
a.toc {
    display: block;
    text-decoration: none;
    margin: 3px;
    padding: 4px 6px;
    font-weight: bold;
    font-size: 14px;
    color: white;
    background-color: #000055;
    border: 1px solid #334488;
}
a.toc:hover {
    background-color: #334488;
    color: white;
    text-decoration: none;
}
a.toc:visited {
    color: #ccddff;
    background-color: #000055;
}

/* CKD content class */
.ckd { font-size: 14px; font-weight: bold; color: white; }
a.ckd { color: #aaddff; }
a.ckd:hover { color: white; background-color: #334488; text-decoration: none; }
a.ckd:visited { color: #ccddff; }
h1.ckd { font-size: 30px; font-weight: bold; color: white; }
h2.ckd { font-size: 24px; font-weight: bold; color: white; }
h3.ckd { font-size: 20px; font-weight: bold; color: yellow; }
p.ckd, li.ckd { font-size: 14px; color: white; }

/* Footer */
.twelve_px { font-size: 12px; color: #cccccc; }
a.twelve_px { font-size: 12px; color: #aaddff; }
a.twelve_px:hover { color: white; text-decoration: underline; }
a.twelve_px:visited { color: #ccddff; }

#image { float: right; margin: 0 0 10px 16px; }
#heart { display: block; float: left; clear: right; }

.red_line { color: red; background-color: red; height: 1px; width: 100%; border: 0; margin: 8px 0; }

</style>"""


def extract_main_content(html_text, filename):
    """
    Extract the main content from the page (the middle/right portion of the layout).
    Returns the content HTML string.
    """
    # Strategy: find the htkwmain div, then find the second/main td content
    # Look for content between left nav closing </div> and the end of main table </table>
    
    # First try to find the table row after the left nav div
    # The left nav is always in the first <td>, content in the second <td>
    
    # Try pattern: find after </div> that closes leftlink, up to </table> or end of htkwmain
    
    # Look for the second <td valign="top"> after the nav div
    # Common patterns in the downloaded pages:
    # Pattern 1: <td valign="top"><h1...> (the main content td)
    
    # Find the leftlink div block
    nav_end = re.search(r'</div>\s*\n\s*</td>', html_text, re.IGNORECASE)
    if not nav_end:
        # Try alternate pattern
        nav_end = re.search(r'nephron\.com/index\.shtml[^<]*</A>\s*\n?\s*</div>', html_text, re.IGNORECASE)
    
    if nav_end:
        after_nav = html_text[nav_end.end():]
        # Now find the opening of the next td (main content)
        content_td = re.search(r'<td[^>]*>', after_nav, re.IGNORECASE)
        if content_td:
            content_start = content_td.end()
            # Find the end - look for </table> that closes the main layout table
            # or </td> followed by </tr> followed by </table>
            content_after = after_nav[content_start:]
            
            # Find end of content - look for closing of the main row
            # Try to find </td></tr></table> or </td> </tr>
            end_match = re.search(r'</td>\s*(<td[^>]*>.*?</td>\s*)?</tr>\s*</table>', 
                                  content_after, re.IGNORECASE | re.DOTALL)
            if end_match:
                content = content_after[:end_match.start()]
            else:
                # Fallback: take until <br clear or <table width=100% or footer
                end_match2 = re.search(r'<br\s+clear|<table[^>]+class="twelve_px"|<hr\s+class', 
                                       content_after, re.IGNORECASE)
                if end_match2:
                    content = content_after[:end_match2.start()]
                else:
                    content = content_after[:5000]  # fallback
            
            return content.strip()
    
    # Fallback for pages with different structure (our created pages r0, r1)
    # Look for content after the nav div closing
    alt_match = re.search(r'</div>\s*\n\s*</td>\s*\n<td[^>]*>(.*?)</td>\s*\n</tr>', 
                          html_text, re.IGNORECASE | re.DOTALL)
    if alt_match:
        return alt_match.group(1).strip()
    
    return ""


def build_page(filename, title, content):
    """Build a standardized page with the given title and content."""
    
    return f"""<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>{title} - Nephron.com Archive</TITLE>
{STANDARD_CSS}
</HEAD>
<BODY>

<table align="center" style="border-collapse:collapse;border:0;background-color:black;" width="100%">
<tr><td>
<img src="images/banner5.jpg" alt="Nephron.com - Kidney Resource Page">
</td></tr>
</table>

<div id="htkwmain">
<table width="100%" style="border-collapse:collapse;" cellpadding="0" cellspacing="0">
<tr>
<td valign="top" style="width:136px;background-color:#d3cece;padding:4px;">
{LEFT_NAV}
</td>
<td valign="top" style="padding:12px;background-color:#000088;">
{content}
</td>
</tr>
</table>
</div>

<br clear="all">
<hr class="red_line">
<div style="background-color:#000044;padding:6px;text-align:center;">
<span class="twelve_px">
<a class="twelve_px" href="nic_service.html">About The Nephron Information Center</a>
&nbsp;|&nbsp;
<a class="twelve_px" href="mailto:fadem@nephron.com">Contact Webmaster</a>
&nbsp;|&nbsp;
<a class="twelve_px" href="../patient_education/index.html">&larr; Patient Education</a>
&nbsp;|&nbsp;
<a class="twelve_px" href="index.html">HTKW Index</a>
</span><br>
<span style="font-size:11px;color:#999999;">&copy; Nephron Information Center. All Rights Reserved.</span>
</div>

</BODY>
</HTML>
"""


def standardize_page(filename, title):
    """Read, extract content, rebuild, and save a page."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        html_text = f.read()
    
    content = extract_main_content(html_text, filename)
    
    if not content:
        print(f"  WARNING: Could not extract content from {filename}, using full body fallback")
        # Fallback: try to get body content
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_text, re.IGNORECASE | re.DOTALL)
        if body_match:
            content = body_match.group(1)
            # Strip banner table
            content = re.sub(r'<table[^>]+background-color:black[^>]*>.*?</table>', '', 
                             content, flags=re.IGNORECASE | re.DOTALL)
        else:
            content = f"<h1 style='color:white'>{title}</h1><p style='color:white'>Content pending.</p>"
    
    # Clean up the content:
    # 1. Remove any remaining htkwmain div wrappers
    content = re.sub(r'<div id="htkwmain">', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</div>\s*$', '', content.strip(), flags=re.IGNORECASE)
    
    # 2. Fix inline color:white on existing h1/h2/h3/p tags to use our CSS instead
    # (just clean up redundant inline styles - leave them if they're setting yellow/other colors)
    content = re.sub(r'style="color:white;font-size:30[^"]*"', 'class="ckd"', content, flags=re.IGNORECASE)
    content = re.sub(r'style="color:white;font-size:24[^"]*"', 'class="ckd"', content, flags=re.IGNORECASE)
    
    # 3. Fix any absolute image paths to local
    content = re.sub(r'src="[^"]*/(banner5\.jpg|circ\.gif|gloms\.gif|mallardwhite\.jpg|nephron1\.gif|nictitle1\.gif)"',
                     lambda m: f'src="images/{m.group(1)}"', content, flags=re.IGNORECASE)
    
    # 4. Ensure h1 has white color
    content = re.sub(r'(<h1)(?![^>]*class)(?![^>]*color)([^>]*>)',
                     r'\1 style="color:white;font-size:28px;"\2', content, flags=re.IGNORECASE)
    
    new_html = build_page(filename, title, content)
    
    with open(filepath, "w", encoding="utf-8", errors="replace") as f:
        f.write(new_html)
    
    print(f"  Standardized: {filename} ({len(content)} bytes of content)")


def main():
    print("=== Standardizing HTKW Main Pages ===\n")
    
    for filename, title in PAGES:
        print(f"\nProcessing: {filename} ({title})")
        standardize_page(filename, title)
    
    print(f"\n=== Done: {len(PAGES)} pages standardized ===")


if __name__ == "__main__":
    main()
