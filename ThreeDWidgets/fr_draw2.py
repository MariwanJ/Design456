
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
Example using the DegreeWeel

from pivy import coin
import fr_draw2 as d 

sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
root=d.draw_DegreeWheel()
sg.addChild(root)

"""

def draw_DegreeWheel(vec=App.Vector(0,0,0), _color=(1,1,1), _rotation=[0,0,1,0], LineWidth=1):
    try:
        TextScale=0.04
        txtCol = coin.SoBaseColor()  # must be converted to SoBaseColor
        txtCol.rgb = FR_COLOR.FR_WHITE

        col1 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col1.rgb = _color

        colx = coin.SoBaseColor()  # must be converted to SoBaseColor
        colx.rgb = FR_COLOR.FR_ORANGERED

        coly = coin.SoBaseColor()  # must be converted to SoBaseColor
        coly.rgb = FR_COLOR.FR_GREENYELLOW

        colCenter = coin.SoBaseColor()  # must be converted to SoBaseColor
        colCenter.rgb = FR_COLOR.FR_BROWN

        col45 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col45.rgb = FR_COLOR.FR_BLUEVIOLET

        col135 = coin.SoBaseColor()  # must be converted to SoBaseColor
        col135.rgb = FR_COLOR.FR_ORANGE


        txtCol = coin.SoBaseColor()  # must be converted to SoBaseColor
        txtCol.rgb =(0.9,0.6,0.1)
        txtXSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtXTransform = coin.SoTransform()
        txtXTransform.translation.setValue(App.Vector(5,0,0))
        txtXTransform.rotation.setValue(coin.SbVec3f(0,0, 0),math.radians(0))
        txtXTransform.scaleFactor.setValue(TextScale ,TextScale,TextScale)
        textX=["90.0°",]
        text3DX = coin.SoAsciiText()  # Draw text in the 3D world
        text3DX.string.setValues([l.encode("utf8") for l in textX if l])
        txtXSo.addChild(txtXTransform)
        txtXSo.addChild(txtCol)
        txtXSo.addChild(text3DX)


        txtXPSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtXPTransform = coin.SoTransform()
        txtXPTransform.translation.setValue(App.Vector(-5,0,0))
        txtXPTransform.rotation.setValue(coin.SbVec3f(0,0, 0),math.radians(0))
        txtXPTransform.scaleFactor.setValue(TextScale,TextScale,TextScale)
        textXP=["270.0°",]
        text3DXP = coin.SoAsciiText()  # Draw text in the 3D world
        text3DXP.string.setValues([l.encode("utf8") for l in textXP if l])
        txtXPSo.addChild(txtXPTransform)
        txtXPSo.addChild(txtCol)
        txtXPSo.addChild(text3DXP)


        txtYSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtYTransform = coin.SoTransform()
        txtYTransform.translation.setValue(App.Vector(0,5,0))
        txtYTransform.rotation.setValue(coin.SbVec3f(0,0, 0),math.radians(0))
        txtYTransform.scaleFactor.setValue(TextScale,TextScale,TextScale)
        textY=["0.0°",]
        text3DY = coin.SoAsciiText()  # Draw text in the 3D world
        text3DY.string.setValues([l.encode("utf8") for l in textY if l])
        txtYSo.addChild(txtYTransform)
        txtYSo.addChild(txtCol)
        txtYSo.addChild(text3DY)

        txtYPSo = coin.SoSeparator()  # must be converted to SoBaseColor
        txtYPTransform = coin.SoTransform()
        txtYPTransform.translation.setValue(App.Vector(0,-5,0))
        txtYPTransform.rotation.setValue(coin.SbVec3f(0,0, 0),math.radians(0))
        txtYPTransform.scaleFactor.setValue(TextScale,TextScale,TextScale)
        textYP=["180.0°",]
        text3DYP = coin.SoAsciiText()  # Draw text in the 3D world
        text3DYP.string.setValues([l.encode("utf8") for l in textYP if l])
        txtYPSo.addChild(txtYPTransform)
        txtYPSo.addChild(txtCol)
        txtYPSo.addChild(text3DYP)


        group=coin.SoSeparator()
        group.addChild(txtXSo)
        group.addChild(txtXPSo)
        group.addChild(txtYSo)
        group.addChild(txtYPSo)


        txtRoot =coin.SoSeparator()
        txtrootTrans=coin.SoTransform()
        txtrootTrans.rotation.setValue(coin.SbVec3f(1,0, 0),math.radians(90))
        txtRoot.addChild(txtrootTrans)
        txtRoot.addChild(group)

        root = coin.SoSeparator()
        transla=coin.SoTranslation()
        transla.translation.setValue(vec)
        root.addChild(transla)
        tempR = coin.SbVec3f()
        tempR.setValue(_rotation[0], _rotation[1], _rotation[2])
        rootTransform=coin.SoTransform()
        rootTransform.rotation.setValue(tempR, math.radians(_rotation[3]))
        
        material=coin.SoMaterial()
        material.ambientColor.setValue(0.2, 0.2, 0.2) #check this
        material.diffuseColor.setValue (_color)
        material.specularColor.setValue( 0, 0, 0)
        material.emissiveColor.setValue(0, 0, 0)
        material.transparency.setValue(0)
        root.addChild(material)
        root.addChild(rootTransform)

        centerseparator=coin.SoSeparator() 
        center=coin.SoCylinder()
        transcenter=coin.SoTransform()   #Center cylinder
        tempC = coin.SbVec3f()
        tempC.setValue(1,0,0)
        transcenter.rotation.setValue(tempC, math.radians(90))
        center.radius=2.5
        center.height=0.25
        centerseparator.addChild(transcenter)
        centerseparator.addChild(colCenter)
        centerseparator.addChild(center)

        separatorX=coin.SoSeparator() # x
        axisx=coin.SoCylinder()
        transX=coin.SoTransform()
        tempX = coin.SbVec3f()
        tempX.setValue(0,0,1)
        transX.rotation.setValue(tempX, math.radians(90))
        axisx.radius=0.15
        axisx.height=10
        separatorX.addChild(transX)
        separatorX.addChild(colx)
        separatorX.addChild(axisx)
        
        separatorY=coin.SoSeparator() # Y
        axisY=coin.SoCylinder()
        transY=coin.SoTransform()
        tempY = coin.SbVec3f()
        tempY.setValue(0,0,1)
        transY.rotation.setValue(tempY, math.radians(0))
        axisY.radius=0.15
        axisY.height=10
        separatorY.addChild(transY)
        separatorY.addChild(coly)
        separatorY.addChild(axisY)        

        separator45=coin.SoSeparator() # 45
        axis45=coin.SoCylinder()
        trans45=coin.SoTransform()
        temp45 = coin.SbVec3f()
        temp45.setValue(0,0,1)
        trans45.rotation.setValue(temp45, math.radians(45))
        axis45.radius=0.15
        axis45.height=10
        separator45.addChild(trans45)
        separator45.addChild(col45)
        separator45.addChild(axis45)        

        separator135=coin.SoSeparator() # 135
        axis135=coin.SoCylinder()
        trans135=coin.SoTransform()
        temp135 = coin.SbVec3f()
        temp135.setValue(0,0,1)
        trans135.rotation.setValue(temp135, math.radians(135))
        axis135.radius=0.15
        axis135.height=10
        separator135.addChild(trans135)
        separator135.addChild(col135)
        separator135.addChild(axis135)        

        group= coin.SoSeparator()
        transG=coin.SoTransform()
        tempG = coin.SbVec3f()
        tempG.setValue(1,0,0)
        transG.rotation.setValue(tempG, math.radians(90))
        group.addChild(transG)

        group.addChild(centerseparator)
        group.addChild(separatorX)
        
        group.addChild(separatorY)
        
        group.addChild(separator45)
        group.addChild(separator135)
        
        root.addChild(rootTransform)        
        root.addChild(transla)
        root.addChild(col1)
        root.addChild(group)
        root.addChild(txtRoot)
        return root

    except Exception as err:
        App.Console.PrintError("'DegreesWheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
