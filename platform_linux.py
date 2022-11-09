from platform_abc import PlatformAbc
import pyautogui
import pywinctl
import time


class PlatformLinux(PlatformAbc):
    async def screenshot(self) -> str:
        pag = pyautogui

        # TODO: make this configurable to accomodate other client software
        pwc = pywinctl.getWindowsWithTitle("mGBA")[0]

        # window needs to be in the foreground in order for screenshot to work
        pwc.activate()

        # this seemed to be necessary because screenshot() kept capturing black rectangles without it
        time.sleep(1)
        
        # uses the timestamp as a filename because just using "screenshot.png" and overwriting that
        # one didn't work. This will, however, clutter of your filesystem.
        # TODO: remove those screenshots at some point
        filename = str(time.time()) + ".png"
        
        pag.screenshot(filename, region=(pwc.left, pwc.top, pwc.width, pwc.height))
        
        return filename

    async def button_press(self, button: PlatformAbc.Buttons):
        # TODO: make this configurable to accomodate other client software
        pwc = pywinctl.getWindowsWithTitle("mGBA")[0]
        
        # window needs to be in the foreground in order for input to work
        pwc.activate()
        time.sleep(1)

        # TODO: this doesn't really work, even though button.value contains the right
        # value and it *does* work for outputting that letter into, e.g., a text editor
        p = pyautogui.press(button.value[0])
        
        return
