from detect_aadhaar import detect_features
from extract_text import extract_text
import cv2
import re
import json

# Aadhaar validation logic
def validate_text(text):
    result = {
        "aadhaar_number": None,
        "dob": None,
        "name": None,
        "valid": False,
        "message": ""
    }

    if not text:
        result["message"] = "No text extracted"
        return result

    # Aadhaar Number: 12 digits, usually written in 4-4-4 format
    uid_match = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
    if uid_match:
        result["aadhaar_number"] = uid_match.group()
    else:
        result["message"] = "Aadhaar number not found"
        return result

    # DOB: Can be in DD/MM/YYYY or YYYY format
    dob_match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text) or re.search(r"\b\d{4}\b", text)
    if dob_match:
        result["dob"] = dob_match.group()
    else:
        result["message"] = "Date of Birth not found"
        return result

    # Name (guessing it's the first line that is not UID/DOB)
    lines = text.strip().split('\n')
    for line in lines:
        if result["aadhaar_number"] not in line and result["dob"] not in line:
            result["name"] = line.strip()
            break

    if not result["name"]:
        result["message"] = "Name not found"
        return result

    result["valid"] = True
    result["message"] = "Aadhaar details valid"
    return result

# Main Pipeline
if __name__ == "__main__":
    img_path = "data/sample_aadhaar.jpg"

    print("\n🔍 Step 1: Detecting Aadhaar visual features...")
    output_img, _, _, _ = detect_features(img_path)
    cv2.imshow("Detected Aadhaar Features", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("\n📄 Step 2: Extracting text...")
    extracted_text = extract_text(img_path)
    print("Extracted Text:\n", extracted_text)

    print("\n✅ Step 3: Validating Aadhaar...")
    validation_result = validate_text(extracted_text)

    print("\n🔎 Final Result:")
    print(json.dumps(validation_result, indent=4))
