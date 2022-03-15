# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# *                                                                        *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from pivy import coin
import FACE_D as faced
from PySide import QtGui, QtCore
from PySide.QtCore import QT_TRANSLATE_NOOP
from draftobjects.base import DraftObject
from draftutils.translate import translate  # for translation
import Design456_Part
__updated__ = '2022-03-15 21:56:51'

class PrimitivePartsIconList:
    def __init__(self):
        self.frmBasicShapes=None
        parts=Design456_Part.Design456_Part()
        
    def Activated(self):
        self.setupUi()
        self.frmBasicShapes.show()
        
    def dock_right_RH(self):
        RHmw = Gui.getMainWindow()
        RHmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.frmBasicShapes)

    def HideIconList(self):
        pass
    
    
    def addListItem(self, text):
        item = QtGui.QListWidgetItem(text)
        self.list.addItem(item)
        widget = QtGui.QWidget(self.list)
        button = QtGui.QToolButton(widget)
        layout = QtGui.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(button)
        self.list.setItemWidget(item, widget)
        button.clicked[()].connect(
            lambda: self.handleButtonClicked(item))

    def handleButtonClicked(self, item):
        print(item.text())
        
    def setupUi(self):
        self.frmBasicShapes=QtGui.QDockWidget()
        self.frmBasicShapes.setObjectName("frmBasicShapes")
        self.frmBasicShapes.resize(260, 534)
        #self.frmBasicShapes.setWindowIcon(icon)
        self.frmBasicShapes.setToolTip("Basic Shapes")
        self.frmBasicShapes.setWindowTitle("Basic Shapes")
        self.frmBasicShapes.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.frmBasicShapes.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.btnHide = QtGui.QPushButton(self.frmBasicShapes)
        self.btnHide.setGeometry(QtCore.QRect(0, 290, 30, 110))
        self.btnHide.clicked.connect(self.HideIconList)
        icon = QtGui.QIcon()
        icon.addFile(Design456Init.IMAGE_PATH + '/Toolbars/1.png', QtCore.QSize(64, 64))
        self.btnHide.setIcon(icon)
        
        self.scrollArea = QtGui.QScrollArea(self.frmBasicShapes)
        self.scrollArea.setGeometry(QtCore.QRect(20,50, 280, 500))
        self.scrollArea.setVisible(True)
        self.scrollArea.setFrameShape(QtGui.QFrame.Box)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setEnabled(True)

        #Container Widget
        self.btnWDG = QtGui.QWidget()
        self.btnWDG.setGeometry(QtCore.QRect(0, 40, 260, 600))
        self.btnWDG.setObjectName("btnWDG")
        self.scrollArea.setWidget(self.btnWDG)

        #Oscar Home Horizontal Layout - QHBoxLayout#
        self.gridLayout = QtGui.QGridLayout(self.btnWDG)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(6)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(Design456Init.IMAGE_PATH + "/Toolbars/Part_Box.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btn1 = QtGui.QPushButton()
        btn1.setIcon(icon)
        
        for  i in range(0,10):
            for j in range(0,3):
                pbtn = QtGui.QPushButton()
                pbtn.setIcon(icon)
                pbtn.setMinimumSize(64,64)
                #pbtn.setIconSize( QtCore.QSize(pbtn.width()-2,pbtn.height()-2) )
                pbtn.setIconSize( QtCore.QSize(48,48) )
                pbtn.setGeometry(QtCore.QRect(0, 0, 68, 68))
                self.gridLayout.addWidget(pbtn,i,j)
                

        # self.frmBasicShapes.setFeatures(
        #    QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        QtCore.QMetaObject.connectSlotsByName(self.frmBasicShapes)
        return self.frmBasicShapes

f=PrimitivePartsIconList()
f.Activated()
f.dock_right_RH()