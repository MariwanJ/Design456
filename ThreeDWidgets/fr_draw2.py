
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



def draw_DegreeWheel(vec=[], color=(1,1,1), _rotation=[0,0,1,0], LineWidth=1):
    try:
        root = coin.SoSeparator()
        transla=coin.SoTranslate()
        transla.translation.setValue(vec)
        root.addChild(transla)
        material=coin.SoMaterial()
        material.ambientColor.set (0.2, 0.2, 0.2) #check this
        material.diffuseColor (coin.SoColor(color))
        material.specularColor.setValue( 0, 0, 0,)
        material.emissiveColor.setValue(0, 0, 0)
        material.shininess(0.1)
        material.transparency (0.1)
        
        transcenter=coin.SoTransform()
        root.addChild(material)
        root.addChild(transcenter)

        centerseparator=coin.SoSeparator() 
        center=coin.SoCylinder()
        transcenter=coin.SoTranform()   #Center cylinder
        center.radius=5
        center.height=0.5
        centerseparator.addChild(transcenter)
        centerseparator.addChild(center)

        separator1=coin.SoSeparator() # x
        axisx=coin.SoCylinder()
        axisx.radius=0.5
        axisx.height=20        
        transX=coin.SoTransform()
        transX.rotation.setValue(1, 0, 0, math.radians(90))
        separator1.addChild(transX)
        separator1.addChild(axisx)
        

        separator2=coin.SoSeparator() # y
        axisy=coin.SoCylinder()
        axisy.radius=0.5
        axisy.height=20
        transY=coin.SoTransform()
        transY.rotation.setValue(0, 0, 1, math.radians(90))
        separator2.addChild(transY)                         
        separator2.addChild(axisy)

        separator3=coin.SoSeparator() # 45
        axis45=coin.SoCylinder()
        trans45=coin.SoTransform()
        axis45.radius=0.5
        axis45.height=20
        trans45.rotation.setValue(0, 0, 1, math.radians(90))
        separator2.addChild(trans45)
        separator2.addChild(axis45)                         

        separator4=coin.SoSeparator() # 135
        axis135=coin.SoCylinder()
        trans135=coin.SoTransform()
        axis135.radius=0.5
        axis135.height=20
        trans135=coin.SoTransform()
        trans135.rotation.setValue(0, 0, 1, math.radians(90))
        separator4.addChild(trans135)
        separator4.addChild(axis135)

        root.addChild(centerseparator)
        root.addChild(separator1)
        root.addChild(separator2)
        root.addChild(separator3)
        root.addChild(separator4)
        return root

    except Exception as err:
        App.Console.PrintError("'DegreesWheel' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
