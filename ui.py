import sys
import threading

import backgroundMusic
import main
import screenDetection
import Deer
import pygetwindow as gw
import time
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtCore import QTimer, QTime, QRegExp
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, \
    QPushButton, QLCDNumber


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
        btnStart.setFixedSize(70, 25)
        btnVolStop = QPushButton("Mute", self)
        btnVolStop.setFixedSize(70, 25)
        btnVolStop.move(5, 410)
        btnVolResume = QPushButton("Resume", self)
        btnVolResume.setFixedSize(70, 25)
        btnVolResume.move(5, 385)
        btnQuit = QPushButton("Exit", self)
        btnQuit.setFixedSize(70, 25)
        btnQuit.move(820, 410)
        btnQuit.clicked.connect(self.close)

        # Connect the button to a function
        btnStart.clicked.connect(self.get_input)
        btnVolStop.clicked.connect(musicPlayer.stopMusic)
        btnVolResume.clicked.connect(musicPlayer.playMusic)

        # Set the window properties
        self.setGeometry(200, 200, 900, 450)
        self.setWindowTitle("Deer Timer")

        # create timer
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(8)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setStyleSheet(
            "QLCDNumber { background-color: transparent; color: #B3A28A; }")
        self.lcd.setFixedSize(450, 250)
        self.lcd.move(215, -75)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        # Create a new timer for the countdown
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_time)

        # Create a new deer
        deer_pixmap = QPixmap('deer_photos/3_normal.png')
        deer_pixmap = deer_pixmap.scaled(330, 330)
        deer_label = QLabel(self)
        deer_label.setPixmap(deer_pixmap)
        deer_label.setGeometry(280, 95, 330, 330)
        self.deer_label = deer_label
        self.deer = Deer.Deer()

        self.screenDetectorStatus = "DEERTAB"

    def closeEvent(self, event):
        """
        Override the default close event handler.
        The modified handler exits the program and stops the music.
        """
        musicPlayer.stopMusic()
        event.accept()
        main.app.quit()
        sys.exit()

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
            detector_thread = threading.Thread(target=screenDetector.check, args=(self,))
            detector_thread.daemon = True
            detector_thread.start()
            bg_music_thread = threading.Thread(target=backgroundMusic.run, args=(musicPlayer,))
            bg_music_thread.daemon = True
            bg_music_thread.start()


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
            self.check_deer()
            self.secs -= 1
            self.lcd.display(
                QTime.fromMSecsSinceStartOfDay(self.secs * 1000).toString(
                    'hh:mm:ss'))
        else:
            self.countdown_timer.stop()
            self.timer.start()

    def update_deer(self, filename):
        """
        Update self.deer_pixmap with new pixmap
        """
        deer_pixmap = QPixmap(filename)
        deer_pixmap = deer_pixmap.scaled(330, 330)
        self.deer_label.setPixmap(deer_pixmap)
        self.deer_label.setGeometry(280, 95, 330, 330)

    def check_deer(self):
        if self.screenDetectorStatus == "DEERTAB":
            self.deer.put_out_fire()
            filename = f'deer_photos/{self.deer.status}_normal.png'
            self.update_deer(filename)
        else:
            deer_thread = threading.Thread(target=self.deer.set_on_fire)
            deer_thread.daemon = True
            deer_thread.start()
            filename = f'deer_photos/{self.deer.status}_fire/frame2.png'
            self.update_deer(filename)
