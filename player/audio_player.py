from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput
)

class AudioPlayer:
    def __init__(self, volume=0):
        self.output = QAudioOutput()

        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.output)

        self.setVolume(volume)


    def setSong(self, path, autoplay=False):

        self.player.setSource(
            QUrl.fromLocalFile(path)
        )

        if autoplay:
            self.play()

    def isPlaying(self):
        return (
            self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
        )

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def toggle(self):
        if self.isPlaying():
            self.pause()

        else:
            self.play()

    def setVolume(self, volume):
        self.output.setVolume(volume / 100)

    def stop(self):
        self.player.stop()

    def setPosition(self, position):
        self.player.setPosition(position)

    def isEmpty(self):
        return self.player.source().isEmpty()   