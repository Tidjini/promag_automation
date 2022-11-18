import pyautogui

BOTTOM = 1000, 1050


class Window:

    def __init__(self, name: str, asset: str, location: tuple) -> None:

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

    def click(self, position):
        '''to lose window focus, capture become more gray'''
        pyautogui.moveTo(*position)
        pyautogui.click()

    def deactivate(self):
        '''to lose window focus, capture become more gray'''
        self.click(*BOTTOM)

    def write(self, location: tuple, text: str):
        # write data to spcific field by position
        pyautogui.doubleClick(*location)
        pyautogui.write(text)

    def checking(self, perform_deactive):
        '''checking if window is running'''

        if perform_deactive:
            self.deactivate()

        try:
            # if the asset is in same location with our location, then window is running
            x, y = pyautogui.locateCenterOnScreen(self.asset)
            win_x, win_y = self.location
            self.is_running = x == win_x and y == win_y

        except (FileNotFoundError, TypeError):
            self.is_running = False


class DateIntervalWindow(Window):

    def __init__(self, name: str, asset: str, location: tuple, start_position: tuple, end_position: tuple):
        super().__init__(name, asset, location)
        self.start_position = start_position
        self.end_position = end_position


class ReferenceWindow(Window):

    def __init__(self, name: str, asset: str, location: tuple, reference_position: tuple):
        super().__init__(name, asset, location)
        self.reference_position = reference_position


class SearchWindow(Window):
    def __init__(self, name: str, asset: str, location: tuple, search: str) -> None:
        super().__init__(name, asset, location)
        self.search = search

    def navigate_to_search(self) -> tuple:
        x, y = pyautogui.locateCenterOnScreen(self.search)
        pyautogui.moveTo(x, y)
        return x, y


class EtatLivraison(DateIntervalWindow, ReferenceWindow, SearchWindow):

    def __init__(self, name: str, asset: str, location: tuple, start_position: tuple, end_position: tuple, reference_position: tuple, search: st):
        DateIntervalWindow.__init__(
            self, name, asset, location, start_position, end_position)
        ReferenceWindow.__init__(
            self, name, asset, location, reference_position)
        SearchWindow.__init__(self, name, asset, location, search)
