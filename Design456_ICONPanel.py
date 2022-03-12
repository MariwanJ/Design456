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

__updated__ = '2022-03-12 21:58:09'

class PrimitivePartsIconList:
    def __init__(self):
        pass
    def Activated(self):
        pass
    
    def dock_right_RH(self):
        
        MyListWidget = QtGui.QDockWidget()
        MyListWidget.setFeatures(
            QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        RHmw = Gui.getMainWindow()
        RHmw.addDockWidget(QtCore.Qt.RightDockWidgetArea, RHDockWidget)
        MyListWidget.setFloating(True)  # undock
        mw = Gui.getMainWindow()
        dw = mw.findChildren(QtGui.QDockWidget)
        idw = 0
        cv = None
        if len(dw)>0:
            while  idw < len(dw):
                d = dw[idw]
                idw += 1
                area = mw.dockWidgetArea(d)
                if area == QtCore.Qt.RightDockWidgetArea:
                    r_w = str(d.objectName()) 
                    cv = mw.findChild(QtGui.QDockWidget, r_w)
                    break
        mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, MyListWidget)
        MyListWidget.activateWindow()
        MyListWidget.raise_()
        if MyListWidget and cv is not None:
            dw = mw.findChildren(QtGui.QDockWidget)
            try:
                mw.tabifyDockWidget(cv, MyListWidget)
            except:
                pass

    def setupUi(self):
        self.frmBasicShapes=QtGui.QDockWidget()
        self.frmBasicShapes.setObjectName("frmBasicShapes")
        self.frmBasicShapes.resize(260, 534)
        self.frmBasicShapes.setWindowIcon(icon)
        self.frmBasicShapes.setToolTip("Basic Shapes")
        self.frmBasicShapes.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frmBasicShapes.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.frmBasicShapes.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.frmBasicShapes.setWindowTitle("Basic Shapes")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        layout = QtGui.QGridLayout()
        btn =  QtGui.QPushButton()
        btn.setIcon(Design456Init.ICON_PATH + 'RoundRoof.svg')
        layout.addWidget(btn)
        count += 1

        DockWidget.setWidget(self.dockWidgetContents)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    DockWidget = QtGui.QDockWidget()
    ui = PrimitivePartsIconList()
    ui.setupUi(DockWidget)
    ui.dock_right_RH() # Dock the widget to the left
    DockWidget.show()
    sys.exit(app.exec_())

