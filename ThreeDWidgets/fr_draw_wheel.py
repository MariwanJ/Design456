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

import os
import sys
from types import coroutine
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init
from typing import List
from ThreeDWidgets.constant import FR_COLOR
# draw a line in 3D world
import math
from dataclasses import dataclass

"""
Example using the Wheel

TODO: To make the wheel interactive, I have to separate the axis, center and the text
from pivy import coin
import fr_draw__wheel as dgw 
from PySide import QtCore,QtGui
import math
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
a=dgw.draw_Text_Wheel()
b=dgw.draw_Center_Wheel()
c=dgw.draw_Xaxis_Wheel()
d=dgw.draw_Yaxis_Wheel()
e=dgw.draw_45axis_Wheel()
f=dgw.draw_135axis_Wheel()

sg.addChild(a)
sg.addChild(b)
sg.addChild(c)
sg.addChild(d)
sg.addChild(e)
sg.addChild(f)


"""

def draw_Text_Wheel(vec=App.Vector(0.0,0.0,0.0), _color=FR_COLOR.FR_WHITE, _rotation=([0.0,0.0,1.0,0.0]), LineWidth=1.0):
    try:
        TextScale=0.04
        txtCol = coin.SoBaseColor()  # must be converted to SoBaseColor
        txtCol.rgb = _color
        txtXSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtXTransform = coin.SoTransform()
        txtXTransform.translation.setValue(5.0,0.0,0.0)
        txtXTransform.rotation.setValue(coin.SbVec3f(0.0,0.0, 0.0),math.radians(0.0))
        txtXTransform.scaleFactor.setValue(TextScale ,TextScale,TextScale)
        textX=["90.0°","____"]
        text3DX = coin.SoAsciiText()  # Draw text in the 3D world
        text3DX.string.setValues([l.encode("utf8") for l in textX if l])
        txtXSo.addChild(txtXTransform)
        txtXSo.addChild(txtCol)
        txtXSo.addChild(text3DX)
        
        txtXPSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtXPTransform = coin.SoTransform()
        txtXPTransform.translation.setValue(-5.0,0.0,0.0)
        txtXPTransform.rotation.setValue(coin.SbVec3f(0.0,0.0,0.0),math.radians(0.0))
        txtXPTransform.scaleFactor.setValue(TextScale,TextScale,TextScale)
        textXP=["270.0°",""]
        text3DXP = coin.SoAsciiText()  # Draw text in the 3D world
        text3DXP.string.setValues([l.encode("utf8") for l in textXP if l])
        txtXPSo.addChild(txtXPTransform)
        txtXPSo.addChild(txtCol)
        txtXPSo.addChild(text3DXP)
        
        txtYSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtYTransform = coin.SoTransform()
        txtYTransform.translation.setValue(0.0,5.0,0.0)
        txtYTransform.rotation.setValue(coin.SbVec3f(0.0,0.0, 0.0),math.radians(0.0))
        txtYTransform.scaleFactor.setValue(TextScale,TextScale,TextScale)
        textY=["0.0°",""]
        text3DY = coin.SoAsciiText()  # Draw text in the 3D world
        text3DY.string.setValues([l.encode("utf8") for l in textY if l])
        txtYSo.addChild(txtYTransform)
        txtYSo.addChild(txtCol)
        txtYSo.addChild(text3DY)
        
        txtYPSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtYPTransform = coin.SoTransform()
        txtYPTransform.translation.setValue(0.0,-5.0,0.0)
        txtYPTransform.rotation.setValue(coin.SbVec3f(0.0,0.0, 0.0),math.radians(0.0))
        txtYPTransform.scaleFactor.setValue(TextScale,TextScale,TextScale)
        textYP=["180.0°",""]
        text3DYP = coin.SoAsciiText()  # Draw text in the 3D world
        text3DYP.string.setValues([l.encode("utf8") for l in textYP if l])
        txtYPSo.addChild(txtYPTransform)
        txtYPSo.addChild(txtCol)
        txtYPSo.addChild(text3DYP)
        
        groupT=coin.SoSeparator()
        groupT.addChild(txtXSo)
        groupT.addChild(txtXPSo)
        groupT.addChild(txtYSo)
        groupT.addChild(txtYPSo)
        
        txtRoot =coin.SoSeparator()
        txtrootTrans=coin.SoTransform()
        txtrootTrans.rotation.setValue(coin.SbVec3f(1.0,0.0, 0.0),math.radians(90))
        txtRoot.addChild(txtrootTrans)
        txtRoot.addChild(groupT)
        
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        
        material=coin.SoMaterial()
        material.diffuseColor.setValue (_color)
        material.emissiveColor.setValue (_color)
        material.specularColor.setValue( 0.0, 0.0, 0.0)
        material.emissiveColor.setValue(0.0, 0.0, 0.0)
        material.transparency.setValue(0.0)

        root = coin.SoSeparator()
        transla=coin.SoTranslation()
        transla.translation.setValue([vec.x,vec.y,vec.z])

        root.addChild(material)
        root.addChild(rootTransform)        
        root.addChild(transla)
        root.addChild(txtRoot)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_Center_Wheel(vec=App.Vector(0,0,0), _color=FR_COLOR.FR_GLASS, _rotation=[0,0,1,0], LineWidth=1):
    try:
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = _color
        coly = coin.SoBaseColor()  # must be converted to SoBaseColor
        coly.rgb = FR_COLOR.FR_GREENYELLOW
        colCenter = coin.SoBaseColor()  # must be converted to SoBaseColor
        colCenter.rgb = FR_COLOR.FR_BROWN
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        root = coin.SoSeparator()
        transla=coin.SoTranslation()
        transla.translation.setValue([vec.x,vec.y,vec.z])
        root.addChild(transla)
        
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        
        material=coin.SoMaterial()
        material.transparency.setValue(0.80)
        material.diffuseColor.setValue (_color)
        
        centerseparator=coin.SoSeparator() 
        center=coin.SoCylinder()
        transcenter=coin.SoTransform()   #Center cylinder
        tempC = coin.SbVec3f()
        tempC.setValue(1,0,0)
        transcenter.rotation.setValue(tempC, math.radians(90))
        center.radius=1.75
        center.height=0.25
        centerseparator.addChild(transcenter)
        centerseparator.addChild(colCenter)
        centerseparator.addChild(center)
        group= coin.SoSeparator()
        
        transG=coin.SoTransform()
        tempG = coin.SbVec3f()
        tempG.setValue(1,0,0)
        transG.rotation.setValue(tempG, math.radians(90))
        group.addChild(transG)
        group.addChild(centerseparator)
        
        root.addChild(material)
        root.addChild(rootTransform)        
        root.addChild(transla)
        #root.addChild(col1)
        root.addChild(group)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_Xaxis_Wheel(vec=App.Vector(0,0,0), _color=FR_COLOR.FR_WHITE, _rotation=[0,0,1,0], LineWidth=1):
    try:
        colx = coin.SoBaseColor()  # must be converted to SoBaseColor
        colx.rgb = FR_COLOR.FR_INDIANRED
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        root = coin.SoSeparator()
        transla=coin.SoTranslation()
        transla.translation.setValue([vec.x,vec.y,vec.z])
        separatorX=coin.SoSeparator() # x
        axisx=coin.SoCylinder()
        transX=coin.SoTransform()
        tempX = coin.SbVec3f()
        tempX.setValue(0,0,1)
        transX.rotation.setValue(tempX, math.radians(90))
        axisx.radius=0.125
        axisx.height=10
        separatorX.addChild(transX)
        separatorX.addChild(colx)
        separatorX.addChild(axisx)
        group= coin.SoSeparator()
        transG=coin.SoTransform()
        tempG = coin.SbVec3f()
        tempG.setValue(1,0,0)
        transG.rotation.setValue(tempG, math.radians(90))
        group.addChild(transG)
        group.addChild(separatorX)
        
        root.addChild(transla)
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2]) 
        
        material=coin.SoMaterial()
        material.diffuseColor.setValue (_color)
        material.specularColor.setValue( 0, 0, 0)
        material.emissiveColor.setValue(0, 0, 0)
        material.transparency.setValue(0)
        root.addChild(material)
        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        root.addChild(rootTransform)        
        root.addChild(transla)
        root.addChild(group)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_Yaxis_Wheel(vec=App.Vector(0,0,0), _color=FR_COLOR.FR_WHITE, _rotation=[0,0,1,0], LineWidth=1):
    try:
        txtCol = coin.SoBaseColor()  # must be converted to SoBaseColor
        txtCol.rgb = FR_COLOR.FR_WHITE
        coly = coin.SoBaseColor()  # must be converted to SoBaseColor
        coly.rgb = FR_COLOR.FR_GREENYELLOW
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        root = coin.SoSeparator()
        transla=coin.SoTranslation()
        transla.translation.setValue([vec.x,vec.y,vec.z])

        separatorY=coin.SoSeparator() # Y
        axisY=coin.SoCylinder()
        transY=coin.SoTransform()
        tempY = coin.SbVec3f()
        tempY.setValue(0,0,1)
        transY.rotation.setValue(tempY, math.radians(0))
        axisY.radius=0.125
        axisY.height=10
        separatorY.addChild(transY)
        separatorY.addChild(coly)
        separatorY.addChild(axisY)        
        group= coin.SoSeparator()
        transG=coin.SoTransform()
        tempG = coin.SbVec3f()
        tempG.setValue(1,0,0)
        transG.rotation.setValue(tempG, math.radians(90))
        group.addChild(transG)
        group.addChild(separatorY)

        root.addChild(transla)
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])

        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        material=coin.SoMaterial()
        material.diffuseColor.setValue (_color)
        root.addChild(material)
        root.addChild(rootTransform)               
        root.addChild(transla)
        root.addChild(group)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

def draw_45axis_Wheel(vec=App.Vector(0,0,0), _color=FR_COLOR.FR_WHITE, _rotation=[0,0,1,0], LineWidth=1):
    try:
        col45 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col45.rgb = FR_COLOR.FR_BLUEVIOLET
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth

        separator45=coin.SoSeparator() # 45
        axis45=coin.SoCylinder()
        trans45=coin.SoTransform()
        temp45 = coin.SbVec3f()
        temp45.setValue(0,0,1)
        trans45.rotation.setValue(temp45, math.radians(45))
        axis45.radius=0.125
        axis45.height=7
        separator45.addChild(trans45)
        separator45.addChild(col45)
        separator45.addChild(axis45)        

        group= coin.SoSeparator()
        transG=coin.SoTransform()
        tempG = coin.SbVec3f()
        tempG.setValue(1,0,0)
        transG.rotation.setValue(tempG, math.radians(90))
        group.addChild(transG)

        group.addChild(separator45)
        
        root = coin.SoSeparator()
        transla=coin.SoTranslation()
        transla.translation.setValue([vec.x,vec.y,vec.z])
        root.addChild(transla)
        material=coin.SoMaterial()
        material.diffuseColor.setValue (_color)
        material.specularColor.setValue( 0, 0, 0)
        material.emissiveColor.setValue(0, 0, 0)
        material.transparency.setValue(0)
        root.addChild(material)
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        
        root.addChild(transla)        
        root.addChild(rootTransform)        
        root.addChild(group)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def draw_135axis_Wheel(vec=App.Vector(0,0,0), _color=FR_COLOR.FR_WHITE, _rotation=[0,0,1,0], LineWidth=1):
    try:
        col135 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col135.rgb = FR_COLOR.FR_ORANGE

        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth

        separator135=coin.SoSeparator() # 135
        axis135=coin.SoCylinder()
        trans135=coin.SoTransform()
        temp135 = coin.SbVec3f()
        temp135.setValue(0,0,1)
        trans135.rotation.setValue(temp135, math.radians(135))
        axis135.radius=0.125
        axis135.height=7
        separator135.addChild(trans135)
        separator135.addChild(col135)
        separator135.addChild(axis135)        

        group= coin.SoSeparator()
        transG=coin.SoTransform()
        tempG = coin.SbVec3f()
        tempG.setValue(1,0,0)
        transG.rotation.setValue(tempG, math.radians(90))
        group.addChild(transG)
        group.addChild(separator135)
        
        material=coin.SoMaterial()
        transla=coin.SoTranslation()       
        root = coin.SoSeparator()       
        root.addChild(transla)        
        transla.translation.setValue([vec.x,vec.y,vec.z])    
        material.diffuseColor.setValue (_color)
        material.specularColor.setValue( 0, 0, 0)
        material.emissiveColor.setValue(0, 0, 0)
        material.transparency.setValue(0)
        
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        root.addChild(material)
        root.addChild(rootTransform)              
        root.addChild(transla)
        root.addChild(group)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)