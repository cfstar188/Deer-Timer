import threading

import backgroundMusic
import screenDetection
import pygetwindow as gw
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtCore import QTimer, QTime, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QLCDNumber

musicPlayer = backgroundMusic.Music()
screenDetector = screenDetection.Detector()


class Window(QWidget):
    def __init__(self):
        """
        Initialize the canvas, buttons and set up the connections.
        """
        super().__init__()

        self.curr_tab = None
        self.deer_tab = gw.getActiveWindow()
        self.prev_tab = None
        self.i = 1
        self.counter = 0

        self.secs = -1
        self.changeWindows = 0
        self.other = False

        # Add a background image
        self.background_image = QLabel(self)
        self.background_image.setGeometry(0, 0, 900, 450)
        self.background_image.setPixmap(QPixmap("defimg.jpeg"))

        # Create a label
        self.label = QLabel("Focus time:", self)
        self.label.setStyleSheet("QLabel { color : #35312C; }")
        self.label.move(295, 415)

        # Create a line edit widget
        self.line_edit = QLineEdit(self)
        self.line_edit.setStyleSheet(
            "QLineEdit { background-color: transparent; color: #35312C; }")
        hourreg = QRegExp("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")
        hourvalid = QRegExpValidator(hourreg)
        self.line_edit.setValidator(hourvalid)
        self.line_edit.move(370, 415)

        # Create a button
        btnStart = QPushButton("Start", self)
        btnStart.move(495, 410)
        btnVolStop = QPushButton("Mute", self)
        btnVolStop.setFixedSize(70, 25)
        btnVolStop.move(5, 410)
        btnVolResume = QPushButton("Resume", self)
        btnVolResume.setFixedSize(70, 25)
        btnVolResume.move(5, 385)

        # Connect the button to a function
        btnStart.clicked.connect(self.get_input)
        btnVolStop.clicked.connect(musicPlayer.stopMusic)
        btnVolResume.clicked.connect(musicPlayer.playMusic)

        # Set the window properties
        self.setGeometry(200, 200, 900, 450)
        self.setWindowTitle("Focus")

        # create timer
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setStyleSheet(
            "QLCDNumber { background-color: transparent; color: #B3A28A; }")
        self.lcd.setFixedSize(450, 250)
        self.lcd.move(205, -30)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        # Create a new timer for the countdown
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_time)

    def get_input(self):
        """
        Get the input from user and start the countdown and music.
        """
        input_num = self.line_edit.text()

        if input_num:
            input_num = int(input_num)
            self.secs = input_num * 60
            self.timer.stop()
            self.countdown_timer.start(1000)
            detector_thread = threading.Thread(target=screenDetector.check)
            detector_thread.start()
            backgroundMusic.run(musicPlayer)
            self.deer_tab = gw.getActiveWindow()

    def showTime(self):
        """
        Display the current time.
        """
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.lcd.display(current_time)

    def update_time(self):
        """
        Display the countdown time.
        """
        if self.secs > 0:
            self.secs -= 1
            self.lcd.display(
                QTime.fromMSecsSinceStartOfDay(self.secs * 1000).toString(
                    'hh:mm:ss'))
        else:
            self.countdown_timer.stop()
            self.timer.start()

    def update_background(self, imgname):
        """
        Update the background of the app.
        """
        self.background_image.setPixmap(QPixmap(imgname))
