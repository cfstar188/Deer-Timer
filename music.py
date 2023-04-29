import random
import os.path
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication


def getContent(num):
    # get the path of the file
    if num == 0:
        mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
    if num == 1:
        mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
    if num == 2:
        mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
    else:
        mediaPath = os.path.join(os.getcwd(), "rainSound.mp3")
    mediaUrl = QUrl.fromLocalFile(mediaPath)
    mediaContent = QMediaContent(mediaUrl)
    return mediaContent


def playMusic():
    player.play()
    while player.state() == QMediaPlayer.PlayingState:
        app.processEvents()
        if User wants it to pause:
            pauseMusic():
        elif User wants it to stop:
            stopMusic()

def pauseMusic():
    player.pause()

def stopMusic():
    player.stop()


app = QApplication(sys.argv)
player = QMediaPlayer()

num = random.randint(0, 3)

content = getContent(num)
player.setMedia(content)
playMusic()
