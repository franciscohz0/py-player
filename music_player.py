import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from gui.about_dialog import AboutDialog
from gui.ui_mainwindow import Ui_MainWindow
from player.audio_player import AudioPlayer
from player.metadata import getMetadata, getCover
from utils.time_utils import formatTime
from utils.constants import AUDIO_EXTENSIONS
from utils.themes import dark_theme



class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.audioPlayer = AudioPlayer(volume=50)
        self.playList = []
        self.currentIndex = -1
        self.isSeeking = False

        self.connectSignals()

    def connectSignals(self):

        self.audioPlayer.player.playbackStateChanged.connect(
            self.updatePlayingStatus
        )

        self.audioPlayer.player.durationChanged.connect(
            self.onDurationChanged
        )

        self.audioPlayer.player.positionChanged.connect(
            self.onPositionChanged
        )

        self.audioPlayer.player.mediaStatusChanged.connect(
            self.onMediaStatusChanged
        )

        self.ui.actionOpenFile.triggered.connect(
            self.openFile
        )

        self.ui.actionOpenFolder.triggered.connect(
            self.openFolder
        )

        self.ui.actionQuit.triggered.connect(
            self.close
        )

        self.ui.actionPlay.triggered.connect(
            self.onPlayTriggered
        )

        self.ui.actionPrevious.triggered.connect(
            self.onPlayPreviousTriggered
        )

        self.ui.actionNext.triggered.connect(
            self.onPlayNextTriggered
        )

        self.ui.actionAbout.triggered.connect(
            self.onAboutMenuTriggered
        )

        self.ui.playButton.clicked.connect(
            self.onPlayTriggered
        )

        self.ui.previousButton.clicked.connect(
            self.onPlayPreviousTriggered
        )

        self.ui.nextButton.clicked.connect(
            self.onPlayNextTriggered
        )

        self.ui.progressSlider.sliderPressed.connect(
            self.onSliderPressed
        )

        self.ui.progressSlider.sliderReleased.connect(
            self.onSliderReleased
        )

        self.ui.volumeButton.clicked.connect(
            self.onVolumeButtonClicked
        )

        self.ui.volumeSlider.valueChanged.connect(
            self.onVolumeChanged
        )


    def loadSong(self, filePath):

        self.audioPlayer.setSong(
            filePath,
            autoplay=True
        )
        self.updateSongInfo(filePath)


    def updateSongInfo(self, filePath):

        self.updateCover(filePath)

        metaData = getMetadata(filePath)

        self.ui.titleLabel.setText(
            metaData['title']
        )

        self.ui.artistLabel.setText(
            metaData['artist']
        )

    def updateCover(self, filePath):

        imageData = getCover(filePath)

        if imageData is None:

            self.ui.coverLabel.setPixmap(
                QPixmap(":/assets/default-cover.png")
            )
            return

        pixmap = QPixmap()
        pixmap.loadFromData(imageData)

        pixmap = pixmap.scaled(
            self.ui.coverLabel.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.ui.coverLabel.setPixmap(pixmap)


    def onPlayTriggered(self):

        if self.audioPlayer.isEmpty():
            self.openFile()
            return

        self.ui.progressSlider.setEnabled(True)
        self.audioPlayer.toggle()

    def onPlayNextTriggered(self):

        if not self.playList:
            return

        self.currentIndex += 1

        if self.currentIndex >= len(self.playList):
            self.currentIndex = 0

        filePath = self.playList[self.currentIndex]
        self.loadSong(filePath)



    def onPlayPreviousTriggered(self):

        if not self.playList:
            return

        self.currentIndex -= 1

        if self.currentIndex < 0:
            self.currentIndex = len(self.playList) - 1

        filePath = self.playList[self.currentIndex]
        self.loadSong(filePath)


    def openFile(self):

        filePath, _ = QFileDialog.getOpenFileName(
            self,
            'Abrir archivo de audio',
            str(Path.home()),
            'Audio (*.mp3 *.m4a *.flac *.webm *.wav *.opus)'
        )

        if not filePath:
            return

        self.playList = [filePath]
        self.currentIndex = 0

        self.loadSong(filePath)


    def openFolder(self):

        folderPath = QFileDialog.getExistingDirectory(
            self,
            'Abrir carpeta de audio'
        )

        if not folderPath:
            return

        self.playList = [
            str(file)
            for file in Path(folderPath).iterdir()
            if file.suffix.lower() in AUDIO_EXTENSIONS
        ]

        if not self.playList:
            return

        self.playList.sort()

        self.currentIndex = 0

        self.loadSong(
            self.playList[self.currentIndex]
        )



    def onDurationChanged(self, duration):

        self.ui.progressSlider.setRange(
            0,
            duration
        )
        self.ui.progressSlider.setEnabled(True)

        self.ui.durationLabel.setText(
            formatTime(duration)
        )


    def onPositionChanged(self, position):

        if not self.isSeeking:
            self.ui.progressSlider.setValue(
                position
            )

        self.ui.progressLabel.setText(
            formatTime(position)
        )

    def onVolumeChanged(self, volume):

        if self.audioPlayer.output.isMuted():

            self.audioPlayer.output.setMuted(
                False
            )

        self.audioPlayer.setVolume(volume)
        self.updateVolumeButton()

        self.ui.volumeLabel.setText(
            f'{volume}%'
        )


    def onSliderPressed(self):
        self.isSeeking = True

    def onSliderReleased(self):

        self.isSeeking = False
        self.audioPlayer.setPosition(
            self.ui.progressSlider.value()
        )

    def onMediaStatusChanged(self, status):

        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return

        if self.currentIndex < len(self.playList) - 1:
            self.onPlayNextTriggered()
        else:
            self.audioPlayer.stop()

    def onVolumeButtonClicked(self):

        muted = self.audioPlayer.output.isMuted()

        self.audioPlayer.output.setMuted(
            not muted
        )

        self.updateVolumeButton()

    def updateVolumeButton(self):

        if self.audioPlayer.output.isMuted():
            self.ui.volumeButton.setIcon(
                QIcon(':/assets/mute.svg')
            )

        else:
            self.ui.volumeButton.setIcon(
                QIcon(':/assets/volume.svg')
            )

    def updatePlayingStatus(self, state):

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.ui.playButton.setIcon(
                QIcon(':/assets/player-pause.svg')
            )
            self.ui.actionPlay.setIcon(
                QIcon(':/assets/player-pause.svg')
            )
            self.ui.actionPlay.setText('Pausar')

        else:
            self.ui.playButton.setIcon(
                QIcon(':/assets/player-play.svg')
            )
            self.ui.actionPlay.setIcon(
                QIcon(':/assets/player-play.svg')
            )
            self.ui.actionPlay.setText('Reproducir')

    def onAboutMenuTriggered(self):

        dialog = AboutDialog(self)
        dialog.exec()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/assets/icon.png'))
    dark_theme(app)

    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())
