import time
from pathlib import Path
from datetime import datetime

# application
from .window import Window
from .procom_io import ProcomIO
from .procom_image_converter import ProcomImageConverter
from .service import ProductServiceAPI

from .helpers import formalize
from .constants import *


assets = Path(__file__).parent.parent.parent / 'assets'
output = Path(__file__).parent.parent.parent / 'assets'
search = assets / 'search.png'
now = datetime.now()


class DeliveryStatus(Window):
    """Delivery Status Window

    perform actions:
        - like open window
        - set start date
        - set end date
        - set reference
        - press the search button
    """

    _name = "Delivery status"

    @property
    def name(self):
        return self._name

    def search(self, product):
        today = '{:%d%m%Y}'.format(now)
        self.write(DATE_DEBUT_POSITION,  DATE_DEBUT)
        self.write(DATE_FIN_POSITION,  today)
        self.write(REFERENCE_POSITION, product[0])
        try:
            self.click_asset(str(search))
        except:
            pass

    def save_output(self, product):
        ProcomIO.save(self, product[0], "qte", QTE_REGION, path=str(output))
        ProcomIO.save(self, product[0], "mtn", MTN_REGION, path=str(output))

    def convert_data(self, product):
        ref = formalize(product[0])
        path_qte = output / f'{ref}.qte.png'
        path_mtn = output / f'{ref}.mtn.png'
        qte, _ = ProcomImageConverter.convert(path=str(path_qte))
        mtn, _ = ProcomImageConverter.convert(path=str(path_mtn))
        return ref, qte, mtn

    def save_to_service(self, product):

        ref, qte, mtn = self.convert_data(product)
        path_qte = output / f'{ref}.qte.png'
        prod = {
            "qte_stock": float(qte),
            "value": float(mtn),
            "reference": ref,
            "designation": product[1],
        }
        ProductServiceAPI.save("products", prod, filenames={
            'picture': str(path_qte)
        })

    def perform_actions(self,  wait_time=20) -> None:
        """Perform Actions:

        Search with: Enter start date, end date with product ref, and press on search
        with sleep to wait for results (software performance 20s default)
        """

        with self as window:
            # wait 3sec to open
            time.sleep(3)
            for product in PRODUCTS:
                self.double_check()

                # if this window is not running go out
                if not window.is_running:
                    continue
                window.search(product)
                # wait untill get data
                time.sleep(wait_time)
                window.save_output(product)
                window.save_to_service(product)


# def checker(window: Window):
#     """Run this in seprate thread"""
#     window.checking()
#     window.double_check()


# def service(window: Window):
#     for n in ["products..."]:
#         with open(window) as win:
#             win.perform_actions(...)
