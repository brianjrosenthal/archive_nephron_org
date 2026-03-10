#!/usr/bin/env python3
"""
Archive the Self Cannulation page for Patient Education
"""

import re
import urllib.request
import os
from bs4 import BeautifulSoup

os.makedirs('/Users/brianrosenthal/vibe_coding/archive/patient_education/images', exist_ok=True)

url = 'http://www.nephron.org/nephsites/nic/self_cannulation.htm'
print(f"Downloading {url}...")

try:
    response = urllib.request.urlopen(url)
    html = response.read().decode('iso-8859-1')
    print("✓ Downloaded")
except Exception as e:
    print(f"✗ Failed to download: {e}")
    exit(1)

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
        
        # Clean up image src paths
        for img in elem.find_all('img'):
            src = img.get('src', '')
            if src and '/images/' in src:
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
<title>Cannulating your own AV Fistula</title>
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

<h1>Cannulating your own AV Fistula</h1>

{content_html}

<div class="footer">
  <p><a href="index.html">← Back to Patient Education</a></p>
  <p>Original content © Nephron Information Center | Archived March 2026</p>
</div>

</body>
</html>
"""

# Save the clean HTML
output_path = '/Users/brianrosenthal/vibe_coding/archive/patient_education/self_cannulation.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(clean_html)

print(f"✓ Created self_cannulation.html")
