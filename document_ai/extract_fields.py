import re
import json
import os


def extract_fields(text):
    data = {
        "registration_number": None,
        "document_date": None,
        "owner_name": None,
        "previous_owner": None,
        "survey_number": None,
        "subdivision_number": None,
        "patta_number": None,
        "district": None,
        "taluk_tehsil": None,
        "village": None,
        "area": None,
        "area_unit": None,
        "land_type": None,
        "registration_date": None,
        "encumbrance_status": None
    }

    # Registration Number
    match = re.search(
        r"Registration Number\s*[:\-]?\s*([A-Z0-9\/\-]+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["registration_number"] = match.group(1).strip()

    # Document Date
    match = re.search(
        r"Document Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})",
        text,
        re.IGNORECASE
    )
    if match:
        data["document_date"] = match.group(1)

    # Owner Name
    match = re.search(
        r"Owner Name\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["owner_name"] = match.group(1).strip()

    # Previous Owner
    match = re.search(
        r"Previous Owner\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["previous_owner"] = match.group(1).strip()

    # Survey Number
    match = re.search(
        r"Survey Number\s*[:\-]?\s*([A-Z0-9\/\-]+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["survey_number"] = match.group(1).strip()

    # Subdivision Number
    match = re.search(
        r"Subdivision Number\s*[:\-]?\s*([A-Z0-9\/\-]+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["subdivision_number"] = match.group(1).strip()

    # Patta Number
    match = re.search(
        r"Patta Number\s*[:\-]?\s*([A-Z0-9\/\-]+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["patta_number"] = match.group(1).strip()

    # District
    match = re.search(
        r"District\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["district"] = match.group(1).strip()

    # Taluk / Tehsil
    match = re.search(
        r"Taluk\s*\/\s*Tehsil\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["taluk_tehsil"] = match.group(1).strip()

    # Village
    match = re.search(
        r"Village\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["village"] = match.group(1).strip()

    # Area
    match = re.search(
        r"Area\s*[:\-]?\s*([\d.]+)\s*(acres?|hectares?|hectare|cents?)",
        text,
        re.IGNORECASE
    )
    if match:
        data["area"] = match.group(1)
        data["area_unit"] = match.group(2).lower()

    # Land Type
    match = re.search(
        r"Land Type\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["land_type"] = match.group(1).strip()

    # Registration Date
    match = re.search(
        r"Registration Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})",
        text,
        re.IGNORECASE
    )
    if match:
        data["registration_date"] = match.group(1)

    # Encumbrance Status
    match = re.search(
        r"Encumbrance Status\s*[:\-]?\s*(.+)",
        text,
        re.IGNORECASE
    )
    if match:
        data["encumbrance_status"] = match.group(1).strip()

    return data


def process_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    data = extract_fields(text)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Extracted fields saved to: {output_file}")


if __name__ == "__main__":

    input_folder = "output"
    extracted_folder = "extracted"

    os.makedirs(extracted_folder, exist_ok=True)

    for filename in os.listdir(input_folder):

        if filename.endswith(".txt"):

            input_file = os.path.join(
                input_folder,
                filename
            )

            output_filename = filename.replace(
                ".txt",
                ".json"
            )

            output_file = os.path.join(
                extracted_folder,
                output_filename
            )

            print("=" * 60)
            print(f"Processing: {filename}")

            process_file(
                input_file,
                output_file
            )

    print("=" * 60)
    print("FIELD EXTRACTION COMPLETED")