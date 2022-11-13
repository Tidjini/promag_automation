import time
from datetime import datetime
import pyautogui

from helpers import formalize
from data_handler import extract_info, push_data
from constants import *

now = datetime.now()
# format date to match the software input pattern
today = "{:02d}{:02d}{:04d}".format(now.day, now.month, now.year)


# better way is to use threading with,
# global variable to track if software is still running
# !IMPORTANT: be careful with threading and actions todo.
is_running = False


def software_is_running():
    """Check if software is still running by check.png
    Check is a png image of sample window header
    """
    try:
        # to disable active procom window, to match the check png (capture in inactive mode)
        pyautogui.moveTo(*BOTTOM_LINE)
        pyautogui.click()
        x, y = pyautogui.locateCenterOnScreen("assets/check.png")
        if x_check == x and y_check == y:
            print("Procom available continue working")
            return True
    except TypeError as e:
        print(e)

    print("Procom is no available quit")
    return False


def save_data(ref, label, region):
    img = pyautogui.screenshot(region=region)
    ref = formalize(ref)
    img.save("output/{}.{}.png".format(ref, label))


def perform_actions(ref):
    """Take all actions needed to get data.
    insert data in there position in software:
        - Start Date (DATE_DEBUT)
        - End  Date (DATE_FIN)
        - Product Reference (REFRENCE)
    then click on Search Button with : assets/recherche.png
    """

    is_running = software_is_running()
    if not is_running:
        return False

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
    return True


def main():
    is_running = software_is_running()
    while is_running:
        print("*" * 10, "{}".format(datetime.now()), "*" * 10)
        try:
            for ref, designation in PRODUCTS:
                break_through = not perform_actions(ref)
                # if software still running preform actions
                if break_through:
                    break
                # wait of results
                time.sleep(NEXT_PRODUCT)
                # to not get some outputs errors
                is_running = software_is_running()
                if not is_running:
                    break
                # save data
                print("collecting {} : {}".format(ref, datetime.now()))
                data = {}
                ref = formalize(ref)
                for label, region in (("qte", QTE_REGION), ("mtn", MTN_REGION)):

                    save_data(ref, label, region)
                    data[label] = extract_info(ref, label)

                push_data(ref, designation, data["qte"], data["mtn"])

        except Exception as e:
            print("Exception due to {}".format(e))
            break
        # wait for refresh time to re-execute, automation, each 2 minutes
        time.sleep(REFRESH_TIME)
        is_running = software_is_running()
    else:
        print(
            "*" * 10,
            "game over ;) {} leave Procom now".format(datetime.now()),
            "*" * 10,
        )


if __name__ == "__main__":
    main()
