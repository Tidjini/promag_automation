import pyautogui
BOTTOM_LINE = 1000, 1050

'''Observer class'''


class Observable:

    def __init__(self) -> None:
        '''Init a list of observers'''
        self._observers = []

    def notify(self):
        '''when event fire, notify and update the observers

        Important: all Observers has notify method
        '''
        for observer in self._observers:
            observer.notify(self)

    def subscribe(self, observer):
        '''subscribtion'''
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubcribe(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass


class WindowObservable(Observable):
    '''Window Observer

    if window is running fire all observers registerd,
    asset represent the image to track in window, and location for presume image location
    to check with result
    '''

    def __init__(self, name: str, asset: str, location: tuple) -> None:
        '''Window Observer 

        set name, asset <image path>, location <(x, y)>
        '''

        super().__init__()

        self.name = name
        self.asset = asset
        self.location = location
        self._is_running = False

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        self._is_running = value
        # fire observers notification
        self.notify()

    def deactivate_window(self):
        '''Set headers to disable mode.

        to match with window assets
        '''
        pyautogui.moveTo(*BOTTOM_LINE)
        pyautogui.click()

    def checking(self, deactivate=False):
        '''checking if window is running

        using pyautogui with center location of an image
        '''
        try:
            if deactivate:
                self.is_running = False
                self.deactivate_window()

            x, y = pyautogui.locateCenterOnScreen(self.asset)
            win_x, win_y = self.location
            self.is_running = win_x == x and win_y == y
        except (FileNotFoundError, TypeError):
            self.is_running = False
