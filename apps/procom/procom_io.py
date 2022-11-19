import pyautogui

from ..helpers import formalize


class ProcomIO:
    """PROCOM IO

    handle  output / input images
    """

    @staticmethod
    def save(reference, field, region):
        """Save

        Frist get screenshot from region, then save it in output,
        and formalize reference to be like 1_0 instead of 1/0
        """

        img = pyautogui.screenshot(region=region)
        ref = formalize(reference)
        img.save("output/{}.{}.png".format(ref, field))


# def save_qte():
#     pass


# def save_vaule():
#     pass


# def save_all():
#     pass
