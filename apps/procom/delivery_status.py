import time
from _typeshed import Self

from .window import Window


class DeliveryStatus(Window):
    """Delivery Status Window

    perform actions:
        - like open window
        - set start date
        - set end date
        - set reference
        - press the search button
    """

    def perform_actions(self, start_date, end_date, reference, wait_time=20) -> None:
        """Perform Actions:

        Search with: Enter start date, end date with product ref, and press on search
        with sleep to wait for results (software performance 20s default)
        """

        # if this window is not running go out
        if not self.is_running:
            return

        self.write(start_date)
        self.write(end_date)
        self.write(reference)

        try:
            x, y = self.click_asset(self.search)
        except TypeError:
            # todo think about make self.is_running = False in here
            return

        # wait untill get data
        time.sleep(wait_time)


# def checker(window: Window):
#     """Run this in seprate thread"""
#     window.checking()
#     window.double_check()


# def service(window: Window):
#     for n in ["products..."]:
#         with open(window) as win:
#             win.perform_actions(...)
