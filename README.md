# Commonwealth Legislative Drafting Manual Web Conversion

This repository holds the project for downloading and converting the PDF chapters of the [Commonwealth Legislative Drafting Manual](https://www.thecommonwealth-ilibrary.org/index.php/comsec/catalog/book/873) into a web-native application.

The digital document generated in this repository was converted using Large Language Models (Gemini 3.1 Pro). It corresponds to the source text originally released under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/) (CC BY-NC-ND 4.0).

### Working UI Demo
![Application Walkthrough](DraftingManualUI/public/assets/working_ui_demo.webp)

## Self-Serve Conversion Engine Tooling

The robust PDF-to-XHTML conversion pipeline, as well as the generalized generic frontend UI for displaying such converted documents, have been decoupled and moved to the dedicated `pdf-convert-llm` repository under the Ad Hoc team. 

Any updates, fixes, or enhancements to the conversion engine, chunking logic, models used, or the generic website UI structure should be directed to that root project instead:
👉 [pdf-convert-llm general repository](https://github.com/aih/pdf-convert-llm)

## Project Structure

* `chapter_pdfs/`: Contains the original scraped PDF chapters.
* `convert_local_genai.py`: Natively uses the `google-genai` SDK to bypass server timeouts and convert the chapters into XML.
* `xml_content/`: Output directory containing the converted XHTML files.
* `DraftingManualUI/`: The deployed static React frontend containing the generated config and UI assets.
