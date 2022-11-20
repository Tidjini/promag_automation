import time
import signal
import os
from threading import Thread
from pathlib import Path

#  application
from procom.window import Window, MainWindow
from procom.delivery_status import DeliveryStatus
from procom.procom_io import ProcomIO
from procom.procom_image_converter import ProcomImageConverter
from procom.constants import *

# folders
root = Path(__file__).parent.parent
assets = root / 'assets'
output = root / 'output'
headers = assets / 'headers'
menu = assets / 'menu'

# general assets
logo = assets / "procom_logo.png"
close = assets / 'close.png'
search = assets / 'search.png'

# delivery
delivery = headers / 'delivery_status.png'
delivery_active = headers / 'delivery_status_active.png'

# menu
menu_status = menu / 'status.png'
menu_delivery = menu / 'delivery_status.png'


def checking(*windows):

    while True:
        for window in windows:
            window.double_check()

        # if not main_window.is_running:
        #     print('Main window is not running, repeat process or close')
        #     time.sleep(2)
        #     continue

        # for window in windows:
        #     window.double_check()
        #     if not window.is_running:
        #         continue

        #     print('{} perform actions, and close it.'.format(window.name))


def actions(*windows):
    while True:
        for window in windows:
            window.perform_actions()

        # window.perform_actions() if window.is_running else print(
        #     f"{window.name} is not running, go next iteration"
        # )

        # ProcomIO.save(window, "1/0", "qte", (94, 760, 78, 15))
        # # try some stupid
        # result = ProcomImageConverter.convert(
        #     "../output/1_0.qte.png", zoom=1, zoom_max=2
        # )
        # if result is None:
        #     print("1/0[qte] -> NONE")
        #     continue
        # data, zoom = result
        # print("1/0[qte]-->data:{}, zoom:{}".format(data, zoom))

        # try:
        #     result = float(data)
        # except:
        #     result = 0.0

        # product = {
        #     "qte_stock": result,
        #     "value": 0.0,
        #     "reference": "1_0",
        #     "designation": "designation",
        # }
        # ProductServiceAPI.save("products", product, filenames=None)
        time.sleep(10)


if __name__ == "__main__":
    logo_location = x_logo, y_logo
    main_window = MainWindow(check_asset=str(
        logo), assume_location=logo_location)

    delivery_window = DeliveryStatus(check_asset=str(delivery), assume_location=delivery_location, check_active_asset=str(
        delivery_active), menu=str(menu_status), sub_menu=str(menu_delivery), close_asset=str(close))

    # checker = Thread(target=checking, args=(
    #     main_window, delivery_window), daemon=True)
    # checker.start()

    actions(main_window, delivery_window)


# - check main window:
