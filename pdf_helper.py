import fitz  # PyMuPDF
import os
import pytesseract
from PIL import Image
import io


def read_pdf_text(filepath):
    """Extracts text from a file and caches it to a .txt file.

    Supported input formats:
    - .txt (returns content directly)
    - .pdf (tries standard extraction first; falls back to OCR when needed)
    - images (.png, .jpg, .jpeg, .bmp, .tiff) (OCR only)

    Future requests will instantly read the .txt cache file instead of re-running OCR.
    """
    if not os.path.exists(filepath):
        print(f"ERROR: The file was not found at path: {filepath}")
        return None

    # Determine file type and cache location
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    text_extensions = {'.txt'}
    pdf_extensions = {'.pdf'}
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}

    if ext in text_extensions:
        cache_filepath = filepath
    else:
        cache_filepath = f"{filepath}.txt"

    # 1. Check if we already processed this file
    if os.path.exists(cache_filepath):
        print(f"SUCCESS: Found cached text for {filepath}. Loading instantly...")
        try:
            with open(cache_filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Failed to read cache: {e}. Re-extracting...")

    extracted_text = ""

    try:
        # Handle plain text files quickly
        if ext in text_extensions:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

        # Handle images (OCR only)
        if ext in image_extensions:
            print(f"Running OCR on image: {filepath}")
            img = Image.open(filepath)
            extracted_text = pytesseract.image_to_string(img)

        # Handle PDFs (text extraction + optional OCR fallback)
        elif ext in pdf_extensions:
            doc = fitz.open(filepath)

            # 2. Try standard text extraction first (Fastest)
            print(f"Scanning {filepath} for standard text...")
            for page in doc:
                extracted_text += page.get_text() + "\n"

            # 3. OCR Fallback (If the PDF is just scanned images)
            if not extracted_text.strip():
                print(f"WARNING: No standard text found. Starting OCR process for {filepath}...")
                print("This might take a few minutes depending on the size of the textbook.")

                extracted_text = ""
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)

                    # Convert the PDF page into an image
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_bytes))

                    # Use Tesseract to read the text
                    page_text = pytesseract.image_to_string(img)
                    extracted_text += page_text + "\n"

                    if page_num % 10 == 0 and page_num > 0:
                        print(f"OCR Progress: Processed {page_num} pages...")

            doc.close()

        # Unknown file type -> try to read as text for best-effort
        else:
            print(f"Unknown file type ({ext}). Attempting to read as text...")
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                extracted_text = f.read()

        # 4. Save (Cache) the result for next time!
        if extracted_text.strip():
            with open(cache_filepath, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"SUCCESS: Text extracted and cached to {cache_filepath}")

        return extracted_text

    except Exception as e:
        print(f"Extraction Error on {filepath}: {e}")
        return None