# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import os
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtWidgets import QGraphicsScene


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1019, 501)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.db450Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db450Label.setFont(font)
        self.db450Label.setObjectName("db450Label")
        self.gridLayout_6.addWidget(self.db450Label, 8, 0, 1, 1)
        self.db500Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db500Label.setFont(font)
        self.db500Label.setObjectName("db500Label")
        self.gridLayout_6.addWidget(self.db500Label, 9, 0, 1, 1)
        self.maxDBLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.maxDBLabel.setFont(font)
        self.maxDBLabel.setObjectName("maxDBLabel")
        self.gridLayout_6.addWidget(self.maxDBLabel, 1, 0, 1, 1)
        self.graphValuesLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.graphValuesLabel.setFont(font)
        self.graphValuesLabel.setObjectName("graphValuesLabel")
        self.gridLayout_6.addWidget(self.graphValuesLabel, 0, 0, 1, 1)
        self.specificLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.specificLabel.setFont(font)
        self.specificLabel.setObjectName("specificLabel")
        self.gridLayout_6.addWidget(self.specificLabel, 6, 0, 1, 1)
        self.db600Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db600Label.setFont(font)
        self.db600Label.setObjectName("db600Label")
        self.gridLayout_6.addWidget(self.db600Label, 12, 0, 1, 1)
        self.maxNMLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.maxNMLabel.setFont(font)
        self.maxNMLabel.setObjectName("maxNMLabel")
        self.gridLayout_6.addWidget(self.maxNMLabel, 2, 0, 1, 1)
        self.minDBLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.minDBLabel.setFont(font)
        self.minDBLabel.setObjectName("minDBLabel")
        self.gridLayout_6.addWidget(self.minDBLabel, 3, 0, 1, 1)
        self.db550Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db550Label.setFont(font)
        self.db550Label.setObjectName("db550Label")
        self.gridLayout_6.addWidget(self.db550Label, 10, 0, 1, 1)
        self.db570Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db570Label.setFont(font)
        self.db570Label.setObjectName("db570Label")
        self.gridLayout_6.addWidget(self.db570Label, 11, 0, 1, 1)
        self.db435Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db435Label.setFont(font)
        self.db435Label.setObjectName("db435Label")
        self.gridLayout_6.addWidget(self.db435Label, 7, 0, 1, 1)
        self.db650Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.db650Label.setFont(font)
        self.db650Label.setObjectName("db650Label")
        self.gridLayout_6.addWidget(self.db650Label, 13, 0, 1, 1)
        self.minNMLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.minNMLabel.setFont(font)
        self.minNMLabel.setObjectName("minNMLabel")
        self.gridLayout_6.addWidget(self.minNMLabel, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 5, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_6, 0, 0, 2, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horaLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horaLabel.sizePolicy().hasHeightForWidth())
        self.horaLabel.setSizePolicy(sizePolicy)
        self.horaLabel.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.horaLabel.setFont(font)
        self.horaLabel.setObjectName("horaLabel")
        self.gridLayout_3.addWidget(self.horaLabel, 0, 1, 1, 1)
        self.graphWidget = pg.PlotWidget(self.centralwidget)
        self.graphWidget.setXRange(350, 750, padding=0)
        self.graphWidget.setAutoFillBackground(True)
        self.graphWidget.setBackgroundBrush(QtCore.Qt.white)
        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.graphWidget.setForegroundBrush(brush)
        self.graphWidget.setGeometry(QtCore.QRect(200, 110, 641, 291))
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setBackground("k" if "dark" == "dark" else "w")
        self.gridLayout_3.addWidget(self.graphWidget, 2, 0, 1, 1)
        self.messageBox = QtWidgets.QLabel(self.centralwidget)
        self.messageBox.setMinimumSize(QtCore.QSize(0, 35))
        self.messageBox.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.messageBox.setAlignment(QtCore.Qt.AlignCenter)
        self.messageBox.setObjectName("messageBox")
        self.gridLayout_3.addWidget(self.messageBox, 1, 0, 1, 1)
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.titleLabel.setFont(font)
        self.titleLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout_3.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pictureIndicasat = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pictureIndicasat.sizePolicy().hasHeightForWidth())
        self.pictureIndicasat.setSizePolicy(sizePolicy)
        self.pictureIndicasat.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pictureIndicasat.setObjectName("pictureIndicasat")
        script_dir = os.path.dirname(__file__)
        indicasat_path = os.path.join(script_dir, 'img/indicasat.jpg')
        pixmap = QPixmap(indicasat_path)
        if pixmap.isNull():
            print("Failed to load image")
        else:
            # Create a QGraphicsPixmapItem with the QPixmap
            pixmap_item = QGraphicsPixmapItem(pixmap)

            # Create a QGraphicsScene and add the QGraphicsPixmapItem to it
            scene = QGraphicsScene()
            scene.addItem(pixmap_item)

            # Set the QGraphicsScene as the scene for the QGraphicsView
            self.pictureIndicasat.setScene(scene)
        self.verticalLayout_2.addWidget(self.pictureIndicasat)
        self.pictureFie = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pictureFie.sizePolicy().hasHeightForWidth())
        self.pictureFie.setSizePolicy(sizePolicy)
        self.pictureFie.setMaximumSize(QtCore.QSize(150, 200))
        self.pictureFie.setObjectName("pictureFie")
        script_dir = os.path.dirname(__file__)
        fie_path = os.path.join(script_dir, 'img/fie.jpg')
        pixmap = QPixmap(fie_path)
        if pixmap.isNull():
            print("Failed to load image")
        else:
            # Create a QGraphicsPixmapItem with the QPixmap
            pixmap_item = QGraphicsPixmapItem(pixmap)

            # Create a QGraphicsScene and add the QGraphicsPixmapItem to it
            scene = QGraphicsScene()
            scene.addItem(pixmap_item)

            # Set the QGraphicsScene as the scene for the QGraphicsView
            self.pictureFie.setScene(scene)
        self.verticalLayout_2.addWidget(self.pictureFie)
        self.pictureUtp = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pictureUtp.sizePolicy().hasHeightForWidth())
        self.pictureUtp.setSizePolicy(sizePolicy)
        self.pictureUtp.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.pictureUtp.setFont(font)
        self.pictureUtp.setObjectName("pictureUtp")
        script_dir = os.path.dirname(__file__)
        utp_path = os.path.join(script_dir, 'img/utp.jpg')
        pixmap = QPixmap(utp_path)
        if pixmap.isNull():
            print("Failed to load image")
        else:
            # Create a QGraphicsPixmapItem with the QPixmap
            pixmap_item = QGraphicsPixmapItem(pixmap)

            # Create a QGraphicsScene and add the QGraphicsPixmapItem to it
            scene = QGraphicsScene()
            scene.addItem(pixmap_item)

            # Set the QGraphicsScene as the scene for the QGraphicsView
            self.pictureUtp.setScene(scene)
        self.verticalLayout_2.addWidget(self.pictureUtp)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 2, 1, 1, 1)
        self.btnWavelength = QtWidgets.QPushButton(self.centralwidget)
        self.btnWavelength.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.btnWavelength.setFont(font)
        self.btnWavelength.setObjectName("btnWavelength")
        self.btnWavelength.setStyleSheet("color: lime;")
        self.gridLayout_3.addWidget(self.btnWavelength, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 1, 2, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_7.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_7.setHorizontalSpacing(20)
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.btnSettings = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnSettings.setFont(font)
        self.btnSettings.setObjectName("btnSettings")
        self.gridLayout_7.addWidget(self.btnSettings, 0, 5, 1, 1)
        self.btnContinuous = QtWidgets.QPushButton(self.centralwidget)
        self.btnContinuous.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnContinuous.setFont(font)
        self.btnContinuous.setObjectName("btnContinuous")
        self.gridLayout_7.addWidget(self.btnContinuous, 0, 3, 1, 1)
        self.btnSaveData = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveData.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnSaveData.setFont(font)
        self.btnSaveData.setObjectName("btnSaveData")
        self.gridLayout_7.addWidget(self.btnSaveData, 0, 4, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMaximumSize(QtCore.QSize(200, 200))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_7.addWidget(self.progressBar, 0, 6, 1, 1)
        self.btnSingle = QtWidgets.QPushButton(self.centralwidget)
        self.btnSingle.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnSingle.setFont(font)
        self.btnSingle.setObjectName("btnSingle")
        self.gridLayout_7.addWidget(self.btnSingle, 0, 2, 1, 1)
        self.btnBaseline = QtWidgets.QPushButton(self.centralwidget)
        self.btnBaseline.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnBaseline.setFont(font)
        self.btnBaseline.setObjectName("btnBaseline")
        self.gridLayout_7.addWidget(self.btnBaseline, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_7, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1019, 22))
        self.menubar.setObjectName("menubar")
        self.menuMain = QtWidgets.QMenu(self.menubar)
        self.menuMain.setObjectName("menuMain")
        self.menuData = QtWidgets.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")
        self.spanData = QtWidgets.QMenu(self.menubar)
        self.spanData.setObjectName("spanData")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMain.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.spanData.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Espectrophotometer UTP-CG-001"))
        self.db450Label.setText(_translate("MainWindow", "450nm: 0.00"))
        self.db500Label.setText(_translate("MainWindow", "500nm: 0.00"))
        self.maxDBLabel.setText(_translate("MainWindow", "Máx dB: 0.00"))
        self.graphValuesLabel.setText(_translate("MainWindow", "Graph Values"))
        self.specificLabel.setText(_translate("MainWindow", "Key Values (dB):"))
        self.db600Label.setText(_translate("MainWindow", "600nm: 0.00"))
        self.maxNMLabel.setText(_translate("MainWindow", "Máx nm: 0.00"))
        self.minDBLabel.setText(_translate("MainWindow", "Min dB: 0.00"))
        self.db550Label.setText(_translate("MainWindow", "550nm: 0.00"))
        self.db570Label.setText(_translate("MainWindow", "570nm: 0.00"))
        self.db435Label.setText(_translate("MainWindow", "435nm: 0.00"))
        self.db650Label.setText(_translate("MainWindow", "650nm: 0.00"))
        self.minNMLabel.setText(_translate("MainWindow", "Min nm: 0.00")) 
        self.horaLabel.setText(_translate("MainWindow", "2023-11-06 14:52"))
        self.messageBox.setText(_translate("MainWindow", "Please calibrate the spectrophotometer before taking a measurement."))
        self.titleLabel.setText(_translate("MainWindow", "Universidad Técnológica de Panamá - Espectofotómetro - Muestras Covid-19 "))
        self.btnWavelength.setText(_translate("MainWindow", "Wavelength"))
        self.btnSettings.setText(_translate("MainWindow", "Settings"))
        self.btnContinuous.setText(_translate("MainWindow", "Continuous"))
        self.btnSaveData.setText(_translate("MainWindow", "Save Data"))
        self.btnSingle.setText(_translate("MainWindow", "Single"))
        self.btnBaseline.setText(_translate("MainWindow", "Baseline"))
        self.menuMain.setTitle(_translate("MainWindow", "Main Window"))
        self.menuData.setTitle(_translate("MainWindow", "Measured Data"))
        self.spanData.setTitle(_translate("MainWindow", "Span Data"))
