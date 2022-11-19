import time
from random import randrange
from threading import Thread
from pathlib import Path

#  application
from procom.window import Window, MainWindow
from procom.procom_io import ProcomIO
from procom.procom_image_converter import ProcomImageConverter
from procom.constants import *

root = Path(__file__).parent.parent
logo = root / "assets/procom_logo.png"
el_header = root / "assets/headers/etat_livraison.png"
je_header = root / "assets/headers/journal_encaissement.png"
search = root / "assets/recherche.png"


def checking(window: Window):
    running = False
    while True:
        print("Checking Time, window ? ", running)
        # rand_number = randrange(1, 10)
        window.is_running = running
        # window.checking()
        time.sleep(2)
        running = not running


def actions(window: Window):
    while True:

        window.perform_actions() if window.is_running else print(
            f"{window.name} is not running, go next iteration"
        )

        ProcomIO.save(window, "1/0", "qte", (94, 760, 78, 15))
        # try some stupid
        result = ProcomImageConverter.convert(
            "../output/1_0.qte.png", zoom=1, zoom_max=2
        )
        if result is None:
            print("1/0[qte] -> NONE")
        else:
            print("1/0[qte]-->data:{}, zoom:{}".format(*result))
        time.sleep(10)


# def main():


# el_location = x_etat_livraison, y_etat_livraison
# je_location = x_journal_encaissement, y_journal_encaissement

# main_ = {
#     "check_asset": logo,
#     "assume_location": logo_location,
# }

# el = {
#     "search": search,
#     "start_position": DATE_DEBUT_POSITION,
#     "end_position": DATE_FIN_POSITION,
#     "reference_position": REFERENCE_POSITION,
# }

# je = {
#     "search": search,
#     "start_position": DATE_DEBUT_POSITION,
#     "end_position": DATE_FIN_POSITION,
# }

# etat_livraison = Window(
#     "Etat Livraison", asset=el_header, location=el_location, **el
# )
# journal_encaissement = Window(
#     "Journal Encaissement", asset=je_header, location=je_location, **je
# )

# while True:
#     main_window.checking()
#     is_main_run = "is running" if main_window.is_running else "is not running"
#     print("{} window".format(main_window.name), is_main_run)

# etat_livraison.checking()
# is_el_run = "is running" if etat_livraison.is_running else "is not running"
# print("etat livraison window", is_el_run)

# journal_encaissement.checking()
# is_je_run = (
#     "is running" if journal_encaissement.is_running else "is not running"
# )
# print("journal encaissement window", is_je_run)

# time.sleep(5)


if __name__ == "__main__":
    logo_location = x_logo, y_logo
    main_window = MainWindow(check_asset=logo, assume_location=logo_location)

    checker = Thread(target=checking, args=(main_window,), daemon=True)
    checker.start()
    actions(main_window)
