#!/usr/bin/env python3
"""
Download all Zope slideshow presentations from nephron.org/shows
"""

import requests
import re
import os
import time
from pathlib import Path

# List of all presentations (excluding aakp_0804 which is already done)
presentations = [
    "alports",
    "av_access",
    "BCM_RGR_102004",
    "BCM_RGR_52307",
    "BCM_RGR_erythropoiesis",
    "calcium_files",
    "DialysisNepal",
    "Get Connected",
    "Info Systems",
    "internet_patients",
    "InternetSecurity",
    "lessons_africa",
    "NKF_041307",
    "NKF_Update_2007",
    "PreventingKidneyFailure",
    "Shaldon Osaka Lecture",
    "Veins",
]

# Presentation metadata (titles)
titles = {
    "aakp_0804": "AAKP CKD (2004)",
    "alports": "BCM Clin Path Conference - Alport's Syndrome (2005)",
    "av_access": "AV Access",
    "BCM_RGR_102004": "Computer Magic (2004)",
    "BCM_RGR_52307": "CKD-MBD (2007)",
    "BCM_RGR_erythropoiesis": "Erythropoiesis and VHL",
    "calcium_files": "Visio Touchmed Example",
    "DialysisNepal": "Dialysis in Nepal",
    "Get Connected": "Get Connected",
    "Info Systems": "Information Systems",
    "internet_patients": "Internet for Patients",
    "InternetSecurity": "Internet Security",
    "lessons_africa": "Lessons from Africa",
    "NKF_041307": "NKF 2007",
    "NKF_Update_2007": "NKF Update 2007",
    "PreventingKidneyFailure": "Preventing Kidney Failure",
    "Shaldon Osaka Lecture": "Shaldon Osaka Lecture",
    "Veins": "Veins",
}

def detect_slide_count(presentation_name):
    """Detect the number of slides by checking the HTML source"""
    url = f"http://nephron.org/shows/{presentation_name}"
    try:
        response = requests.get(url, timeout=10)
        content = response.text
        
        # Look for: for (count=2;count<=N;count++)
        match = re.search(r'for\s*\(\s*count\s*=\s*2\s*;\s*count\s*<=\s*(\d+)', content)
        if match:
            return int(match.group(1))
        
        # Fallback: try sequential downloads
        print(f"  No count found in JavaScript, trying sequential detection...")
        for i in range(1, 500):  # Max 500 slides
            slide_url = f"http://nephron.org/shows/{presentation_name}/slide{i}.gif"
            resp = requests.head(slide_url, timeout=5)
            if resp.status_code == 404:
                return i - 1
            time.sleep(0.1)
        
        return 0
    except Exception as e:
        print(f"  Error detecting slide count: {e}")
        return 0

def download_presentation(name, slide_count):
    """Download all slides for a presentation"""
    base_dir = Path("/Users/brianrosenthal/vibe_coding/archive/presentations")
    pres_dir = base_dir / name / "slides"
    pres_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading {slide_count} slides...")
    
    # Detect image extension
    extensions = ['gif', 'jpg', 'JPG', 'png']
    detected_ext = 'gif'
    
    for ext in extensions:
        test_url = f"http://nephron.org/shows/{name}/slide1.{ext}"
        resp = requests.head(test_url, timeout=5)
        if resp.status_code == 200:
            detected_ext = ext
            break
    
    print(f"  Using extension: .{detected_ext}")
    
    success_count = 0
    for i in range(1, slide_count + 1):
        slide_url = f"http://nephron.org/shows/{name}/slide{i}.{detected_ext}"
        slide_path = pres_dir / f"slide{i}.{detected_ext}"
        
        try:
            resp = requests.get(slide_url, timeout=10)
            if resp.status_code == 200:
                with open(slide_path, 'wb') as f:
                    f.write(resp.content)
                success_count += 1
                if i % 10 == 0:
                    print(f"  Downloaded {i}/{slide_count}")
            else:
                print(f"  Failed slide {i}: {resp.status_code}")
        except Exception as e:
            print(f"  Error downloading slide {i}: {e}")
        
        time.sleep(0.2)  # Be nice to the server
    
    print(f"  Successfully downloaded {success_count}/{slide_count} slides")
    return success_count, detected_ext

def create_viewer_page(name, slide_count, extension):
    """Create HTML viewer page for a presentation"""
    base_dir = Path("/Users/brianrosenthal/vibe_coding/archive/presentations")
    title = titles.get(name, name)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{
  font-family: Arial, Helvetica, sans-serif;
  margin: 0;
  padding: 20px;
  background: #f5f5f5;
  text-align: center;
}}
.container {{
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-radius: 8px;
}}
h1 {{
  color: #000066;
  font-size: 24px;
  margin-bottom: 10px;
}}
.archived-note {{
  font-size: 12px;
  color: #666;
  background: #f9f9f9;
  border: 1px solid #ccc;
  padding: 0.5em 1em;
  margin-bottom: 1.5em;
  border-radius: 4px;
}}
.slide-viewer {{
  background: #000;
  padding: 10px;
  margin: 20px 0;
  border-radius: 4px;
}}
.slide-viewer img {{
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
  min-height: 400px;
  background: #f0f0f0;
}}
.controls {{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin: 20px 0;
  flex-wrap: wrap;
}}
.btn {{
  background: #000066;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.3s;
}}
.btn:hover {{
  background: #000099;
}}
.btn:disabled {{
  background: #ccc;
  cursor: not-allowed;
}}
.slide-counter {{
  font-size: 16px;
  color: #000066;
  font-weight: bold;
  min-width: 120px;
}}
.slide-select {{
  padding: 8px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  color: #000066;
}}
.keyboard-hint {{
  font-size: 12px;
  color: #666;
  margin-top: 10px;
}}
.back-link {{
  margin-top: 20px;
  font-size: 14px;
}}
.back-link a {{
  color: #0000cc;
  text-decoration: none;
}}
.back-link a:hover {{
  text-decoration: underline;
}}
</style>
</head>
<body>

<div class="container">
  <div class="archived-note">
    <strong>Archived from:</strong> <a href="http://nephron.org/shows/{name}" target="_blank">http://nephron.org/shows/{name}</a> — 
    Archived March 2026
  </div>

  <h1>{title}</h1>

  <div class="slide-viewer">
    <img id="slideImage" src="slides/slide1.{extension}" alt="Slide 1" onerror="this.onerror=null; this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22800%22 height=%22600%22%3E%3Crect width=%22800%22 height=%22600%22 fill=%22%23f0f0f0%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-family=%22Arial%22 font-size=%2224%22 fill=%22%23999%22%3ESlide not available%3C/text%3E%3C/svg%3E';">
  </div>

  <div class="controls">
    <button class="btn" id="firstBtn" onclick="goToSlide(1)">⏮ First</button>
    <button class="btn" id="prevBtn" onclick="previousSlide()">← Previous</button>
    
    <div class="slide-counter">
      <span id="currentSlide">1</span> / <span id="totalSlides">{slide_count}</span>
    </div>
    
    <button class="btn" id="nextBtn" onclick="nextSlide()">Next →</button>
    <button class="btn" id="lastBtn" onclick="goToSlide({slide_count})">Last ⏭</button>
  </div>

  <div style="margin: 20px 0;">
    <label for="slideSelect" style="color: #000066; font-size: 14px; margin-right: 10px;">Jump to slide:</label>
    <select id="slideSelect" class="slide-select" onchange="goToSlide(this.value)">
      <script>
        for (let i = 1; i <= {slide_count}; i++) {{
          document.write('<option value="' + i + '">Slide ' + i + '</option>');
        }}
      </script>
    </select>
  </div>

  <div class="keyboard-hint">
    💡 Tip: Use arrow keys (← →) or Page Up/Page Down to navigate
  </div>

  <div class="back-link">
    <a href="../index.html">← Back to Presentations</a> |
    <a href="../../index.html">← Back to Archive Home</a>
  </div>
</div>

<script>
let currentSlide = 1;
const totalSlides = {slide_count};
const extension = "{extension}";

function updateSlide() {{
  document.getElementById('slideImage').src = `slides/slide${{currentSlide}}.${{extension}}`;
  document.getElementById('slideImage').alt = `Slide ${{currentSlide}}`;
  document.getElementById('currentSlide').textContent = currentSlide;
  document.getElementById('slideSelect').value = currentSlide;
  
  document.getElementById('firstBtn').disabled = currentSlide === 1;
  document.getElementById('prevBtn').disabled = currentSlide === 1;
  document.getElementById('nextBtn').disabled = currentSlide === totalSlides;
  document.getElementById('lastBtn').disabled = currentSlide === totalSlides;
}}

function nextSlide() {{
  if (currentSlide < totalSlides) {{
    currentSlide++;
    updateSlide();
  }}
}}

function previousSlide() {{
  if (currentSlide > 1) {{
    currentSlide--;
    updateSlide();
  }}
}}

function goToSlide(slideNum) {{
  slideNum = parseInt(slideNum);
  if (slideNum >= 1 && slideNum <= totalSlides) {{
    currentSlide = slideNum;
    updateSlide();
  }}
}}

document.addEventListener('keydown', function(event) {{
  if (event.key === 'ArrowRight' || event.key === 'PageDown') {{
    nextSlide();
    event.preventDefault();
  }} else if (event.key === 'ArrowLeft' || event.key === 'PageUp') {{
    previousSlide();
    event.preventDefault();
  }} else if (event.key === 'Home') {{
    goToSlide(1);
    event.preventDefault();
  }} else if (event.key === 'End') {{
    goToSlide(totalSlides);
    event.preventDefault();
  }}
}});

updateSlide();
</script>

</body>
</html>'''
    
    index_path = base_dir / name / "index.html"
    with open(index_path, 'w') as f:
        f.write(html)
    
    print(f"  Created viewer page: {index_path}")

# Main execution
print("="*60)
print("Downloading Nephron.org Presentations")
print("="*60)

results = []

for pres_name in presentations:
    print(f"\n{pres_name}:")
    print(f"  Detecting slide count...")
    
    slide_count = detect_slide_count(pres_name)
    
    if slide_count == 0:
        print(f"  Could not detect slides, skipping...")
        continue
    
    print(f"  Found {slide_count} slides")
    
    success, ext = download_presentation(pres_name, slide_count)
    
    if success > 0:
        create_viewer_page(pres_name, slide_count, ext)
        results.append({
            'name': pres_name,
            'title': titles.get(pres_name, pres_name),
            'slides': slide_count,
            'extension': ext
        })

print("\n" + "="*60)
print(f"SUMMARY: Successfully archived {len(results)} presentations")
print("="*60)

for r in results:
    print(f"  {r['title']}: {r['slides']} slides")

# Save results for creating index
import json
with open('/Users/brianrosenthal/vibe_coding/archive/presentations/metadata.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nMetadata saved to presentations/metadata.json")
