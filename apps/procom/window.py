from abc import ABC, abstractmethod
import pyautogui

BOTTOM = 1000, 1050


class Window(ABC):
    def __init__(self, name: str, location: tuple, **kwargs) -> None:
        self.name = name
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

    @abstractmethod
    def perform_actions(self, *args, **kwargs):
        pass

    @abstractmethod
    def open(self, *args, **kwargs):
        pass

    @abstractmethod
    def close(self, *args, **kwargs):
        pass

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

    def checking(self):
        """checking if window is running"""

        try:
            # if the asset is in same location with our location, then window is running
            x, y = pyautogui.locateCenterOnScreen(self.asset)
            win_x, win_y = self.location
            self.is_running = x == win_x and y == win_y

        except (FileNotFoundError, TypeError):
            self.is_running = False

    def double_check(self):
        self.checking(self.asset)
        if self.is_running:
            return
        self.checking(self.active_asset)

    def navigate_to(self, asset):
        try:
            x, y = pyautogui.locateCenterOnScreen(asset)
            pyautogui.moveTo(x, y)
            return x, y
        except (FileNotFoundError, TypeError):
            return None

    def click_asset(self, asset: str) -> None:
        try:
            x, y = self.navigate_to(asset)
        except TypeError as e:
            raise TypeError("click an asset exception due to:", e)
        self.click((x, y))
