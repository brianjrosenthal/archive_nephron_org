#!/usr/bin/env python3
"""
Download all photos from nephron.com/photos with their descriptions
"""

import requests
from pathlib import Path
import time
import json
import urllib.parse

# Read the folder list
with open('/tmp/photo_folders.txt', 'r') as f:
    folders = [line.strip() for line in f if line.strip()]

print(f"Found {len(folders)} photo folders")

base_url = "http://www.nephron.com/photos"
auth = ('fadem', 'K1dney')
output_dir = Path("/Users/brianrosenthal/vibe_coding/archive/photos")
output_dir.mkdir(exist_ok=True)

results = []
failed = []

for i, folder in enumerate(folders, 1):
    print(f"\n[{i}/{len(folders)}] Processing: {folder}")
    
    # URL decode folder name for local storage
    folder_decoded = urllib.parse.unquote(folder)
    folder_dir = output_dir / folder_decoded
    folder_dir.mkdir(exist_ok=True)
    
    # Try to download the image (try common names and extensions)
    image_names = ['photo', 'image', 'picture']
    image_extensions = ['jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG']
    image_downloaded = None
    
    for name in image_names:
        for ext in image_extensions:
            image_url = f"{base_url}/{folder}/{name}.{ext}"
            try:
                resp = requests.get(image_url, auth=auth, timeout=10)
                if resp.status_code == 200:
                    image_path = folder_dir / f"{name}.{ext}"
                    with open(image_path, 'wb') as f:
                        f.write(resp.content)
                    image_downloaded = f"{name}.{ext}"
                    print(f"  ✓ Downloaded {name}.{ext}")
                    break
            except Exception as e:
                continue
        if image_downloaded:
            break
    
    # If no standard image name, try listing directory
    if not image_downloaded:
        # Try to get any image file
        try:
            # Get the folder listing
            folder_url = f"{base_url}/{folder}/manage_main"
            resp = requests.get(folder_url, auth=auth, timeout=10)
            if resp.status_code == 200:
                import re
                # Look for image files in the HTML
                images = re.findall(r'href="([^"]+\.(?:jpg|jpeg|gif|png|JPG|JPEG|GIF|PNG))"', resp.text, re.IGNORECASE)
                if images:
                    img_file = images[0]
                    img_url = f"{base_url}/{folder}/{img_file}"
                    img_resp = requests.get(img_url, auth=auth, timeout=10)
                    if img_resp.status_code == 200:
                        ext = img_file.split('.')[-1]
                        image_path = folder_dir / f"image.{ext}"
                        with open(image_path, 'wb') as f:
                            f.write(img_resp.content)
                        image_downloaded = f"image.{ext}"
                        print(f"  ✓ Downloaded {img_file} as image.{ext}")
        except Exception as e:
            print(f"  ✗ Could not find image: {e}")
    
    # Download the description (answer file)
    description = None
    answer_url = f"{base_url}/{folder}/answer"
    try:
        resp = requests.get(answer_url, auth=auth, timeout=10)
        if resp.status_code == 200:
            description = resp.text.strip()
            desc_path = folder_dir / "description.txt"
            with open(desc_path, 'w', encoding='utf-8') as f:
                f.write(description)
            print(f"  ✓ Downloaded description ({len(description)} chars)")
        else:
            print(f"  ✗ No description found")
    except Exception as e:
        print(f"  ✗ Error getting description: {e}")
    
    if image_downloaded or description:
        results.append({
            'folder': folder_decoded,
            'image': image_downloaded,
            'description': description,
            'has_image': image_downloaded is not None,
            'has_description': description is not None
        })
    else:
        failed.append(folder_decoded)
    
    time.sleep(0.3)  # Be nice to the server

print("\n" + "="*60)
print(f"SUMMARY")
print("="*60)
print(f"Total folders processed: {len(folders)}")
print(f"Successfully downloaded: {len(results)}")
print(f"Failed: {len(failed)}")

if failed:
    print(f"\nFailed folders:")
    for f in failed:
        print(f"  - {f}")

# Save metadata
metadata_path = output_dir / "metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nMetadata saved to {metadata_path}")
