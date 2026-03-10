#!/usr/bin/env python3
"""
Create photo gallery HTML page
"""

import json
from pathlib import Path

# Load metadata
metadata_path = Path("/Users/brianrosenthal/vibe_coding/archive/photos/metadata.json")
with open(metadata_path, 'r') as f:
    photos = json.load(f)

# Sort by folder name
photos.sort(key=lambda x: x['folder'].lower())

# Filter out entries without images
photos = [p for p in photos if p['has_image']]

print(f"Creating gallery with {len(photos)} photos")

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Radiology Images — Nephron.org Archive</title>
<style>
body {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 14px;
  color: #000066;
  background: #f5f5f5;
  margin: 0;
  padding: 2em;
  line-height: 1.6;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  padding: 2em;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-radius: 8px;
}
h1 {
  font-size: 28px;
  color: #000066;
  margin-bottom: 0.5em;
}
.archived-note {
  font-size: 12px;
  color: #666;
  background: #f9f9f9;
  border: 1px solid #ccc;
  padding: 0.5em 1em;
  margin-bottom: 1.5em;
  border-radius: 4px;
}
.intro {
  color: #666;
  font-size: 14px;
  margin-bottom: 2em;
}
.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  margin: 2em 0;
}
.photo-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
  transition: all 0.3s;
}
.photo-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}
.photo-thumbnail {
  width: 100%;
  height: 200px;
  object-fit: contain;
  background: #000;
  border-radius: 4px;
  margin-bottom: 12px;
  display: block;
  cursor: pointer;
}
.photo-title {
  font-size: 14px;
  font-weight: bold;
  color: #000066;
  margin-bottom: 8px;
  text-transform: capitalize;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}
.photo-description {
  font-size: 13px;
  color: #666;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
.back-link {
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid #ccc;
  font-size: 14px;
}
.back-link a {
  color: #0000cc;
  text-decoration: none;
}
.back-link a:hover {
  text-decoration: underline;
}
/* Lightbox */
.lightbox {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.9);
}
.lightbox-content {
  position: relative;
  margin: auto;
  padding: 20px;
  width: 90%;
  max-width: 1000px;
  height: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.lightbox-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}
.lightbox-caption {
  color: white;
  text-align: center;
  padding: 15px;
  font-size: 16px;
  margin-top: 10px;
}
.lightbox-caption * {
  color: white !important;
}
.lightbox-close {
  position: absolute;
  top: 15px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  cursor: pointer;
}
.lightbox-close:hover {
  color: #bbb;
}
</style>
</head>
<body>

<div class="container">
  <div class="archived-note">
    <strong>Archived from:</strong> <a href="http://www.nephron.com/photos" target="_blank">http://www.nephron.com/photos</a> — 
    Archived March 2026
  </div>

  <h1>Radiology Images</h1>
  
  <div class="intro">
    Collection of kidney and urological radiology images with clinical descriptions.
  </div>

  <div class="photo-grid">
'''

for photo in photos:
    folder = photo['folder']
    image = photo['image']
    description = photo.get('description') or 'No description available'
    
    # Clean up folder name for display
    display_name = folder.replace('_', ' ').replace('%20', ' ')
    
    # Escape for HTML attributes
    description_attr = description.replace('"', '&quot;').replace("'", '&#39;')
    display_name_attr = display_name.replace('"', '&quot;').replace("'", '&#39;')
    
    html += f'''    <div class="photo-card">
      <img src="{folder}/{image}" alt="{display_name}" class="photo-thumbnail" data-title="{display_name_attr}" data-description="{description_attr}" onclick="openLightbox(this)">
      <div class="photo-title">{display_name}</div>
      <div class="photo-description">{description}</div>
    </div>
'''

html += '''  </div>

  <div class="back-link">
    <p><a href="../index.html">← Back to Archive Home</a></p>
  </div>
</div>

<div id="lightbox" class="lightbox" onclick="closeLightbox()">
  <div class="lightbox-content" onclick="event.stopPropagation()">
    <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
    <img id="lightbox-img" class="lightbox-image" src="">
    <div id="lightbox-caption" class="lightbox-caption"></div>
  </div>
</div>

<script>
function openLightbox(img) {
  const title = img.getAttribute('data-title');
  const description = img.getAttribute('data-description');
  
  document.getElementById('lightbox').style.display = 'block';
  document.getElementById('lightbox-img').src = img.src;
  document.getElementById('lightbox-caption').innerHTML = '<strong>' + title + '</strong><br>' + description;
}

function closeLightbox() {
  document.getElementById('lightbox').style.display = 'none';
}

document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    closeLightbox();
  }
});
</script>

</body>
</html>'''

# Write the gallery page
gallery_path = Path("/Users/brianrosenthal/vibe_coding/archive/photos/index.html")
with open(gallery_path, 'w') as f:
    f.write(html)

print(f"✓ Created photo gallery: {gallery_path}")
print(f"✓ {len(photos)} photos included")
