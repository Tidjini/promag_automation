import socketio
import time

sio = socketio.Client()

messages = [f"message {i}" for i in range(1, 10)]


@sio.event
def connect():
    print('connection established')
    while messages:
        message = messages.pop(0)
        sio.emit('message', {'message': message})
        print(f'{message} sended with success')
        time.sleep(3)


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server, rest messages', len(messages))


sio.connect('https://eassalnotif.herokuapp.com/notify/')
sio.wait()
