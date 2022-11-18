import pyautogui

from ..helpers import formalize


def save_data(ref, label, region):
    img = pyautogui.screenshot(region=region)
    ref = formalize(ref)
    img.save("output/{}.{}.png".format(ref, label))
