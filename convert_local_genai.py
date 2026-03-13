import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("GOOGLE_API_KEY environment variable not set.")
    exit(1)

client = genai.Client(
    api_key=api_key,
    http_options={'timeout': 600000} # Provide a long timeout to avoid connection drops
)
prompt = """
You are an expert in legislative drafting documents. 
Convert the following PDF content into structured XHTML. 
Use standard HTML tags:
- <h1> for the main chapter title
- <h2>, <h3>, <h4> for section and subsection headings
- <p> for regular text paragraphs
- <ul> and <li> for bulleted lists
- <ol> and <li> for numbered lists
- <strong> or <em> for emphasis where apparent in the text

Do NOT include any XML declarations or markdown formatting backticks (```html, ```xml). 
Return ONLY the raw HTML elements that can be placed directly inside a <body> tag.
"""

pdf_dir = "chapter_pdfs"
out_dir = "xml_content"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])

def process_pdf(filename):
    pdf_path = os.path.join(pdf_dir, filename)
    out_filename = filename.replace('.pdf', '.xhtml')
    out_file_path = os.path.join(out_dir, out_filename)
    
    # Skip if already processed successfully (check if size is reasonable and doesn't contain quota error)
    if os.path.exists(out_file_path) and os.path.getsize(out_file_path) > 100:
        with open(out_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "Quota exceeded" not in content and "API error" not in content and "chunk_error" not in content:
            return f"Skipped {filename}, already properly converted."

    print(f"Processing {filename}...")
    for attempt in range(3):
        try:
            print(f"Uploading {filename} to Gemini (Attempt {attempt+1})...")
            gfile = client.files.upload(file=pdf_path)
            
            print(f"Generating content for {filename}...")
            response = client.models.generate_content(
                model='gemini-3.1-pro-preview',
                contents=[prompt, gfile]
            )
            
            # Save output
            with open(out_file_path, 'w', encoding='utf-8') as out_f:
                html_content = response.text
                if html_content.startswith("```html"):
                    html_content = html_content[7:]
                if html_content.endswith("```"):
                    html_content = html_content[:-3]
                out_f.write(html_content.strip())
            
            # Clean up the file on the server
            client.files.delete(name=gfile.name)
            return f"Saved {out_filename}"
            
        except Exception as e:
            print(f"Error processing {filename} on attempt {attempt+1}: {e}")
            time.sleep(5)  # Backoff before retrying
            
    return f"Failed to process {filename} after 3 attempts."

# Process sequentially
for filename in pdf_files:
    result = process_pdf(filename)
    print(result)
    # To stay safely under 2 Requests Per Minute (RPM) limits for free/preview models:
    if not result.startswith("Skipped"):
        print("Waiting 35 seconds to avoid rate limiting...")
        time.sleep(35)

print("Finished processing all PDFs.")
