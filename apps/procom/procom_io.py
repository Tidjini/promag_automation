from pathlib import Path
# third-party
import pyautogui

# application
from .window import Window
from .helpers import formalize


output = Path(__file__).parent.parent.parent / 'assets'


class ProcomIO:
    """PROCOM IO

    handle  output / input
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
            #print("{}\{}.{}.png".format(path, ref, field))
            filename = "{}\{}.{}.png".format(output, ref, field)
            img.save(filename)
        except Exception as ex:
            print("Procomi IO exception, due to", ex)

    @staticmethod
    def save_simple(
        window: Window,
        name: str,
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
            img.save("{}\\{}.png".format(output, name))
        except Exception as ex:
            print("Procomi IO exception, due to", ex)
