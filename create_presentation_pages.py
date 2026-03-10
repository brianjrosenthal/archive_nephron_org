#!/usr/bin/env python3
"""
Generate both grid and list view pages for presentations
"""

import json

# Load metadata
with open('/Users/brianrosenthal/vibe_coding/archive/presentations/metadata.json', 'r') as f:
    presentations = json.load(f)

# Add aakp_0804 which was done first
all_presentations = [{
    "name": "aakp_0804",
    "title": "AAKP CKD (2004)",
    "slides": 110,
    "extension": "gif",
    "description": "American Association of Kidney Patients presentation on Chronic Kidney Disease"
}] + [
    {**p, "description": {
        "alports": "Baylor College of Medicine Clinical Pathology Conference",
        "av_access": "Arteriovenous access for hemodialysis",
        "BCM_RGR_102004": "BCM Renal Grand Rounds - Medical informatics",
        "BCM_RGR_52307": "Chronic Kidney Disease - Mineral and Bone Disorder",
        "BCM_RGR_erythropoiesis": "BCM Renal Grand Rounds - Red blood cell production",
        "calcium_files": "Calcium metabolism demonstration",
        "DialysisNepal": "International nephrology and dialysis care",
        "Get Connected": "Internet connectivity and resources for healthcare",
        "Info Systems": "Medical information systems and technology",
        "internet_patients": "Online resources and tools for patients",
        "InternetSecurity": "Healthcare information security and privacy",
        "lessons_africa": "Global health and nephrology perspectives",
        "NKF_041307": "National Kidney Foundation presentation",
        "NKF_Update_2007": "National Kidney Foundation updates and guidelines",
        "PreventingKidneyFailure": "Prevention strategies and early intervention",
        "Shaldon Osaka Lecture": "Historical perspective on dialysis development",
        "Veins": "Venous anatomy and dialysis access",
    }[p['name']]} for p in presentations
]

total_slides = sum(p['slides'] for p in all_presentations)

# Generate Grid View (index.html)
grid_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Presentations — Nephron.org</title>
<style>
body {{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  color: #000066;
  background: #f5f5f5;
  margin: 0;
  padding: 2em;
  line-height: 1.6;
}}
.container {{
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  padding: 2em;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-radius: 8px;
}}
h1 {{
  font-size: 28px;
  color: #000066;
  margin-bottom: 0.5em;
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
.intro {{
  color: #666;
  font-size: 14px;
  margin-bottom: 2em;
}}
.presentation-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin: 2em 0;
}}
.presentation-card {{
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
  transition: all 0.3s;
  text-decoration: none;
  color: #000066;
  display: block;
  overflow: hidden;
}}
.presentation-card:hover {{
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transform: translateY(-2px);
  text-decoration: none;
}}
.presentation-thumbnail {{
  width: 100%;
  height: 150px;
  object-fit: contain;
  background: #f0f0f0;
  border-radius: 4px;
  margin-bottom: 10px;
  display: block;
}}
.presentation-title {{
  font-size: 16px;
  font-weight: bold;
  color: #000066;
  margin-bottom: 8px;
}}
.presentation-meta {{
  font-size: 13px;
  color: #666;
}}
.slide-count {{
  display: inline-block;
  background: #e8f0ff;
  color: #000066;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-top: 8px;
}}
.stats {{
  background: #f0f0f0;
  padding: 1em;
  border-radius: 4px;
  margin: 2em 0;
  text-align: center;
}}
.stats strong {{
  color: #000066;
  font-size: 24px;
}}
.back-link {{
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid #ccc;
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
    <strong>Archived from:</strong> <a href="http://www.nephron.com/shows" target="_blank">http://www.nephron.com/shows</a> — 
    Archived March 2026
  </div>
  <h1>Presentations</h1>
  <div class="intro">
    Collection of educational presentations on nephrology, dialysis, kidney disease, and related medical informatics topics.
  </div>
  <div style="text-align: center; margin: 2em 0;">
    <a href="list.html" style="color: #0000cc; text-decoration: none; font-size: 14px;">Switch to Compact List View →</a>
  </div>
  <div class="presentation-grid">
'''

for p in all_presentations:
    grid_html += f'''    <a href="{p['name']}/index.html" class="presentation-card">
      <img src="{p['name']}/slides/slide1.{p['extension']}" alt="{p['title']} preview" class="presentation-thumbnail">
      <div class="presentation-title">{p['title']}</div>
      <div class="presentation-meta">{p['description']}</div>
      <span class="slide-count">{p['slides']} slides</span>
    </a>
'''

grid_html += '''  </div>
  <div class="back-link">
    <p><a href="../index.html">← Back to Archive Home</a></p>
  </div>
</div>
</body>
</html>'''

# Generate List View (list.html)
list_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Presentations Archive (List View) — Nephron.org</title>
<style>
body {{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 14px;
  color: #000066;
  background: #f5f5f5;
  margin: 0;
  padding: 2em;
  line-height: 1.5;
}}
.container {{
  max-width: 900px;
  margin: 0 auto;
  background: white;
  padding: 2em;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-radius: 8px;
}}
h1 {{
  font-size: 24px;
  color: #000066;
  margin-bottom: 0.5em;
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
.stats {{
  background: #f0f0f0;
  padding: 0.8em;
  border-radius: 4px;
  margin: 1.5em 0;
  text-align: center;
  font-size: 14px;
}}
.stats strong {{
  color: #000066;
  font-size: 18px;
}}
.presentation-list {{
  list-style: none;
  padding: 0;
  margin: 1.5em 0;
}}
.presentation-item {{
  padding: 0.8em 0;
  border-bottom: 1px solid #e0e0e0;
}}
.presentation-item:last-child {{
  border-bottom: none;
}}
.presentation-link {{
  text-decoration: none;
  color: #0000cc;
  font-weight: bold;
  font-size: 15px;
}}
.presentation-link:hover {{
  text-decoration: underline;
}}
.presentation-desc {{
  color: #666;
  font-size: 13px;
  margin: 0.3em 0;
}}
.presentation-count {{
  color: #888;
  font-size: 12px;
}}
.back-link {{
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid #ccc;
  font-size: 13px;
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
    <strong>Archived from:</strong> <a href="http://www.nephron.com/shows" target="_blank">http://www.nephron.com/shows</a> — 
    Archived March 2026
  </div>
  <h1>Presentations (Compact List)</h1>
  <div style="text-align: center; margin: 1.5em 0;">
    <a href="index.html" style="color: #0000cc; text-decoration: none; font-size: 13px;">Switch to Grid View with Thumbnails →</a>
  </div>
  <ul class="presentation-list">
'''

for p in all_presentations:
    list_html += f'''    <li class="presentation-item">
      <a href="{p['name']}/index.html" class="presentation-link">{p['title']}</a>
      <div class="presentation-desc">{p['description']}</div>
      <div class="presentation-count">{p['slides']} slides</div>
    </li>
'''

list_html += '''  </ul>
  <div class="back-link">
    <p><a href="../index.html">← Back to Archive Home</a></p>
  </div>
</div>
</body>
</html>'''

# Write files
with open('/Users/brianrosenthal/vibe_coding/archive/presentations/index.html', 'w') as f:
    f.write(grid_html)

with open('/Users/brianrosenthal/vibe_coding/archive/presentations/list.html', 'w') as f:
    f.write(list_html)

print("✓ Created presentations/index.html (grid view with thumbnails)")
print("✓ Created presentations/list.html (compact list view)")
print(f"✓ {len(all_presentations)} presentations | {total_slides:,} slides total")
