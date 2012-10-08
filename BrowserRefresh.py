import os
import sys
import platform

import sublime
import sublime_plugin

# Fix windows imports
__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

if __path__ not in sys.path:
    sys.path.insert(0, __path__)

_pywinauto = os.path.join(__path__ + os.path.sep + 'win')
if _pywinauto not in sys.path:
    sys.path.insert(0, _pywinauto)

# Cache user operating system
_os = platform.system()


class BrowserRefreshCommand(sublime_plugin.TextCommand):
    def run(self, args, activate_browser=True,
        browser_name="all", auto_save=True,
        delay=None):

        # Auto-save
        if auto_save == True and self.view and self.view.is_dirty():
            self.view.run_command("save")

        # Detect OS and import
        if _os == 'Darwin':
            from mac import MacBrowserRefresh
            refresher = MacBrowserRefresh(activate_browser)
        elif _os == 'Windows':
            from win import WinBrowserRefresh
            refresher = WinBrowserRefresh(activate_browser)
        else:
            sublime.error_message('Your operating system is not supported')

        # Delay refresh
        if delay is not None:
            import time
            time.sleep(delay)

        # Actually refresh browsers
        if browser_name == "Google Chrome":
            refresher.chrome()

        elif browser_name == "Safari":
            refresher.safari()

        elif browser_name == "Firefox":
            refresher.firefox()

        elif browser_name == "Opera":
            refresher.opera()

        elif browser_name == 'IE' and _os == 'Windows':
            refresher.ie()

        elif browser_name == 'all':
            refresher.chrome()
            refresher.safari()
            refresher.firefox()
            refresher.opera()

            if _os == 'Windows':
                refresher.ie()
