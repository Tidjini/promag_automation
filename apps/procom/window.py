import time
from typing import Any
from abc import ABC, abstractmethod

# check for from _typeshed import Self
# third-party
import pyautogui

# constants
BOTTOM = 1000, 1050


class Window(ABC):
    """Window

    main purpose is check the window running and perfom some actions
    """

    def __init__(self, **kwargs) -> None:
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
    def perform_actions(self, *args, **kwargs) -> None:
        """implement perform actions in sub class"""
        pass

    def click(self, location) -> None:
        """Generic click function by position"""
        pyautogui.click(*location)

    def deactivate(self) -> None:
        """to lose window focus, capture become more gray"""
        self.click(*BOTTOM)

    def write(self, location: tuple, text: str) -> None:
        # write data to spcific field by position
        pyautogui.doubleClick(*location)
        pyautogui.write(text)

    def checking(self) -> None:
        """checking if window is running"""

        try:
            # if the asset is in same location with our location, then window is running
            x, y = pyautogui.locateCenterOnScreen(self.check_asset)
            win_x, win_y = self.assume_location
            self.is_running = x == win_x and y == win_y

        except (FileNotFoundError, TypeError):
            self.is_running = False

    def double_check(self) -> None:
        """double check to avoid active / non active windows

        cause pyautogui make no difference between images,
        so this helps to check both active/non active asset
        """
        self.checking(self.check_asset)
        if self.is_running:
            return
        self.checking(self.check_active_asset)

    def navigate_to(self, asset) -> Any:
        """navigate to a given asset"""
        try:
            x, y = pyautogui.locateCenterOnScreen(asset)
            pyautogui.moveTo(x, y)
            return x, y
        except (FileNotFoundError, TypeError):
            return None

    def click_asset(self, asset: str) -> None:
        """navigate and click on given asset"""
        try:
            x, y = self.navigate_to(asset)
        except TypeError as e:
            raise TypeError("click an asset exception due to:", e)
        self.click((x, y))

    def __enter__(self):
        """use 'with' keyword to perform actions on this object"""

        if self.is_running:
            return self
        try:
            # click on menu button with image asset
            self.click_asset(self.menu)
            time.sleep(1)
            # after opening the menu click on sub_menu button
            self.click_asset(self.sub_menu)
            time.sleep(2)
            # make state of this window as running
            self.is_running = True
        except TypeError as e:
            self.is_running = False

        return self

    def __exit__(self) -> None:
        """when we run out of 'with' bloc close this window"""

        if not self.is_running:
            return

        # make is_running False whatever the result of closing
        self.is_running = False
        try:
            self.click_asset(self.close_asset)
        except TypeError:
            pass


class MainWindow(Window):
    _name = "MAIN"

    def __init__(self, check_asset: str, assume_location: tuple) -> None:
        super().__init__(check_asset=check_asset, assume_location=assume_location)

    def perform_actions(self, *args, **kwargs) -> None:
        print(f"{self.name} perform actions")

    @property
    def name(self) -> str:
        return self._name
