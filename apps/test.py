import time
from datetime import datetime
from pathlib import Path
from procom.procom_image_converter import ProcomImageConverter

# third-party
import pyautogui

root = Path(__file__).parent.parent

assets = root / 'assets'
headers = assets / 'headers'
menu = assets / 'menu'
output = root / 'output'
delivery_status_active = headers/'delivery_status_active.png'
etat = headers/'journal_encaissement.png'

# time.sleep(5)
# # # region = pyautogui.locateOnScreen(str(etat))
# # region = (4, 24, 178, 49)
# # img = pyautogui.screenshot(region=region)
# # print(region)
# # img.save("{}/active.png".format(headers))

# region = pyautogui.locateCenterOnScreen(str(delivery_status_active))
# now = datetime.now()
# print(f'{region}')

pt = headers / 'enc.png'
data, zoom = ProcomImageConverter.convert(path=str(pt))
print(data, zoom)
