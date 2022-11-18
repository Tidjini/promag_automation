import pyautogui

BOTTOM = 1000, 1050


class Window:
    def __init__(self, name: str, asset: str, location: tuple, **kwargs) -> None:
        self.name = name
        self.asset = asset
        self.location = location
        self._is_running = False
        # set other properties from kwargs
        self.__dict__.update(kwargs)

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        self._is_running = value

    def click(self, location):
        """Generic click function by position"""
        pyautogui.click(*location)

    def deactivate(self):
        """to lose window focus, capture become more gray"""
        self.click(*BOTTOM)

    def write(self, location: tuple, text: str):
        # write data to spcific field by position
        pyautogui.doubleClick(*location)
        pyautogui.write(text)

    def checking(self, deactive=False):
        """checking if window is running"""

        if deactive:
            self.deactivate()

        try:
            # if the asset is in same location with our location, then window is running
            x, y = pyautogui.locateCenterOnScreen(self.asset)
            win_x, win_y = self.location
            self.is_running = x == win_x and y == win_y

        except (FileNotFoundError, TypeError):
            self.is_running = False

    def navigate_to_search(self) -> tuple:
        try:
            x, y = pyautogui.locateCenterOnScreen(self.search)
            pyautogui.moveTo(x, y)
            return x, y
        except (FileNotFoundError, TypeError):
            return None
