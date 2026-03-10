#!/usr/bin/env python3
"""
Clean up tribute pages - remove header/footer, keep just content
"""

from pathlib import Path
from bs4 import BeautifulSoup

def create_clean_tribute(input_file, output_file, title):
    """Extract main content and create clean page"""
    
    # Read original file
    with open(input_file, 'r', encoding='iso-8859-1') as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Try to find the main content - first try the tribute div (for berges.html)
    tribute_div = soup.find('div', {'id': 'tribute'})
    
    if tribute_div:
        tribute_content = str(tribute_div)
    else:
        # Try table format (for dale.ester.html)
        main_table = soup.find('table', {'bgcolor': '#FFFFFF', 'bordercolor': '#CCCCCC'})
        if main_table:
            tribute_content = str(main_table)
        else:
            print(f"Could not find main content in {input_file}")
            return False
    
    # Create clean HTML
    clean_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 14px;
  color: #000066;
  background: #fff;
  max-width: 900px;
  margin: 2em auto;
  padding: 1em 2em;
  line-height: 1.6;
}}
h1 {{
  font-size: 30px;
  color: #980000;
  font-weight: bold;
  text-align: center;
}}
h2 {{
  font-size: 24px;
  color: #000066;
  text-align: center;
}}
a {{
  color: #0000cc;
  text-decoration: none;
}}
a:hover {{
  text-decoration: underline;
}}
.archived-note {{
  font-size: 12px;
  color: #666;
  background: #f9f9f9;
  border: 1px solid #ccc;
  padding: 0.6em 1em;
  margin-bottom: 1.5em;
  border-radius: 4px;
}}
.footer {{
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid #ccc;
  font-size: 12px;
  color: #666;
}}
table {{
  width: 100%;
  border-collapse: collapse;
}}
</style>
</head>
<body>

<div class="archived-note">
<strong>Archived from:</strong> <a href="http://nephron.com/nephsites/lundin/{Path(input_file).name}" target="_blank">http://nephron.com/nephsites/lundin/{Path(input_file).name}</a> — 
Archived March 2026
</div>

{tribute_content}

<div class="footer">
<p><a href="index.html">← Back to Lundin's Corner</a></p>
<p>Original content © Nephron Information Center</p>
</div>

</body>
</html>'''
    
    # Write clean version
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(clean_html)
    
    print(f"✓ Created clean version: {output_file}")
    return True

# Process both tribute pages
lundin_dir = Path('/Users/brianrosenthal/vibe_coding/archive/lundin')

files_to_clean = [
    ('dale.ester.html', "Dale Ester's Tribute to Peter Lundin"),
    ('berges.html', "Richard Berge's Tribute to Peter Lundin")
]

for filename, title in files_to_clean:
    input_path = lundin_dir / filename
    if input_path.exists():
        create_clean_tribute(input_path, input_path, title)
    else:
        print(f"✗ File not found: {input_path}")
