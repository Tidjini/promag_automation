import pyautogui

from ..helpers import formalize


def save_data(ref, label, region):
    img = pyautogui.screenshot(region=region)
    ref = formalize(ref)
    img.save("output/{}.{}.png".format(ref, label))


def save_qte():
    pass


def save_vaule():
    pass


def save_all():
    pass
