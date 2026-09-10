from flask import Flask, render_template, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# =========================================================
# CONFIGURATION
# =========================================================

# Folder containing extracted JSON records
EXTRACTED_FOLDER = os.path.join("document_ai", "extracted")

# Folder where uploaded documents are temporarily stored
UPLOAD_FOLDER = os.path.join("uploads")

# Allowed document formats
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

os.makedirs(EXTRACTED_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# HELPER FUNCTION
# =========================================================

def allowed_file(filename):
    """
    Check whether the uploaded file has an allowed extension.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        results=[],
        search_text=""
    )


# =========================================================
# SEARCH LAND RECORDS
# =========================================================

@app.route("/search", methods=["POST"])
def search():

    search_text = request.form.get(
        "search_text",
        ""
    ).strip().lower()

    results = []

    if search_text and os.path.exists(EXTRACTED_FOLDER):

        for filename in os.listdir(EXTRACTED_FOLDER):

            if not filename.lower().endswith(".json"):
                continue

            filepath = os.path.join(
                EXTRACTED_FOLDER,
                filename
            )

            try:

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                # Convert JSON data to searchable text
                searchable_text = json.dumps(
                    data,
                    ensure_ascii=False
                ).lower()

                # Search
                if search_text in searchable_text:

                    results.append({
                        "filename": filename,
                        "data": data
                    })

            except Exception as e:

                print(
                    f"Error reading {filename}: {e}"
                )

    return render_template(
        "index.html",
        results=results,
        search_text=search_text
    )


# =========================================================
# VERIFY DOCUMENT PAGE
# =========================================================

@app.route("/verify")
def verify():

    return render_template(
        "verify.html",
        error=None
    )


# =========================================================
# DOCUMENT UPLOAD + VERIFICATION
# =========================================================

@app.route("/verify", methods=["POST"])
def verify_document():

    # Check whether a file was submitted
    if "document" not in request.files:

        return render_template(
            "verify.html",
            error="No document was selected."
        )

    file = request.files["document"]

    # Check filename
    if file.filename == "":

        return render_template(
            "verify.html",
            error="Please select a document."
        )

    # Check extension
    if not allowed_file(file.filename):

        return render_template(
            "verify.html",
            error=(
                "Unsupported file type. "
                "Please upload PDF, JPG, JPEG or PNG."
            )
        )

    # Secure filename
    filename = secure_filename(file.filename)

    # Save uploaded file
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # -----------------------------------------------------
    # TEMPORARY VERIFICATION RESULT
    # -----------------------------------------------------
    #
    # This is currently a demonstration result.
    #
    # Later we will replace this section with:
    #
    # Upload
    #     ↓
    # OCR
    #     ↓
    # Field extraction
    #     ↓
    # MySQL reference search
    #     ↓
    # Field comparison
    #     ↓
    # Verification result
    #
    # -----------------------------------------------------

    verification = {

        "status": "REVIEW REQUIRED",

        "status_type": "warning",

        "message": (
            "The document has been uploaded successfully. "
            "Detailed verification requires comparison "
            "with the trusted land-record database."
        ),

        "filename": filename,

        "fields": [

            {
                "name": "Owner Name",
                "reference": "Pending",
                "uploaded": "Pending",
                "status": "Pending"
            },

            {
                "name": "Survey Number",
                "reference": "Pending",
                "uploaded": "Pending",
                "status": "Pending"
            },

            {
                "name": "Patta Number",
                "reference": "Pending",
                "uploaded": "Pending",
                "status": "Pending"
            },

            {
                "name": "Village",
                "reference": "Pending",
                "uploaded": "Pending",
                "status": "Pending"
            },

            {
                "name": "Land Area",
                "reference": "Pending",
                "uploaded": "Pending",
                "status": "Pending"
            },

            {
                "name": "Registration Date",
                "reference": "Pending",
                "uploaded": "Pending",
                "status": "Pending"
            }

        ]

    }

    return render_template(
        "verification_result.html",
        verification=verification
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )