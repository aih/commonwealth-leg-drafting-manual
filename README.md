# Commonwealth Legislative Drafting Manual Web Conversion

This repository holds the project for downloading and converting the PDF chapters of the [Commonwealth Legislative Drafting Manual](https://www.thecommonwealth-ilibrary.org/index.php/comsec/catalog/book/873) into a web-native application.

The digital document generated in this repository was converted using Large Language Models (Gemini 3.1 Pro). It corresponds to the source text originally released under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/) (CC BY-NC-ND 4.0).

### Working UI Demo
![Application Walkthrough](DraftingManualUI/public/assets/working_ui_demo.webp)

## GitHub Pages Deployment
The converted web-native application is deployed to GitHub Pages at:
[https://aih.github.io/commonwealth-leg-drafting-manual/](https://aih.github.io/commonwealth-leg-drafting-manual/)

### Deployment Architecture
The documentation UI is built as a static Single-Page Application (SPA) using Vite. Since GitHub Pages natively expects individual HTML files for every route, we implement a simple SPA router hack using a `404.html` redirect script. 

When a direct deep link is accessed (like `/commonwealth-drafting-manual` followed by a chapter name), GitHub Pages initially flags it as a 404. The `404.html` script catches this, translates the URL path into a search query string, and redirects to the base `index.html`. Finally, a small `<script>` block in the index `<head>` parses the query string, strips the `commonwealth-drafting-manual` prefix, and uses `window.history.replaceState` to seamlessly restore the original clean URL view before the application router begins to load the actual chapter content. The default root URL will redirect to the `about.html` chapter.

## Self-Serve Conversion Engine Tooling

The robust PDF-to-XHTML conversion pipeline, as well as the generalized generic frontend UI for displaying such converted documents, have been decoupled and moved to the dedicated `pdf-convert-llm` repository under the Ad Hoc team. 

Any updates, fixes, or enhancements to the conversion engine, chunking logic, models used, or the generic website UI structure should be directed to that root project instead:
👉 [pdf-convert-llm general repository](https://github.com/aih/pdf-convert-llm)

## Project Structure

* `chapter_pdfs/`: Contains the original scraped PDF chapters.
* `convert_local_genai.py`: Natively uses the `google-genai` SDK to bypass server timeouts and convert the chapters into XML.
* `xml_content/`: Output directory containing the converted XHTML files.
* `DraftingManualUI/`: The deployed static React frontend containing the generated config and UI assets.
