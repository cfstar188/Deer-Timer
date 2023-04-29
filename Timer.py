import time
import math
import threading

ONGOING = "ONGOING"
STOPPED = "STOPPED"


class Timer:
    """Facilitates creating and decrementing the timer"""

    def __init__(self, start_time):
        """Create a new Timer object"""
        self.start_time = start_time
        self.current_time = start_time
        self.status = STOPPED

    def get_time(self):
        """Return a string that is self.current_time in the format of hours:minutes:seconds"""
        current_time = self.current_time
        hours = math.floor(current_time / 3600)
        minutes = math.floor(current_time / 60) % 60
        seconds = current_time % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def start(self):
        """Countdown the timer from self.start_time. At the end of execution, self.stop() is invoked."""
        self.status = ONGOING
        while self.status != STOPPED and self.current_time > 0:
            print(self.get_time())  # replace this line with code that displays the time in the GUI
            time.sleep(1)
            self.current_time -= 1
        self.stop()

    def stop(self):
        """Stops the timer"""
        self.status = STOPPED
        print("TIMER STOPPED")  # replace this line with code that displays the end of the timer in the GUI


if __name__ == "__main__":
    """An example of how to use the Timer object"""
    # set a new Timer object that would start from 20 seconds
    timer = Timer(20)

    # create and execute a new timer thread to start the timer
    timer_thread = threading.Thread(target=timer.start)
    timer_thread.daemon = True
    timer_thread.start()

    # sleep for 10 seconds
    time.sleep(10)

    # end timer prematurely
    timer.stop()
    print(f"The timer stopped at {timer.current_time} seconds")
