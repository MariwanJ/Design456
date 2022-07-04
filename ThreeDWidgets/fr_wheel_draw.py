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

__updated__ = '2022-07-04 20:23:45'

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


def draw_Text_Wheel(_color=FR_COLOR.FR_WHITE,
                    setupRotation=[0, 0, 0], 
                    _Scale=[1, 1, 1],LineWidth=1.0):
    try:
        TextScale = 0.04
        txtCol = coin.SoBaseColor()  # must be converted to SoBaseColor
        txtCol.rgb = _color
        txtXSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtXSo.Name = "270Degree"
        txtXTransform = coin.SoTransform()
        txtXTransform.translation.setValue(5.5, 0.0, 0.0)
        txtXTransform.rotation.setValue(
            coin.SbVec3f(6.0, 0.0, 0.0), math.radians(0.0))
        txtXTransform.scaleFactor.setValue(TextScale, TextScale, TextScale)
        textX = ["270.0°", ""]
        text3DX = coin.SoAsciiText()  # Draw text in the 3D world
        text3DX.string.setValues([l.encode("utf8") for l in textX if l])
        txtXSo.addChild(txtXTransform)
        txtXSo.addChild(txtCol)
        txtXSo.addChild(text3DX)

        txtXPSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtXPSo.Name = "180Degree"
        txtXPTransform = coin.SoTransform()
        txtXPTransform.translation.setValue(0.0, -5.5, 0.0)
        txtXPTransform.rotation.setValue(
            coin.SbVec3f(0.0, 0.0, 0.0), math.radians(0.0))
        txtXPTransform.scaleFactor.setValue(TextScale, TextScale, TextScale)
        textXP = ["180.0°", ""]
        text3DXP = coin.SoAsciiText()  # Draw text in the 3D world
        text3DXP.string.setValues([l.encode("utf8") for l in textXP if l])
        txtXPSo.addChild(txtXPTransform)
        txtXPSo.addChild(txtCol)
        txtXPSo.addChild(text3DXP)

        txtYSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtYSo.Name = "0Degree"
        txtYTransform = coin.SoTransform()
        txtYTransform.translation.setValue(0.0, 5.5, 0.0)
        txtYTransform.rotation.setValue(
            coin.SbVec3f(0.0, 0.0, 0.0), math.radians(00.0))
        txtYTransform.scaleFactor.setValue(TextScale, TextScale, TextScale)
        textY = ["0.0°", ""]
        text3DY = coin.SoAsciiText()  # Draw text in the 3D world
        text3DY.string.setValues([l.encode("utf8") for l in textY if l])
        txtYSo.addChild(txtYTransform)
        txtYSo.addChild(txtCol)
        txtYSo.addChild(text3DY)

        txtYPSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtYPSo.Name = "90Degree"
        txtYPTransform = coin.SoTransform()
        txtYPTransform.translation.setValue(-6.0, 0.0, 0.0)
        txtYPTransform.rotation.setValue(
            coin.SbVec3f(0.0, 0.0, 0.0), math.radians(0.0))
        txtYPTransform.scaleFactor.setValue(TextScale, TextScale, TextScale)
        textYP = ["90.0°", ""]
        text3DYP = coin.SoAsciiText()  # Draw text in the 3D world
        text3DYP.string.setValues([l.encode("utf8") for l in textYP if l])
        txtYPSo.addChild(txtYPTransform)
        txtYPSo.addChild(txtCol)
        txtYPSo.addChild(text3DYP)

        groupT = coin.SoSeparator()
        groupT.Name = "GroupT"
        groupT.addChild(txtXSo)
        groupT.addChild(txtXPSo)
        groupT.addChild(txtYSo)
        groupT.addChild(txtYPSo)

        txtRoot = coin.SoSeparator()
        txtRoot.Name = "AllText-coordination"
        txtrootTrans = coin.SoTransform()
        txtrootTrans.rotation.setValue(
            coin.SbVec3f(1.0, 0.0, 0.0), math.radians(0))
        txtRoot.addChild(txtrootTrans)
        txtRoot.addChild(groupT)

        tRadiusX = coin.SbVec3f()
        tRadiusY = coin.SbVec3f()
        tRadiusZ = coin.SbVec3f()

        transfromX = coin.SoTransform()
        transfromY = coin.SoTransform()
        transfromZ = coin.SoTransform()

        tRadiusX.setValue(1, 0, 0)
        tRadiusY.setValue(0, 1, 0)
        tRadiusZ.setValue(0, 0, 1)
        transfromX.rotation.setValue(tRadiusX, math.radians(setupRotation[0]))
        transfromY.rotation.setValue(tRadiusY, math.radians(setupRotation[1]))
        transfromZ.rotation.setValue(tRadiusZ, math.radians(setupRotation[2]))

        SoSeparatorSetupX = coin.SoSeparator()
        SoSeparatorSetupX.Name = "SetupX"
        SoSeparatorSetupY = coin.SoSeparator()
        SoSeparatorSetupY.Name = "SetupY"
        SoSeparatorSetupZ = coin.SoSeparator()
        SoSeparatorSetupZ.Name = "SetupZ"

        SoSeparatorSetupX.addChild(transfromX)
        SoSeparatorSetupX.addChild(txtRoot)

        SoSeparatorSetupY.addChild(transfromY)
        SoSeparatorSetupY.addChild(SoSeparatorSetupX)

        SoSeparatorSetupZ.addChild(transfromZ)
        SoSeparatorSetupZ.addChild(SoSeparatorSetupY)
        rootTransform = coin.SoTransform()
        rootTransform.scaleFactor.setValue(_Scale)
        
        material = coin.SoMaterial()
        material.diffuseColor.setValue(_color)
        material.emissiveColor.setValue(_color)
        material.transparency.setValue(0.0)

        root = coin.SoSeparator()
        root.Name = "RootText"
        root.addChild(material)
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = _color

        root.addChild(rootTransform)
        root.addChild(col1)
        root.addChild(SoSeparatorSetupZ)
        return root

    except Exception as err:
        App.Console.PrintError("'Wheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

#We have only setup rotation, other rotation must be done later.
def draw_AllParts(Ptype: str = "",
                  _color=FR_COLOR.FR_RED,
                  setupRotation=[0, 0, 0, 0],
                  _Scale=[1, 1, 1],
                  LineWidth=1):

    style = coin.SoDrawStyle()
    style.lineWidth = LineWidth

    objectToDraw = coin.SoSeparator()
    theObject = coin.SoCylinder()
    transtheObject = coin.SoTransform()  # theObject cylinder

    tempC = coin.SbVec3f()
    if Ptype == "Center":
        objectToDraw.Name = "Center"
        tempC.setValue(1, 0, 0)
        transtheObject.rotation.setValue(tempC, math.radians(90))
        theObject.radius = 4.5
        theObject.height = 0.65
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = FR_COLOR.FR_GLASS
    elif Ptype == "Xaxis":
        objectToDraw.Name = "Xaxis"
        tempC.setValue(0, 0, 1)
        transtheObject.rotation.setValue(tempC, math.radians(90))
        theObject.radius = 0.25
        theObject.height = 20
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = FR_COLOR.FR_RED
    elif Ptype == "Yaxis":
        objectToDraw.Name = "Yaxis"
        tempC.setValue(0, 0, 1)
        transtheObject.rotation.setValue(tempC, math.radians(0))
        theObject.radius = 0.25
        theObject.height = 20
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = FR_COLOR.FR_GREENYELLOW
    elif Ptype == "45axis":
        objectToDraw.Name = "45axis"
        tempC.setValue(0, 0, 1)
        transtheObject.rotation.setValue(tempC, math.radians(45))
        theObject.radius = 0.25
        theObject.height = 14
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = FR_COLOR.FR_BLUEVIOLET
    elif Ptype == "135axis":
        objectToDraw.Name = "135Axis"
        tempC.setValue(0, 0, 1)
        transtheObject.rotation.setValue(tempC, math.radians(135))
        theObject.radius = 0.25
        theObject.height = 14
        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = FR_COLOR.FR_ORANGE

    objectToDraw.addChild(col1)   #cOLOR
    objectToDraw.addChild(transtheObject)    #ROTATION OF THE SUB OBJECT
    objectToDraw.addChild(theObject)         #THE DRAWN OBJECT

    tRadiusX = coin.SbVec3f()
    tRadiusY = coin.SbVec3f()
    tRadiusZ = coin.SbVec3f()

    #Axis
    tRadiusX.setValue(1, 0, 0)
    tRadiusY.setValue(0, 1, 0)
    tRadiusZ.setValue(0, 0, 1)

    tempTransform_x = coin.SoTransform()
    tempTransform_y = coin.SoTransform()
    tempTransform_z = coin.SoTransform()

    tempTransform_x.rotation.setValue(tRadiusX, math.radians(setupRotation[0]))
    tempTransform_y.rotation.setValue(tRadiusY, math.radians(setupRotation[1]))
    tempTransform_z.rotation.setValue(tRadiusZ, math.radians(setupRotation[2]))

    SoSeparatorSetupX = coin.SoSeparator()
    SoSeparatorSetupY = coin.SoSeparator()
    SoSeparatorSetupZ = coin.SoSeparator()

    SoSeparatorSetupX.addChild(tempTransform_x)
    SoSeparatorSetupX.addChild(objectToDraw)

    SoSeparatorSetupY.addChild(tempTransform_y)
    SoSeparatorSetupY.addChild(SoSeparatorSetupX)

    SoSeparatorSetupZ.addChild(tempTransform_z)
    SoSeparatorSetupZ.addChild(SoSeparatorSetupY)
    
    #Scale
    rootTransform = coin.SoTransform()
    rootTransform.scaleFactor.setValue(_Scale)

    root = coin.SoSeparator()
    root.Name = "RootAxisDrawing"
    
    #for giving color to the object
    material = coin.SoMaterial()
    if(Ptype == "Center"):
        material.transparency.setValue(0.80)
    else:
        material.transparency.setValue(0.0)
    material.diffuseColor.setValue(_color)
    material.emissiveColor.setValue(_color)
    
    root.addChild(rootTransform)
    root.addChild(SoSeparatorSetupZ)
    return root