import os
from paddleocr import PaddleOCR


# ============================================================
# LAND RECORD DOCUMENT OCR
# Member 1 - Document AI / OCR
# ============================================================

# ------------------------------------------------------------
# Folder paths
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")


# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ------------------------------------------------------------
# Initialize PaddleOCR
# ------------------------------------------------------------

print("Initializing OCR...")

ocr = PaddleOCR(
    lang="en"
)

print("OCR initialized successfully.")
print()


# ------------------------------------------------------------
# Function to extract text from PaddleOCR result
# ------------------------------------------------------------

def extract_text_from_result(result):
    """
    Extract only detected text from PaddleOCR result.

    PaddleOCR versions can return results in slightly
    different formats, so this function handles the
    common formats.
    """

    extracted_text = []

    for item in result:

        # ----------------------------------------------------
        # Case 1:
        # Result is a dictionary containing "res"
        # ----------------------------------------------------

        if isinstance(item, dict):

            # Example:
            # {
            #     "res": {
            #         "rec_texts": [...]
            #     }
            # }

            if "res" in item:

                inner_result = item["res"]

                if isinstance(inner_result, dict):

                    # New PaddleOCR format
                    if "rec_texts" in inner_result:

                        texts = inner_result["rec_texts"]

                        if texts:
                            for text in texts:

                                text = str(text).strip()

                                if text:
                                    extracted_text.append(text)

                    # Older/alternative format
                    elif "text" in inner_result:

                        texts = inner_result["text"]

                        if isinstance(texts, list):

                            for text in texts:

                                text = str(text).strip()

                                if text:
                                    extracted_text.append(text)

                        else:

                            text = str(texts).strip()

                            if text:
                                extracted_text.append(text)

            # ------------------------------------------------
            # Case 2:
            # Result itself contains rec_texts
            # ------------------------------------------------

            elif "rec_texts" in item:

                texts = item["rec_texts"]

                if texts:

                    for text in texts:

                        text = str(text).strip()

                        if text:
                            extracted_text.append(text)

        # ----------------------------------------------------
        # Case 3:
        # Object has a "res" attribute
        # ----------------------------------------------------

        else:

            try:

                if hasattr(item, "res"):

                    inner_result = item.res

                    if isinstance(inner_result, dict):

                        if "rec_texts" in inner_result:

                            texts = inner_result["rec_texts"]

                            if texts:

                                for text in texts:

                                    text = str(text).strip()

                                    if text:
                                        extracted_text.append(text)

            except Exception:
                pass


    return extracted_text


# ------------------------------------------------------------
# Process one image
# ------------------------------------------------------------

def process_image(image_path):

    filename = os.path.basename(image_path)

    print("=" * 60)
    print(f"Processing: {filename}")
    print("=" * 60)

    try:

        # Run OCR
        result = ocr.predict(image_path)

        # Extract only text
        extracted_text = extract_text_from_result(result)

        # ----------------------------------------------------
        # Output filename
        # ----------------------------------------------------

        filename_without_extension = os.path.splitext(filename)[0]

        output_file = os.path.join(
            OUTPUT_FOLDER,
            filename_without_extension + ".txt"
        )

        # ----------------------------------------------------
        # Save extracted text
        # ----------------------------------------------------

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            if extracted_text:

                for text in extracted_text:

                    file.write(text)
                    file.write("\n")

            else:

                file.write(
                    "No text detected in this document.\n"
                )

        print("Saved successfully:")
        print(output_file)
        print()

    except Exception as error:

        print("ERROR while processing:")
        print(filename)

        print(error)
        print()


# ------------------------------------------------------------
# Main program
# ------------------------------------------------------------

def main():

    print()
    print("=" * 60)
    print("LAND RECORD DOCUMENT OCR")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Check input folder
    # --------------------------------------------------------

    if not os.path.exists(INPUT_FOLDER):

        print("ERROR:")
        print("Input folder does not exist:")
        print(INPUT_FOLDER)

        return


    # --------------------------------------------------------
    # Get image files
    # --------------------------------------------------------

    image_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
        ".webp"
    )

    image_files = []

    for filename in os.listdir(INPUT_FOLDER):

        if filename.lower().endswith(image_extensions):

            image_files.append(filename)


    # --------------------------------------------------------
    # Check if images exist
    # --------------------------------------------------------

    if not image_files:

        print("No images found inside:")
        print(INPUT_FOLDER)

        return


    # Sort files alphabetically
    image_files.sort()


    print(f"Found {len(image_files)} image(s).")
    print()


    # --------------------------------------------------------
    # Process every image
    # --------------------------------------------------------

    for filename in image_files:

        image_path = os.path.join(
            INPUT_FOLDER,
            filename
        )

        process_image(image_path)


    # --------------------------------------------------------
    # Completed
    # --------------------------------------------------------

    print("=" * 60)
    print("OCR PROCESSING COMPLETED")
    print("=" * 60)

    print()
    print("Check the OCR results inside:")
    print(OUTPUT_FOLDER)
    print()


# ------------------------------------------------------------
# Run program
# ------------------------------------------------------------

if __name__ == "__main__":
    main()