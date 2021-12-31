# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a apart of the Open Source Design456 Workbench - FreeCAD. *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore

#There are several preferences that must be registered somewhere
#For example simplecopy of extruded object, chamfer,..etc
#Originally I wanted to simplify everything. But there are users don't like that.
#This is a start of the preferences pages. Not finished yet. 
#TODO : FIXME:

__updated__ = ''

class Ui_Design456Preferences(object):
    def setupUi(self, Design456Preferences):
        Design456Preferences.setObjectName("Design456Preferences")
        Design456Preferences.resize(800, 600)
        self.tabConfig = QtGui.QTabWidget(Design456Preferences)
        self.tabConfig.setGeometry(QtCore.QRect(110, 0, 691, 581))
        self.tabConfig.setObjectName("tabConfig")
        self.tabfirst = QtGui.QWidget()
        self.tabfirst.setObjectName("tabfirst")
        self.grpSimplify = QtGui.QGroupBox(self.tabfirst)
        self.grpSimplify.setGeometry(QtCore.QRect(10, 10, 671, 61))
        self.grpSimplify.setObjectName("grpSimplify")
        self.chkSimplify = QtGui.QCheckBox(self.grpSimplify)
        self.chkSimplify.setGeometry(QtCore.QRect(10, 20, 171, 20))
        self.chkSimplify.setObjectName("chkSimplify")
        self.tabConfig.addTab(self.tabfirst, "")
        self.tabsecond = QtGui.QWidget()
        self.tabsecond.setObjectName("tabsecond")
        self.tabConfig.addTab(self.tabsecond, "")
        self.listWidget = QtGui.QListWidget(Design456Preferences)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 111, 581))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(Design456Preferences)
        self.tabConfig.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Design456Preferences)

    def retranslateUi(self, Design456Preferences):
        _translate = QtCore.QCoreApplication.translate
        Design456Preferences.setWindowTitle(_translate("Design456Preferences", "Design456Preferences"))
        self.grpSimplify.setTitle(_translate("Design456Preferences", "Object Creation in Design456"))
        self.chkSimplify.setText(_translate("Design456Preferences", "Simplify created objects"))
        self.tabConfig.setTabText(self.tabConfig.indexOf(self.tabfirst), _translate("Design456Preferences", "General"))
        self.tabConfig.setTabText(self.tabConfig.indexOf(self.tabsecond), _translate("Design456Preferences", "Tab 2"))



from PySide import QtGui

class Design456Prefrences:
    def __init__(self):
        self.form = QtGui.QCalendarWidget()
        self.form.setWindowTitle("Design456 Preferences")
    def saveSettings(self):
        pass
    def loadSettings(self):
        pass

Gui.addPreferencePage(Design456Prefrences, "Design456Workbench
                      ")