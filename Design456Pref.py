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

__updated__ = '2022-05-07 16:52:21'

class Design456PrefValues:
    """ Static variable for preferences
    """
    PlaneGridEnabled=True
    PlaneGridSize=5
    Simplified=False
    MouseStepSize=1.0
    BKGColor = int(65536*FR_COLOR.FR_SPECIAL_BLUE[0]+ 256*FR_COLOR.FR_SPECIAL_BLUE[1]+FR_COLOR.FR_SPECIAL_BLUE[2])
    pickSize=5.0
    
Design456pref_var= Design456PrefValues()




    #Convert RGB color to push button color format 
def getColor(c):
    r = ((c>>24)&0xFF)/255.0
    g = ((c>>16)&0xFF)/255.0
    b = ((c>>8)&0xFF)/255.0
    return QtGui.QColor.fromRgbF(r,g,b)

def Design456_preferences():
    return App.ParamGet("User parameter:BaseApp/Preferences/Mod/Design456")

#set 
def setPlaneGrid(enabled):
    """ Show or hide the Grid drawn for xyz plane

    Args:
        enabled (bool): show or hide grid on the xyz plane.
    """
    pref = Design456_preferences()
    pref.SetBool("PlaneGridEnabled", enabled)

def setPlaneGridSize(_size):
    """Size of the XY-Plane 
    
    Args:
        _size (Integer): Customize the size of the drawing grid for xy plane.
    """
    pref = Design456_preferences()
    pref.SetInt("PlaneGridSize",_size)

def setSimplified(enabled):
    """ If this is checked, objects gets simplified after manupulations(for ex merge, cut ..etc)

    Args:
        enabled (Boolean): if checked, the objects will be simplified
    """
    pref = Design456_preferences()
    pref.SetBool("Simplified", enabled)

def setMouseStepSize(_size):
    """ Mouse movement step size. Used in Part mover, Paint and all other tools 

    Args:
        _size (Float): Mouse to mm step size. 
    """
    pref = Design456_preferences()
    pref.SetFloat("MouseStepSize", _size)

def setBKGColor(_color):
    """Line color - XY Plane grid drawing 

    Args:
        _color (unsigned int): color represent RGB line color in unsigned int
    """
    pref = Design456_preferences()
    pref.SetUnsigned("BKGColor", _color)

def setPickSize(_size):
    """COIN 3D Picksize 

    Args:
        _size (Float): picking radius Size- COIN3D 
    """
    pref = Design456_preferences()
    pref.SetUnsigned("PickSize", _size)
    
#get
def getPlaneGrid():
    pref = Design456_preferences()
    return pref.GetBool("PlaneGridEnabled", True)

def getPlaneGridSize():
    pref = Design456_preferences()
    return pref.GetInt("PlaneGridSize", 5)

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

def getPickSize():
    pref = Design456_preferences()
    return pref.GetUnsigned("PickSize",5) 


class Design456Preferences:
    
    def __init__(self):
        self.form= None
    
    @classmethod
    def saveSettings(self):
        print("SAVE Setting")
        self.form=Gui.PySideUic.loadUi(Design456Init.UI_PATH+'Design456Pref.ui')

        Design456pref_var.PlaneGridEnabled=Design456Preferences.form.chkEnableGrid.isChecked()
        Design456pref_var.PlaneGridSize=Design456Preferences.form.grdSize.value()
        Design456pref_var.Simplified=Design456Preferences.form.chkSimplify.isChecked()
        RGB=Design456Preferences.form.btnBkgColor.palette().button().color()
        Design456pref_var.BKGColor=65536*RGB.red()+256*RGB.green()+RGB.blue()
        Design456pref_var.MouseStepSize=Design456Preferences.form.comMouseStepSize.value()

        setPlaneGrid(Design456pref_var.PlaneGridEnabled)
        setPlaneGridSize(Design456pref_var.PlaneGridSize)
        setSimplified(Design456pref_var.Simplified)
        setBKGColor(Design456pref_var.BKGColor)
        setMouseStepSize(Design456pref_var.MouseStepSize)
    
    @classmethod
    def loadSettings(self):
        self.form=Gui.PySideUic.loadUi(Design456Init.UI_PATH+'Design456Pref.ui')
        print("load Setting")

        Design456pref_var.PlaneGridEnabled=getPlaneGrid()
        Design456pref_var.PlaneGridSize=getPlaneGridSize()
        Design456pref_var.Simplified=getSimplified()
        Design456pref_var.BKGColor=getBKGColor()
        Design456pref_var.MouseStepSize=getMouseStepSize()
        
        Design456Preferences.form.chkEnableGrid.setChecked(Design456pref_var.PlaneGridEnabled)
        Design456Preferences.form.grdSize.setValue(Design456pref_var.PlaneGridSize)
        Design456Preferences.form.chkSimplify.setChecked(Design456pref_var.Simplified)
        Design456Preferences.form.btnBkgColor.setProperty("color",Design456pref_var.BKGColor) 
        Design456Preferences.form.comMouseStepSize.setValue(Design456pref_var.MouseStepSize)
        
Gui.addPreferencePage(Design456Preferences,QT_TRANSLATE_NOOP("Design456","Design456"))

