#!/usr/bin/env python3
"""
Archive ZEN and Dialysis at Home and Please be Careful with my Veins pages
"""

import re
import urllib.request
import os
from bs4 import BeautifulSoup
import time

os.makedirs('/Users/brianrosenthal/vibe_coding/archive/patient_education/images', exist_ok=True)

pages = [
    {
        'url': 'http://www.nephron.org/nephsites/nic/zen_weintraub.html',
        'filename': 'zen_dialysis.html',
        'title': 'ZEN and Dialysis at Home'
    },
    {
        'url': 'http://www.nephron.org/nephsites/nic/saving_veins.html',
        'filename': 'saving_veins.html',
        'title': 'Please be Careful with my Veins'
    }
]

for page in pages:
    print(f"\n{'='*70}")
    print(f"Processing: {page['title']}")
    print(f"{'='*70}")
    
    url = page['url']
    print(f"Downloading {url}...")
    
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode('iso-8859-1')
        print("✓ Downloaded")
    except Exception as e:
        print(f"✗ Failed to download: {e}")
        continue
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script tags
    for script in soup.find_all('script'):
        script.decompose()
    
    # Remove footer content
    for element in soup.find_all(['table', 'div'], class_=re.compile('twelve_px|footer')):
        element.decompose()
    
    # Find images in content and download them
    images_found = []
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if not src or 'HONcode' in src or 'honcode' in src:
            continue
            
        # Convert relative URLs to absolute
        if src.startswith('/'):
            src = 'http://nephron.com' + src
        elif not src.startswith('http'):
            src = 'http://nephron.com/' + src
        
        # Extract filename
        filename = os.path.basename(src.split('?')[0])
        if filename and filename not in [f for _, f in images_found]:
            images_found.append((src, filename))
    
    # Download images
    for img_url, img_filename in images_found:
        try:
            print(f"  Downloading image: {img_filename}...")
            urllib.request.urlretrieve(img_url, f'/Users/brianrosenthal/vibe_coding/archive/patient_education/images/{img_filename}')
            print(f"  ✓ Downloaded {img_filename}")
        except Exception as e:
            print(f"  ✗ Failed to download {img_filename}: {e}")
    
    # Extract main content
    body_content = soup.find('body')
    content_parts = []
    if body_content:
        for elem in body_content.find_all(['p', 'h1', 'h2', 'h3', 'div', 'blockquote', 'ul', 'ol', 'img', 'br']):
            # Skip footer/header
            if elem.find('a', href=re.compile(r'HONcode|service\.html|mailto|fadem@')):
                continue
            if 'twelve_px' in str(elem.get('class', [])):
                continue
            if elem.find('script'):
                continue
            
            # Skip navigation menus
            elem_text = elem.get_text().lower()
            if 'nephron.com' in elem_text and 'food values' in elem_text:
                continue
            if 'wikipedia' in elem_text and 'search' in str(elem):
                continue
            
            # Clean up image src paths
            for img in elem.find_all('img'):
                src = img.get('src', '')
                if src:
                    # Remove external links from images
                    if 'kidney57.gif' in src or 'nictitle' in src.lower():
                        continue
                    if '/images/' in src:
                        img_name = os.path.basename(src)
                        img['src'] = f'images/{img_name}'
                    
            content_parts.append(str(elem))
        
        content_html = '\n'.join(content_parts)
    
    # Create clean HTML
    clean_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<style>
body {{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  color: #132B77;
  background: #fff;
  max-width: 900px;
  margin: 2em auto;
  padding: 1em 2em;
  line-height: 1.6;
}}
h1 {{
  font-size: 30px;
  color: #132B77;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1em;
}}
h2 {{
  font-size: 24px;
  color: #132B77;
  margin-top: 1.5em;
}}
p {{
  margin: 1em 0;
  text-align: justify;
}}
img {{
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
}}
ul, ol {{
  margin: 1em 0;
  padding-left: 2em;
}}
.footer {{
  margin-top: 3em;
  padding-top: 1em;
  border-top: 1px solid #ccc;
  font-size: 14px;
  color: #666;
  text-align: center;
}}
</style>
</head>
<body>

<h1>{page['title']}</h1>

{content_html}

<div class="footer">
  <p><a href="index.html">← Back to Patient Education</a></p>
  <p>Original content © Nephron Information Center | Archived March 2026</p>
</div>

</body>
</html>
"""
    
    # Save the clean HTML
    output_path = f'/Users/brianrosenthal/vibe_coding/archive/patient_education/{page["filename"]}'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(clean_html)
    
    print(f"✓ Created {page['filename']}")
    time.sleep(1)  # Be nice to the server

print(f"\n{'='*70}")
print("Both pages processed successfully!")
print(f"{'='*70}")
