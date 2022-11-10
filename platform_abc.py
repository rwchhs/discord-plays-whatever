from enum import Enum
import abc
from abc import ABCMeta
import os
import glob

# Abstract Base Class, defining methods that need to be implemented
# platform-specific
class PlatformAbc(metaclass=ABCMeta):
    # Enum mapping UI buttons to keyboard buttons. Name refers to display name of the button
    # in the UI, value refers to keyboard button
    class Buttons(Enum):
        A = "X",
        B = "X",

    # constructor
    def __init__(self, config: dict) -> None:
        self.config = config

    # takes a screenshot of the client and returns the file name
    @abc.abstractmethod
    def screenshot(self) -> str:
        raise NotImplementedError()

    # handles a button press
    @abc.abstractmethod
    def button_press(self):
        raise NotImplementedError()

    # get the client window
    @abc.abstractmethod
    def get_window(self):
        raise NotImplementedError()

    # TODO: this should be in a more generic helper/util class
    def cleanup(self) -> None:
        # cleanup temporary screenshots
        files = glob.glob("./tmp/screenshots/screen_*.png")
        for file in files:
            try:
                os.remove(file)
            except:
                pass

    def run_client(self, rom_path: str) -> None:
        raise NotImplementedError()
