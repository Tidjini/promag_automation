import pyautogui

# application
from .window import Window
from .helpers import formalize


class ProcomIO:
    """PROCOM IO

    handle  output / input images
    """

    @staticmethod
    def save(
        window: Window,
        reference: str,
        field: str,
        region: tuple,
        path: str = "../output",
    ):
        """Save

        Frist get screenshot from region, then save it in output,
        and formalize reference to be like 1_0 instead of 1/0
        """
        if not window.is_running:
            # if window is not running do nothing
            print("Can't save, window is not running")
            return

        print("Perform Saving")
        try:
            img = pyautogui.screenshot(region=region)
            ref = formalize(reference)
            img.save("{}/{}.{}.png".format(path, ref, field))
        except Exception as ex:
            print("Procomi IO exception, due to", ex)