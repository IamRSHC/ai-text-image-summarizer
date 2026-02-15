import pytesseract
import cv2
import numpy as np

# set tesseract path
pytesseract.pytesseract.tesseract_cmd = r"D:\HAREECHARAN\Internships\MS ELEVATE AZURE\TESSERACT OCR\tesseract.exe"

def extract_text_from_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)
    return text
