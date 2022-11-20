import time
from pathlib import Path

# third-party
import pyautogui

root = Path(__file__).parent.parent

assets = root / 'assets'
headers = assets / 'headers'
menu = assets / 'menu'
output = root / 'output'
etat = headers/'journal_encaissement.png'

time.sleep(5)
# region = pyautogui.locateOnScreen(str(etat))
region = (4, 24, 178, 49)
img = pyautogui.screenshot(region=region)
print(region)
img.save("{}/active.png".format(headers))
