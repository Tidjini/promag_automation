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

        time.sleep(wait_time)

    def __enter__(self) -> Self:
        """use with keyword to perform actions in this object"""
        if self.is_running:
            return self
        try:
            # click status button in main window menu
            self.click_asset(self.status)
            time.sleep(1)
            # click in delivery status in displayed menu
            self.click_asset(self.delivery_status)
            time.sleep(2)
            # after that delivery status is opened
            self.is_running = True
        except TypeError as e:
            self.is_running = False

        return self

    def __exit__(self) -> None:
        """exit the with keyword with trying to close the window"""

        if not self.is_running:
            return

        self.is_running = False
        try:
            self.click_asset(self.close_asset)
            time.sleep(1)
        except TypeError as e:
            pass


# def checker(window: Window):
#     """Run this in seprate thread"""
#     window.checking()
#     window.double_check()


# def service(window: Window):
#     for n in ["products..."]:
#         with open(window) as win:
#             win.perform_actions(...)
