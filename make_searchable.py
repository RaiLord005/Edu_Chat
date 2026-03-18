import ocrmypdf
import os

def convert_to_searchable_pdf(input_filepath):
    """
    Takes a scanned PDF and overwrites it with a Searchable PDF 
    containing an embedded text layer.
    """
    # We will save it with a new name just to be safe
    output_filepath = input_filepath.replace('.pdf', '_searchable.pdf')
    
    print(f"Starting OCR on {input_filepath}...")
    print("This may take a while depending on the book length...")

    try:
        # deskew=True straightens crooked scans
        # force_ocr=True ensures it scans everything
        ocrmypdf.ocr(input_filepath, output_filepath, deskew=True, force_ocr=True)
        print(f"SUCCESS! Searchable PDF saved as: {output_filepath}")
        
    except Exception as e:
        print(f"Failed to convert PDF: {e}")

# Try it on your butterfly book!
convert_to_searchable_pdf("books/butterfly-5.pdf")