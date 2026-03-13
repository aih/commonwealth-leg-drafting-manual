import os
import re
import urllib.request
import time

html_file = 'ilibrary.html'
out_dir = 'chapter_pdfs'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all PDF download links directly
matches = re.findall(r'href="https://www.thecommonwealth-ilibrary.org/index.php/comsec/catalog/view/873/873/(\d+)"\s+class="cmp_download_link"', content)

print(f"Found {len(matches)} PDF links.")

for item_id in set(matches):
    url = f"https://www.thecommonwealth-ilibrary.org/index.php/comsec/catalog/download/873/873/{item_id}"
    filename = f"{item_id}.pdf"
    out_path = os.path.join(out_dir, filename)
    
    print(f"Downloading {url} to {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response, open(out_path, 'wb') as out_f:
            out_f.write(response.read())
        time.sleep(0.5)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

print("Done downloading.")
