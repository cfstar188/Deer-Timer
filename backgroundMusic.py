import random
import os.path
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import QApplication
import threading


class Music:
    """
    A music player that plays a background music.
    """
    def __init__(self):
        """
        Initialize a music player.
        """
        self.app = QApplication(sys.argv)
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.num = random.randint(0, 3)
        self.mediaUrl = None
        self.mediaPath = None
        self.mediaContent = None

    def getContent(self):
        """
        Return the music content of a song.
        """
        # get the path of the file
        if self.num == 0:
            self.mediaPath = os.path.join(os.getcwd(), "rain.mp3")
        elif self.num == 1:
            self.mediaPath = os.path.join(os.getcwd(), "fire.mp3")
        elif self.num == 2:
            self.mediaPath = os.path.join(os.getcwd(), "bird.mp3")
        else:
            self.mediaPath = os.path.join(os.getcwd(), "piano.mp3")
        self.mediaUrl = QUrl.fromLocalFile(self.mediaPath)
        self.mediaContent = QMediaContent(self.mediaUrl)
        return self.mediaContent

    def playMusic(self):
        """
        Play particular music.
        """
        self.playlist.addMedia(self.getContent())
        self.playlist.setPlaybackMode(self.playlist.Loop)
        self.player.setPlaylist(self.playlist)

        self.player.play()

    def stopMusic(self):
        """
        If a user presses the stop button, the music will be stopped.
        """
        self.player.stop()


def run(musicPlayer):
    """
    Start to run the music player.
    """
    content = musicPlayer.getContent()
    musicPlayer.player.setMedia(content)

    musicThread = threading.Thread(target=musicPlayer.playMusic())
    musicThread.daemon = True
    musicThread.start()

    while True:
        musicPlayer.app.processEvents()
