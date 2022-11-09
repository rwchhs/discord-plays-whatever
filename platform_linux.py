from platform_abc import PlatformAbc
import pyautogui
import pywinctl
import time


class PlatformLinux(PlatformAbc):

    def get_window(self) -> pywinctl.LinuxWindow:
        pwc = pywinctl.getWindowsWithTitle(self.config["WINDOW_TITLE"])[0]

        # window needs to be in the foreground in order for screenshot to work
        pwc.activate()

        return pwc

    async def screenshot(self) -> str:
        pag = pyautogui

        window = self.get_window()

        # this seemed to be necessary because screenshot() kept capturing black rectangles without it
        time.sleep(1)

        # uses the timestamp as a filename because just using "screenshot.png" and overwriting that
        # one didn't work.
        filename = "./tmp/screenshots/" + str(time.time()) + ".png"

        pag.screenshot(filename, region=(
            window.left, window.top, window.width, window.height))

        return filename

    async def button_press(self, button: PlatformAbc.Buttons):
        self.get_window()
        time.sleep(1)

        # TODO: this doesn't really work, even though button.value contains the right
        # value and it *does* work for outputting that letter into, e.g., a text editor
        pyautogui.press(button.value[0])

        return
