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


# for _ref, designation in PRODUCTS:
#     ref = formalize(_ref)
#     qte = cv2.imread(f"output/{ref}.qte.png")
#     h, w = qte.shape[:2]
#     qte = cv2.resize(qte, (w * 3, h * 3))

#     mtn = cv2.imread(f"output/{ref}.mtn.png")
#     h, w = mtn.shape[:2]
#     mtn = cv2.resize(mtn, (w * 3, h * 3))

#     str_qte = pytesseract.image_to_string(qte)
#     str_mtn = pytesseract.image_to_string(mtn)
#     str_qte = str_qte.strip().replace(" ", "").replace(",", ".")
#     str_mtn = str_mtn.strip().replace(" ", "").replace(",", ".")

#     quantite = 0.0
#     montant = 0.0
#     try:
#         quantite = float(str_qte)
#     except Exception:
#         pass

#     try:
#         montant = float(str_mtn)
#     except Exception:
#         pass

#     product = {
#         "qte_stock": quantite,
#         "value": montant,
#         "reference": ref,
#         "designation": designation,
#     }

#     update(product)
