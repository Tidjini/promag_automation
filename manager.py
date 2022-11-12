import time
from datetime import datetime
import pyautogui

from helpers import formelize
from constants import *

now = datetime.now()
# format date to match the software input pattern
today = "{:02d}{:02d}{:04d}".format(now.day, now.month, now.year)


def software_is_running():
    """Check if software is still running by check.png


    Check is a png image of sample window header
    """
    try:
        x, y = pyautogui.locateCenterOnScreen("assets/check.png")
        print(x, y)
        if x_check == x and y_check == y:
            print("Procom available continue working")
            return True
    except TypeError as e:
        print(e)

    print("Procom is no available quit")
    return False


def save_data(ref, label, region):
    img = pyautogui.screenshot(region=region)
    ref = formelize(ref)
    img.save("outputs/{}.{}.png".format(ref, label))


def perform_actions(ref):
    """Take all actions needed to get data.


    insert data in there position in software:
        - Start Date (DATE_DEBUT)
        - End  Date (DATE_FIN)
        - Product Reference (REFRENCE)
        - click on Search Button with : assets/recherche.png
    """

    print("{}:{}".format(ref, datetime.now()))
    pyautogui.doubleClick(*DATE_DEBUT_POSITION)
    pyautogui.write(DATE_DEBUT)
    pyautogui.doubleClick(*DATE_FIN_POSITION)
    pyautogui.write(today)
    pyautogui.doubleClick(*REFERENCE_POSITION)
    pyautogui.write(ref)
    x, y = pyautogui.locateCenterOnScreen("assets/recherche.png")
    pyautogui.moveTo(x, y)
    pyautogui.click()


def main():
    while True:
        is_running = software_is_running()
        if not is_running:
            print(
                "*" * 10,
                "game over ;) {} leave Procom now".format(datetime.now()),
                "*" * 10,
            )
            break

        print("*" * 10, "iteration: {}".format(datetime.now()), "*" * 10)
        try:
            for ref in PRODUCTS:
                perform_actions(ref)
                # wait of results
                time.sleep(NEXT_PRODUCT)
                # save data
                print("collecting {} : {}".format(ref, datetime.now()))
                for label, region in (("qte", QTE_REGION), ("mtn", MTN_REGION)):
                    save_data(ref, label, region)

        except Exception as e:
            print("Exception due to {}".format(e))
            break
        # wait for refresh time to re-execute, automation, each 2 minutes
        time.sleep(REFRESH_TIME)


if __name__ == "__main__":
    main()
