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
from draftutils.translate import translate   #for translate

#There are several preferences that must be registered somewhere
#For example simplecopy of extruded object, chamfer,..etc
#Originally I wanted to simplify everything. But there are users don't like that.
#This is a start of the preferences pages. Not finished yet. 
#TODO : FIXME:

__updated__ = '2022-05-05 22:19:49'

def getColor(c):
    r = ((c>>24)&0xFF)/255.0
    g = ((c>>16)&0xFF)/255.0
    b = ((c>>8)&0xFF)/255.0
    return QtGui.QColor.fromRgbF(r,g,b)

def Design456_preferences():
    return App.ParamGet("User parameter:BaseApp/Preferences/Mod/Design456")

#set 
def setPlaneGrid(enabled=True):
    pref = Design456_preferences()
    pref.SetBool("PlaneGridEnabled", enabled)

def setPlaneGridSize(_size=True):
    pref = Design456_preferences()
    pref.SetFloat("PlaneGridSize",_size)

def setSimplified(enabled=False):
    pref = Design456_preferences()
    pref.SetBool("Simplified", enabled)

def setMouseStepSize(_size=0.1):
    pref = Design456_preferences()
    pref.comMouseStepSize.SetFloat("MouseStepSize", _size)

def setBKGColor(color=0xbde1eb):
    pref = Design456_preferences()
    pref.btnBkgColor.SetUnsigned("BKGColor", color)


#get
def getPlaneGrid():
    pref = Design456_preferences()
    return pref.GetBool("PlaneGridEnabled", True)

def getPlaneGridSize():
    pref = Design456_preferences()
    return pref.GetFloat("PlaneGridSize", 5)

def getSimplified():
    pref = Design456_preferences()
    return pref.GetBool("getSimplified", False)

def getMouseStepSize(_size=0.1):
    pref = Design456_preferences()
    return pref.GetFloat("MouseStepSize", 5)

def getBKGColor():
    pref = Design456_preferences()
    c=pref.GetUnsigned("BKGColor",0xbde1eb)
    return getColor(c)



class Design456Preferences:
    def __init__(self, parent=None):
        self.form = Gui.PySideUic.loadUi(Design456Init.UI_PATH+'Design456Pref.ui')

    def saveSettings(self):
        setPlaneGrid(self.form.chkDisableGrid.isChecked())
        setPlaneGridSize(self.form.grdSize.value())
        setSimplified(self.form.chkSimplify.isChecked())
        setMouseStepSize(self.form.comMouseStepSize.value())
        setBKGColor(self.form.btnBkgColor.getColor())

    def loadSettings(self):
        self.form.chkDisableGrid.setChecked(getPlaneGrid())
        self.form.grdSize.setValue(getPlaneGridSize())
        self.form.comMouseStepSize.setValue(getMouseStepSize())

        self.form.chkSimplify.setChecked(getSimplified())
        self.form.btnBkgColor.setProperty("color",getBKGColor()) 

    def updateSelection(self, state=None):
        pass

Gui.addPreferencePage(Design456Preferences,"Design456")