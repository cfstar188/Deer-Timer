import random
import os.path
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication
import threading


class Music():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.player = QMediaPlayer()
        self.num = random.randint(0, 3)
        self.mediaUrl = None
        self.mediaPath = None
        self.mediaContent = None

    def getContent(self):
        # get the path of the file
        if self.num == 0:
            self.mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
        if self.num == 1:
            self.mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
        if self.num == 2:
            self.mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
        else:
            self.mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
        self.mediaUrl = QUrl.fromLocalFile(self.mediaPath)
        self.mediaContent = QMediaContent(self.mediaUrl)
        return self.mediaContent

    def playMusic(self):
        self.player.play()
        while self.player.state() == QMediaPlayer.PlayingState:
            self.app.processEvents()
            # UI IMPLEMENTATION
            # if User wants it to pause:
            #     self.pauseMusic():
            # elif User wants it to stop:
            #     self.stopMusic()

    def pauseMusic(self):
        self.player.pause()

    def stopMusic(self):
        self.player.stop()


if __name__ == "__main__":
    """ Example use"""
    musicPlayer = Music()

    content = musicPlayer.getContent()
    musicPlayer.player.setMedia(content)

    musicThread = threading.Thread(target=musicPlayer.playMusic())
    musicThread.daemon = True
    musicThread.start()
