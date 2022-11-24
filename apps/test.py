# import time
# from datetime import datetime
# from pathlib import Path
# from procom.procom_image_converter import ProcomImageConverter

# # third-party
# import pyautogui

# root = Path(__file__).parent.parent

# assets = root / 'assets'
# headers = assets / 'headers'
# menu = assets / 'menu'
# output = root / 'output'
# delivery_status_active = headers/'delivery_status_active.png'
# etat = headers/'journal_encaissement.png'

# # time.sleep(5)
# # # # region = pyautogui.locateOnScreen(str(etat))
# # # region = (4, 24, 178, 49)
# # # img = pyautogui.screenshot(region=region)
# # # print(region)
# # # img.save("{}/active.png".format(headers))

# # region = pyautogui.locateCenterOnScreen(str(delivery_status_active))
# # now = datetime.now()
# # print(f'{region}')

# t = headers / 'enc.png'
# img = pyautogui.locateOnScreen(str(t))
# print(img)
# img.save('{}/collection_journal_actdve.png'.format(headers))


# import socketio
# import time

# sio = socketio.Client()

# messages = [f"message {i}" for i in range(1, 10)]


# @sio.event
# def connect():
#     print('connection established')
#     for message in messages:
#         sio.emit('message', {'message': message})
#         print(f'{message} sended with success')
#         messages.pop(0)
#         time.sleep(3)


# @sio.event
# def my_message(data):
#     print('message received with ', data)
#     sio.emit('my response', {'response': 'my response'})


# @sio.event
# def disconnect():
#     print('disconnected from server, rest messages', len(messages))


# sio.connect('https://eassalnotif.herokuapp.com/notify/')
# sio.wait()

import pyautogui
from pathlib import Path

output = Path(__file__).parent.parent / 'output'

img = pyautogui.screenshot(region=(15, 20, 100, 100))
file = "{}\{}.{}.png".format(output, 'o', 'q')
img.save(file)

# with open('C:\\Projects\\python\\autosaver\\output\\temp.qte.png'.replace('\\', '/')) as file:
#     print('File ', file)
