import os
import time
import requests

api_url = "http://localhost:8000"
pdf_dir = "chapter_pdfs"
out_dir = "xml_content"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

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

for filename in sorted(os.listdir(pdf_dir)):
    if not filename.endswith('.pdf'):
        continue
        
    pdf_path = os.path.join(pdf_dir, filename)
    print(f"Submitting {filename} to API...")
    
    with open(pdf_path, 'rb') as f:
        files = {'files': (filename, f, 'application/pdf')}
        data = {
            'prompt': prompt,
            'llm_provider': 'gemini',
            'model_name': 'gemini-3.1-pro-preview',
            'processing_mode': 'batch'
        }
        
        response = requests.post(f"{api_url}/convert", files=files, data=data)
        
        if response.status_code != 200:
            print(f"Error submitting {filename}: {response.text}")
            continue
            
        job_id = response.json().get('job_id')
        print(f"Job started. ID: {job_id}")
        
        # Poll for completion
        while True:
            status_response = requests.get(f"{api_url}/status/{job_id}")
            if status_response.status_code != 200:
                print(f"Error checking status for {job_id}")
                break
                
            status_data = status_response.json()
            status = status_data.get('status')
            
            if status in ['completed', 'completed_with_errors', 'failed']:
                print(f"Job {status}: {status_data.get('message')}")
                break
                
            print(f"Progress: {status_data.get('progress')}% - {status_data.get('message')}")
            time.sleep(5)
            
        # Download results if completed
        if status in ['completed', 'completed_with_errors']:
            download_response = requests.get(f"{api_url}/download/{job_id}")
            if download_response.status_code == 200:
                results = download_response.json().get('results', [])
                for result in results:
                    xml_filename = result.get('filename')
                    xml_content = result.get('xml_content')
                    
                    if xml_filename and xml_content:
                        # Change extension to .xhtml or .html
                        out_filename = xml_filename.replace('.xml', '.xhtml')
                        out_file_path = os.path.join(out_dir, out_filename)
                        
                        with open(out_file_path, 'w', encoding='utf-8') as out_f:
                            out_f.write(xml_content)
                        print(f"Saved {out_filename}")
            else:
                print(f"Failed to download results for {job_id}")
                
        # Clean up job
        requests.delete(f"{api_url}/jobs/{job_id}")
        print("-" * 40)

print("All processing finished.")
