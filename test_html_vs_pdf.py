import os
import re
import unittest
import pymupdf
from bs4 import BeautifulSoup

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = pymupdf.open(pdf_path)
        for page in doc:
            # Simple text extraction, might include some headers/footers
            text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def extract_text_from_html(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # If the file has the parsererror string, it failed badly on UI, but we check raw content
        soup = BeautifulSoup(content, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator=' ')
    except Exception as e:
        print(f"Error reading {html_path}: {e}")
        return ""

def clean_text(text):
    # Remove newlines, non-alphanumeric chars, normalize whitespace
    text = re.sub(r'[^a-zA-Z0-9]+', ' ', text)
    return text.lower().strip()

class TestHtmlVsPdf(unittest.TestCase):
    def test_chapter_text_matches(self):
        pdf_dir = "chapter_pdfs"
        html_dir = "DraftingManualUI/public" # The UI public directory has the latest chapters
        
        pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
        
        failed_chapters = []
        
        for pdffile in pdf_files:
            base_name = pdffile.replace('.pdf', '')
            html_file = f"{base_name}.xhtml"
            
            pdf_path = os.path.join(pdf_dir, pdffile)
            html_path = os.path.join(html_dir, html_file)
            
            if not os.path.exists(html_path):
                # Check xml_content just in case it hasn't been copied
                html_path = os.path.join("xml_content", html_file)
                if not os.path.exists(html_path):
                    print(f"Skipping {pdffile}, HTML not found.")
                    failed_chapters.append(pdffile)
                    continue

            pdf_text = extract_text_from_pdf(pdf_path)
            html_text = extract_text_from_html(html_path)
            
            pdf_clean = clean_text(pdf_text)
            html_clean = clean_text(html_text)
            
            # Since HTML won't have headers/footers/page numbers like PDF, 
            # the PDF text will likely be slightly longer.
            # But the HTML text should be a subset of the PDF text, or at least very close in length.
            # Let's check token overlap or length ratio
            
            pdf_words = pdf_clean.split()
            html_words = html_clean.split()
            
            if not pdf_words:
                continue
                
            ratio = len(html_words) / len(pdf_words)
            print(f"[{base_name}] Word Count Ratio (HTML/PDF): {ratio:.2f} ({len(html_words)}/{len(pdf_words)})", end=" ")
            
            if ratio < 0.75:
                # If HTML has less than 75% of the words of the PDF, it's likely truncated
                print("-> FAILED (Truncated?)")
                failed_chapters.append(pdffile)
            elif ratio > 1.25:
                print("-> FAILED (Too Long?)")
                failed_chapters.append(pdffile)
            else:
                print("-> PASSED")
                
        # We assert that no chapters failed validation
        self.assertEqual(len(failed_chapters), 0, f"The following chapters failed text matching: {failed_chapters}")

if __name__ == '__main__':
    unittest.main()
