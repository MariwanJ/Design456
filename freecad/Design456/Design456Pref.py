# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Part of the Design456 addon.

from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  Copyright (C) 2025                                                    *
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

from PySide.QtCore import QT_TRANSLATE_NOOP
from PySide import QtGui, QtCore
from draftutils.translate import translate   #for translate

#There are several preferences that must be registered somewhere
#For example simplecopy of extruded object, chamfer,..etc
#Originally I wanted to simplify everything. But there are users don't like that.
#This is a start of the preferences pages. Not finished yet. 

#TODO :  FIXME: Further preferences will be added later 

__updated__ = '2022-10-05 21:44:57'


class Design456PrefValues:
    """ Static variable for preferences
    """
    PlaneGridEnabled=True
    PlaneGridSize=5
    Simplified=False
    MouseStepSize=1.0
    BKGColor = 0xbde1eb      #12444139  #ONLY RGB no Alfa value
    pickSize=5.0
    
Design456pref_var= Design456PrefValues()

#Convert RGB color to push button color format 
def QTgetColor(c):
    r = ((c>>16)&0xFF)/255.0
    g = ((c>>8)&0xFF)/255.0
    b = ((c)&0xFF)/255.0
    result=QtGui.QColor.fromRgbF(r,g,b)
    return result

def getRGBColor(c):
    #Contains RGB only no alfa 
    r = ((c>>16)&0xFF)/255.0
    g = ((c>>8)&0xFF)/255.0
    b = ((c)&0xFF)/255.0
    return (r,g,b)

def Design456_preferences():
    return App.ParamGet("User parameter:BaseApp/Preferences/Mod/Design456")

#set  (Save values in user.cfg)
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
    try:
        Design456Init.pToWorkbench.planeShow.redraw()
    except:
        print("please switch to the workbench to see the plane")
        pass #if workbench is not loaded, this will fail
def setSimplified(enabled):
    """ If this is checked, objects gets simplified after manipulations(for ex merge, cut ..etc)

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
    Design456pref_var.MouseStepSize=_size
    

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
    
#get values from (user.cfg)
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
    c=pref.GetUnsigned("BKGColor",12444139)
    return c

def getPickSize():
    pref = Design456_preferences()
    return pref.GetUnsigned("PickSize",5) 


class Design456Preferences:
    """ Design456 preferences- Definitions and implementation of the 
        Load and save mechanism. 
        Reading carefully the code, you should be able to make your own.
        Don't forget that you should have a xxx.ui file in your Resources folder 
    """
    @classmethod
    def __init__(self):
        self.form= None
        # Dialog made by QTDesigner 
        self.form=Gui.PySideUic.loadUi(Design456Init.UI_PATH+'Design456Pref.ui')
        
    @classmethod
    def saveSettings(self):
        """ Save preferences - settings 
        """
        Design456pref_var.PlaneGridEnabled=self.form.chkEnableGrid.isChecked()
        Design456pref_var.PlaneGridSize=self.form.grdSize.value()
        Design456pref_var.Simplified=self.form.chkSimplify.isChecked()
        #Retrieve the chosen value in RGB (INT) form as a list
        RGB=self.form.btnBkgColor.property("color").getRgb()

        R=RGB[0]
        G=RGB[1]
        B=RGB[2]
        Design456pref_var.BKGColor=  0x10000 * R + 0x100 * G + B #Alfa value is ignored
        Design456pref_var.MouseStepSize=self.form.comMouseStepSize.value()
        
        #Save New values to user.cfg
        setPlaneGrid(Design456pref_var.PlaneGridEnabled)
        setPlaneGridSize(Design456pref_var.PlaneGridSize)
        setSimplified(Design456pref_var.Simplified)
        setBKGColor(Design456pref_var.BKGColor)
        setMouseStepSize(Design456pref_var.MouseStepSize)
    
    @classmethod
    def loadSettings(self):
        """ Load preferences
        """
        Design456pref_var.PlaneGridEnabled=getPlaneGrid()
        Design456pref_var.PlaneGridSize=getPlaneGridSize()
        Design456pref_var.Simplified=getSimplified()
        Design456pref_var.BKGColor=getBKGColor()
        Design456pref_var.MouseStepSize=getMouseStepSize()
        
        self.form.chkEnableGrid.setChecked(Design456pref_var.PlaneGridEnabled)
        self.form.grdSize.setValue(Design456pref_var.PlaneGridSize)
        self.form.chkSimplify.setChecked(Design456pref_var.Simplified)
        _color=QTgetColor(Design456pref_var.BKGColor)
        self.form.btnBkgColor.setProperty("color",_color) 
        self.form.comMouseStepSize.setValue(Design456pref_var.MouseStepSize)
        
Gui.addPreferencePage(Design456Preferences,QT_TRANSLATE_NOOP("Design456","Design456"))

