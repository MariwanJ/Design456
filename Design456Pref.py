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
from ThreeDWidgets.constant import FR_COLOR
#There are several preferences that must be registered somewhere
#For example simplecopy of extruded object, chamfer,..etc
#Originally I wanted to simplify everything. But there are users don't like that.
#This is a start of the preferences pages. Not finished yet. 
#TODO : FIXME:

__updated__ = '2022-05-06 20:57:04'


class Design456PrefValues:
    """ Static variable for preferences
    """
    MouseStepSize=1.0
    PlaneGridDisabled=True
    Simplified=False
    PlaneGridSize=5
    BKGColor = int(65536*FR_COLOR.FR_SPECIAL_BLUE[0]+ 256*FR_COLOR.FR_SPECIAL_BLUE[1]+FR_COLOR.FR_SPECIAL_BLUE[2])
    
    
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
    pref.SetBool("PlaneGridDisabled", enabled)

def setPlaneGridSize(_size):
    pref = Design456_preferences()
    pref.SetInt("PlaneGridSize",_size)

def setSimplified(enabled):
    pref = Design456_preferences()
    pref.SetBool("Simplified", enabled)

def setMouseStepSize(_size):
    pref = Design456_preferences()
    pref.SetFloat("MouseStepSize", _size)

def setBKGColor(color=0xbde1eb):
    pref = Design456_preferences()
    pref.SetUnsigned("BKGColor", color)

#get
def getPlaneGrid():
    pref = Design456_preferences()
    return pref.GetBool("PlaneGridDisabled", True)

def getPlaneGridSize():
    pref = Design456_preferences()
    return pref.GetFloat("PlaneGridSize", 5.0)

def getSimplified():
    pref = Design456_preferences()
    return pref.GetBool("getSimplified", False)

def getMouseStepSize(_size=0.1):
    pref = Design456_preferences()
    return pref.GetFloat("MouseStepSize", 5.0)

def getBKGColor():
    pref = Design456_preferences()
    c=pref.GetUnsigned("BKGColor",0xbde1eb)
    return getColor(c)

class Design456Preferences:
    def __init__(self, parent=None):
        self.form = Gui.PySideUic.loadUi(Design456Init.UI_PATH+'Design456Pref.ui')

    def saveSettings(self):
        Design456Init.Design456pref.PlaneGridDisabled=self.form.chkDisableGrid.isChecked()
        Design456Init.Design456pref.PlaneGridSize=self.form.grdSize.value()
        Design456Init.Design456pref.Simplified=self.form.chkSimplify.isChecked()
        RGB=self.form.btnBkgColor.palette().button().color()
        Design456Init.Design456pref.BKGColor=65536*RGB.red()+256*RGB.green()+RGB.blue()
        Design456Init.Design456pref.MouseStepSize=self.form.comMouseStepSize.value()

        setPlaneGrid(Design456Init.Design456pref.PlaneGridDisabled)
        setPlaneGridSize(Design456Init.Design456pref.PlaneGridSize)
        setSimplified(Design456Init.Design456pref.Simplified)
        setBKGColor(Design456Init.Design456pref.BKGColor)
        setMouseStepSize(Design456Init.Design456pref.MouseStepSize)

    def loadSettings(self):
        Design456Init.Design456pref.PlaneGridDisabled=getPlaneGrid()
        Design456Init.Design456pref.PlaneGridSize=getPlaneGridSize()
        Design456Init.Design456pref.Simplified=getSimplified()
        Design456Init.Design456pref.BKGColor=getBKGColor()
        Design456Init.Design456pref.MouseStepSize=getMouseStepSize()
        
        self.form.chkDisableGrid.setChecked(Design456Init.Design456pref.PlaneGridDisabled)
        self.form.grdSize.setValue(Design456Init.Design456pref.PlaneGridSize)
        self.form.chkSimplify.setChecked(Design456Init.Design456pref.Simplified)
        self.form.btnBkgColor.setProperty("color",Design456Init.Design456pref.BKGColor) 
        self.form.comMouseStepSize.setValue(Design456Init.Design456pref.MouseStepSize)
        
Gui.addPreferencePage(Design456Preferences,"Design456")