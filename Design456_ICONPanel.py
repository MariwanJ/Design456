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
import Design456_Part as p
import PyramidMo.polyhedrons as dd
__updated__ = '2022-03-17 22:23:52'

COMMANDS=[
    ["Design456_Part_Box",Design456Init.ICON_PATH + 'Part_Box.svg'],
    ["Design456_Part_Cylinder",Design456Init.ICON_PATH + 'Part_Cylinder.svg'],
    ["Design456_Part_Tube",Design456Init.ICON_PATH + 'Part_Tube.svg' ],
    ["Design456_Part_Sphere",Design456Init.ICON_PATH + 'Part_Sphere.svg'],
    ["Design456_Part_Cone",Design456Init.ICON_PATH + 'Part_Cone.svg'],
    ["Design456_Part_Torus", Design456Init.ICON_PATH + 'Part_Torus.svg'],
    ["Design456_Part_Wedge",Design456Init.ICON_PATH + 'Part_Wedge.svg'],
    ["Design456_Part_Prism", Design456Init.ICON_PATH + 'Part_Prism.svg'],
    ["Design456_Part_Pyramid",Design456Init.ICON_PATH + 'Part_Pyramid.svg'],
    ["Pyramid", Design456Init.PYRAMID_ICON_PATH + 'pyramid.svg'],
    ["Tetrahedron",Design456Init.PYRAMID_ICON_PATH + 'tetrahedron.svg'],
    ["Octahedron",Design456Init.PYRAMID_ICON_PATH + 'octahedron.svg'],
    ["Dodecahedron", Design456Init.PYRAMID_ICON_PATH+'dodecahedron.svg'],
    ["Icosahedron", Design456Init.PYRAMID_ICON_PATH+'icosahedron.svg'],
    ["Icosahedron_truncated",  Design456Init.PYRAMID_ICON_PATH+ 'icosahedron_trunc.svg'],    
    ["Geodesic_sphere",  Design456Init.PYRAMID_ICON_PATH+'geodesic_sphere.svg']
    ]

class PrimitivePartsIconList:
    def __init__(self):
        self.frmBasicShapes=None
        self.btn=[]
        self.hidden = False    
        
    def Activated(self):
        self.setupUi()
        self.frmBasicShapes.show()
        
    def dock_right_RH(self):
        RHmw = Gui.getMainWindow()
        RHmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.frmBasicShapes)
  
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

    def HideIconList(self):
        print("clicked")
        if self.hidden == True:
            self.hidden = False
            icon = QtGui.QIcon()
            icon.addFile(Design456Init.IMAGE_PATH + '/Toolbars/1.png', QtCore.QSize(64, 64))
            self.btnHide.setIcon(icon)
            self.frmBasicShapes.resize(260, 534)
        else:
            self.hidden=True
            icon = QtGui.QIcon()
            icon.addFile(Design456Init.IMAGE_PATH + '/Toolbars/2.png', QtCore.QSize(64, 64))
            self.btnHide.setIcon(icon)
            self.frmBasicShapes.resize(30,534)

    def runCommands(self,index):
        Gui.runCommand(COMMANDS[index][0],0)
        
    def setupUi(self):
        from functools import partial
        self.frmBasicShapes=QtGui.QDockWidget()
        self.frmBasicShapes.setObjectName("frmBasicShapes")
        #self.frmBasicShapes.resize(260, 534)
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
        
        j=0 
        self.btn.clear()    
        for items in range(0,len(COMMANDS)):
            i=int(items/3)
            index=i*3+j
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(COMMANDS[index][1]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.btn.append(QtGui.QPushButton())
            self.btn[index].setIcon(icon)
            self.btn[index].setMinimumSize(64,64)
            self.btn[index].setIconSize( QtCore.QSize(48,48) )
            self.btn[index].setGeometry(QtCore.QRect(0, 0, 68, 68))   
            self.btn[index].setObjectName(str(index))
            self.btn[index].setToolTip(COMMANDS[index][0]   )         
            self.gridLayout.addWidget(self.btn[index],i,j)
            self.btn[index].clicked.connect(partial(self.runCommands,index))
            j+=1
            if j==3:
                j=0   
        
        # self.frmBasicShapes.setFeatures(
        #    QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        QtCore.QMetaObject.connectSlotsByName(self.frmBasicShapes)
        return self.frmBasicShapes

f=PrimitivePartsIconList()
f.Activated()
f.dock_right_RH()