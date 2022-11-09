from enum import Enum
import abc
from abc import ABCMeta

# Abstract Base Class, defining methods that need to be implemented
# platform-specific
class PlatformAbc(metaclass=ABCMeta):
    # Enum mapping UI buttons to keyboard buttons. Name refers to display name of the button
    # in the UI, value refers to keyboard button
    class Buttons(Enum):
        A = "X",
        B = "X",

    # takes a screenshot of the client and returns the file name
    @abc.abstractmethod
    def screenshot(self) -> str:
        raise NotImplementedError()

    # handles a button press
    @abc.abstractmethod
    def button_press(self):
        raise NotImplementedError()
