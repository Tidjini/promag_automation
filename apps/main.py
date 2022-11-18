import time
from pathlib import Path
from procom.window import MainWindow

from constants import *

root = Path(__file__).parent.parent
logo = root / "assets/procom_logo.png"
el_header = root / "assets/headers/etat_livraison.png"
je_header = root / "assets/headers/journal_encaissement.png"
search = root / "assets/recherche.png"


def main():

    logo_location = x_logo, y_logo
    el_location = x_etat_livraison, y_etat_livraison
    je_location = x_journal_encaissement, y_journal_encaissement

    main_ = {
        "check_asset": logo,
        "assume_location": logo_location,
    }

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
    main_window = MainWindow(check_asset=logo, assume_location=logo_location)

    # etat_livraison = Window(
    #     "Etat Livraison", asset=el_header, location=el_location, **el
    # )
    # journal_encaissement = Window(
    #     "Journal Encaissement", asset=je_header, location=je_location, **je
    # )

    while True:
        main_window.checking()
        is_main_run = "is running" if main_window.is_running else "is not running"
        print("{} window".format(main_window.name), is_main_run)

        # etat_livraison.checking()
        # is_el_run = "is running" if etat_livraison.is_running else "is not running"
        # print("etat livraison window", is_el_run)

        # journal_encaissement.checking()
        # is_je_run = (
        #     "is running" if journal_encaissement.is_running else "is not running"
        # )
        # print("journal encaissement window", is_je_run)

        time.sleep(5)


if __name__ == "__main__":
    main()
