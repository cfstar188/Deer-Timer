import pygetwindow as gw
import threading


class Detector:
    """
    Check if a user switches window.
    """
    def __init__(self):
        """
        Initialize a detector.
        """
        self.curr_tab = None
        self.deer_tab = gw.getActiveWindow()
        self.prev_tab = None
        self.i = 1

    def check(self):
        """
        Check if a user switches to a different window.
        """
        while True:
            self.curr_tab = gw.getActiveWindow()
            if self.curr_tab == self.deer_tab:
                self.i = 0
            else:
                if self.curr_tab != self.deer_tab and \
                        self.prev_tab != self.curr_tab and self.i == 0:
                    self.i = 1
            self.prev_tab = self.curr_tab


if __name__ == "__main__":
    """ Example use"""
    detector = Detector()

    detector_thread = threading.Thread(target=detector.check())
