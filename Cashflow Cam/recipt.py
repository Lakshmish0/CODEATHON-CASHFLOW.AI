import cv2
import pytesseract
import re

# Set up Tesseract command (adjust the path if necessary)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Read the uploaded image
image_path = "/home/greatness-within/PycharmProjects/LoanAproval/res.jpg"
image = cv2.imread(image_path)

# Preprocess the image (convert to grayscale and apply thresholding)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Perform OCR on the image
ocr_result = pytesseract.image_to_string(thresh)

# Extract the amount using regex
amount_pattern = r'\b(?:AMOUNT|TOTAL)\s*[:\-]?\s*(\d+\.\d{2})'
match = re.search(amount_pattern, ocr_result, re.IGNORECASE)

if match:
    print("Extracted Amount:", match.group(1))
else:
    print("Amount not found in the receipt.")
