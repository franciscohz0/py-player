# -*- coding: utf-8 -*-

################################################################################
## File generated from reading UI file 'about-dialog.ui'
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
    QSize, Qt)
from PySide6.QtGui import (QFont, QPixmap)
from PySide6.QtWidgets import (QLabel, QPushButton)
import resources_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(500, 300)
        AboutDialog.setMinimumSize(QSize(500, 300))
        AboutDialog.setMaximumSize(QSize(500, 300))
        self.iconLabel = QLabel(AboutDialog)
        self.iconLabel.setObjectName(u"iconLabel")
        self.iconLabel.setGeometry(QRect(30, 40, 191, 191))
        self.iconLabel.setPixmap(QPixmap(u":/assets/icon.png"))
        self.iconLabel.setScaledContents(True)
        self.acceptButton = QPushButton(AboutDialog)
        self.acceptButton.setObjectName(u"acceptButton")
        self.acceptButton.setGeometry(QRect(400, 260, 86, 26))
        self.softwareLabel = QLabel(AboutDialog)
        self.softwareLabel.setObjectName(u"softwareLabel")
        self.softwareLabel.setGeometry(QRect(240, 20, 161, 51))
        font = QFont()
        font.setFamilies([u"Sans"])
        font.setPointSize(17)
        font.setBold(True)
        self.softwareLabel.setFont(font)
        self.softwareLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.versionLabel = QLabel(AboutDialog)
        self.versionLabel.setObjectName(u"versionLabel")
        self.versionLabel.setGeometry(QRect(250, 70, 101, 31))
        font1 = QFont()
        font1.setFamilies([u"Sans"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.versionLabel.setFont(font1)
        self.versionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.infoLabel = QLabel(AboutDialog)
        self.infoLabel.setObjectName(u"infoLabel")
        self.infoLabel.setGeometry(QRect(280, 110, 181, 111))
        font2 = QFont()
        font2.setFamilies([u"Sans"])
        font2.setPointSize(11)
        font2.setBold(False)
        self.infoLabel.setFont(font2)
        self.infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.infoLabel.setWordWrap(True)

        self.retranslateUi(AboutDialog)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"Acerca de", None))
        self.iconLabel.setText("")
        self.acceptButton.setText(QCoreApplication.translate("AboutDialog", u"Aceptar", None))
        self.softwareLabel.setText(QCoreApplication.translate("AboutDialog", u"PyPlayer", None))
        self.versionLabel.setText(QCoreApplication.translate("AboutDialog", u"v1.0", None))
        self.infoLabel.setText(QCoreApplication.translate("AboutDialog", u"Un reproductor de audio simple.", None))
    # retranslateUi
