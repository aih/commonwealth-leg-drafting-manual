import os
import json
import re
from bs4 import BeautifulSoup

public_dir = "DraftingManualUI/public"
xml_dir = "xml_content"
pdf_dir = "chapter_pdfs"
chapters_json_path = os.path.join(public_dir, "chapters.json")

def slugify(text):
    text = text.lower()
    text = re.sub(r'chapter\s+(\d+)', r'ch\1', text)
    text = re.sub(r'appendix\s+([a-zA-Z0-9]+)', r'app-\1', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open(chapters_json_path, 'r') as f:
    chapters = json.load(f)

new_chapters = []

for chapter in chapters:
    old_filename = chapter['filename']
    if old_filename == "7305.xhtml":
        # Delete redundant 7305 files
        for d in [public_dir, xml_dir]:
            p = os.path.join(d, old_filename)
            if os.path.exists(p):
                os.remove(p)
        pdf_p = os.path.join(pdf_dir, "7305.pdf")
        if os.path.exists(pdf_p):
            os.remove(pdf_p)
        continue
        
    old_basename = old_filename.replace('.xhtml', '')
    public_file = os.path.join(public_dir, old_filename)
    
    title = chapter['title']
    
    # Try to extract a better title from the file
    if os.path.exists(public_file):
        with open(public_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            h1 = soup.find('h1')
            if h1:
                # Replace <br> with space
                for br in h1.find_all('br'):
                    br.replace_with(' ')
                extracted_title = h1.get_text(separator=' ', strip=True)
                if extracted_title:
                    title = extracted_title
                    
    title = re.sub(r'\s+', ' ', title)
    chapter['title'] = title
    
    slug = slugify(title)
    if not slug:
        slug = old_basename
    new_filename = f"{slug}.xhtml"
    
    # Handle duplicates
    counter = 1
    base_slug = slug
    while any(c.get('filename') == new_filename for c in new_chapters):
        slug = f"{base_slug}-{counter}"
        new_filename = f"{slug}.xhtml"
        counter += 1
        
    chapter['filename'] = new_filename
    new_chapters.append(chapter)
    
    # Rename files
    for d in [public_dir, xml_dir]:
        src = os.path.join(d, old_filename)
        dst = os.path.join(d, new_filename)
        if os.path.exists(src) and src != dst:
            os.rename(src, dst)
            
    # Rename PDFs
    pdf_src = os.path.join(pdf_dir, f"{old_basename}.pdf")
    pdf_dst = os.path.join(pdf_dir, f"{slug}.pdf")
    if os.path.exists(pdf_src) and pdf_src != pdf_dst:
        os.rename(pdf_src, pdf_dst)
        
with open(chapters_json_path, 'w') as f:
    json.dump(new_chapters, f, indent=2)
    
print("Renamed chapters successfully.")
