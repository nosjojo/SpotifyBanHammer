# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SpotifyBanHammer(object):
    def setupUi(self, SpotifyBanHammer):
        SpotifyBanHammer.setObjectName("SpotifyBanHammer")
        SpotifyBanHammer.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SpotifyBanHammer)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.start_hotkeys_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_hotkeys_btn.setCheckable(True)
        self.start_hotkeys_btn.setChecked(False)
        self.start_hotkeys_btn.setObjectName("start_hotkeys_btn")
        self.verticalLayout.addWidget(self.start_hotkeys_btn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        SpotifyBanHammer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SpotifyBanHammer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        SpotifyBanHammer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SpotifyBanHammer)
        self.statusbar.setObjectName("statusbar")
        SpotifyBanHammer.setStatusBar(self.statusbar)

        self.retranslateUi(SpotifyBanHammer)
        QtCore.QMetaObject.connectSlotsByName(SpotifyBanHammer)

    def retranslateUi(self, SpotifyBanHammer):
        _translate = QtCore.QCoreApplication.translate
        SpotifyBanHammer.setWindowTitle(_translate("SpotifyBanHammer", "Spotify Ban Hammer"))
        self.pushButton_2.setText(_translate("SpotifyBanHammer", "Ban Artist"))
        self.pushButton.setText(_translate("SpotifyBanHammer", "Sanitize Playlist"))
        self.start_hotkeys_btn.setText(_translate("SpotifyBanHammer", "Start Hotkeys"))

