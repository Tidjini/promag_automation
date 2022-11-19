# third-party
import cv2
import pytesseract

# application
from .helpers import has_number_or_dot

# static configuration
try:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
except:
    pass


class ProcomImageConverter:
    @staticmethod
    def get_image(picture_path):
        """Try to get image from picture path with zoom

        defaut zoom, is matched with my tests
        """
        try:
            return cv2.imread(picture_path)
        except Exception as e:
            print("Get Image Exception due, to:", e)

        return None

    @staticmethod
    def apply_zoom(image, zoom=4):
        h, w = image.shape[:2]
        image = cv2.resize(image, (w * zoom, h * zoom))
        return image

    @staticmethod
    def threshold(image):
        """This steps are copied from StackoverFlow

        todo put the link here
        """
        # Grayscale, Gaussian blur, Otsu's threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return thresh

    @staticmethod
    def remove_noise(image):
        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
        return 255 - opening

    @staticmethod
    def get_data(image):
        """Apply image to string

        psm = 7
        need just numbers, both integers [0..9] and decimals, can include dot and comma
        """
        try:
            data = pytesseract.image_to_string(
                image, config="--psm 7 -c tessedit_char_whitelist=0123456789.,"
            )

            # return more clean data, avoid spaces and comma to dot
            return data.strip().replace(",", ".").replace(" ", "").replace("_", "")
        except Exception as ex:
            print("pytesseract exception due to:", ex)

        return None

    @staticmethod
    def convert(path, zoom=4, zoom_max=10):
        image = ProcomImageConverter.get_image(path)
        if image is None:
            return None
        data = None
        while not has_number_or_dot(data):
            image = ProcomImageConverter.apply_zoom(image, zoom)
            thresh = ProcomImageConverter.threshold(image)
            invert = ProcomImageConverter.remove_noise(thresh)
            data = ProcomImageConverter.get_data(invert)

            # try get data untill to zoom max or return data
            if zoom == zoom_max:
                data = "0"
            # increment zoom on step
            zoom += 1

        return data, zoom


# ORIGINAL
# def convert(picture_path, zoom=4):
#     data = None
#     while not data or not has_number_or_dot(data):
#         # Grayscale, Gaussian blur, Otsu's threshold
#         image = cv2.imread(picture_path)
#         h, w = image.shape[:2]
#         image = cv2.resize(image, (w * zoom, h * zoom))

#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (3, 3), 0)
#         thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#         # Morph open to remove noise and invert image
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#         opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
#         invert = 255 - opening

#         # Perform text extraction
#         # data = pytesseract.image_to_string(
#         #     invert, lang='eng', config='--psm 6 or 7') no 5 / 8 / 9 / 11 / 12 /13
#         data = pytesseract.image_to_string(
#             invert, config="--psm 7 -c tessedit_char_whitelist=0123456789.,"
#         )
#         # print('raw data', data)

#         data = data.strip().replace(",", ".").replace(" ", "").replace("_", "")
#         print(data, "zoom: ", zoom)
#         # cv2.imshow('invert', invert)
#         # cv2.waitKey()
#         if zoom == 10:
#             data = "0"
#         zoom += 1
#     return data
