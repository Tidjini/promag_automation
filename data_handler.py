import cv2
from PIL import Image
import pytesseract


from helpers import formalize
import service
from constants import *


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_info(ref: str, field: str) -> float:
    """Extract data from images

    Using pytessaract image to string
    """
    result = 0.0
    try:
        data = cv2.imread(f"output/{ref}.{field}.png")
    except:
        return result
    # get width, and height
    h, w = data.shape[:2]
    data = cv2.resize(data, (w * 3, h * 3))
    str_data = pytesseract.image_to_string(data)
    # clean str data
    str_data = str_data.strip().replace(" ", "").replace(",", ".")

    try:
        result = float(str_data)
    except:
        result = 0.0

    return result


def push_data(ref: str, designation: str, qte: float, mtn: float) -> None:
    """Push data to remote server"""
    product = {
        "qte_stock": qte,
        "value": mtn,
        "reference": ref,
        "designation": designation,
    }

    service.update(product)


def is_number(word):

    for char in word:
        if not char.isdigit() and not char == ".":
            return False

    return True


def convert(picture_path, zoom=4):
    data = None
    while not data or not is_number(data):
        # Grayscale, Gaussian blur, Otsu's threshold
        image = cv2.imread(picture_path)
        h, w = image.shape[:2]
        image = cv2.resize(image, (w * zoom, h * zoom))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening

        # Perform text extraction
        # data = pytesseract.image_to_string(
        #     invert, lang='eng', config='--psm 6 or 7') no 5 / 8 / 9 / 11 / 12 /13
        data = pytesseract.image_to_string(
            invert, config="--psm 7 -c tessedit_char_whitelist=0123456789.,"
        )
        # print('raw data', data)

        data = data.strip().replace(",", ".").replace(" ", "").replace("_", "")
        print(data, "zoom: ", zoom)
        # cv2.imshow('invert', invert)
        # cv2.waitKey()
        if zoom == 10:
            data = "0"
        zoom += 1
    return data
