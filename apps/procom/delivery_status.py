import time
from .window import Window


class DelivryStatus(Window):
    """Delivery Status Window

    perform actions:
        - like open window
        - set start date
        - set end date
        - set reference
        - press the search button
    """

    def perform_actions(self, start_date, end_date, reference, wait_time=20):
        """Perform Actions:

        Search with: Enter start date, end date with product ref, and press on search
        with sleep to wait for results (software performance 20s default)
        """
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

    def __enter__(self):
        if self.is_running:
            return self
        try:
            self.click_asset(self.status)
            time.sleep(1)
            self.click_asset(self.delivery_status)
            time.sleep(2)
            self.is_running = True
        except TypeError as e:
            self.is_running = False

        return self

    def __exit__(self) -> None:
        if not self.is_running:
            return
        self.is_running = False
        try:
            close_asset = self.close
            self.click_asset(close_asset)
            time.sleep(1)
        except TypeError as e:
            pass


def checker(window: Window):
    """Run this in seprate thread"""
    window.checking()
    window.double_check()


def service(window: Window):
    with open(window) as win:
        for n in ["products..."]:
            win.perform_actions(...)
