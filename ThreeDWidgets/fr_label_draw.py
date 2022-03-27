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
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import Design456Init


from ThreeDWidgets.constant import FR_COLOR
from ThreeDWidgets.fr_widget import propertyValues
import math

__updated__ = '2021-12-31 08:57:06'

def draw_label(text=[], prop: propertyValues = None):
    ''' Draw widgets label relative to the position with 
        prop: Consist of several data for example:
        prop.vectors = [App.Vector(0, 0, 0), ]
        prop.linewidth = 1
        prop.fontName = 'sans'
        prop.fontsize = 2
        prop.labelcolor = constant.FR_COLOR.FR_BLACK
        prop.rotation = [0.0, 0.0, 0.0, 0.0] # Normal rotation like you have in FreeCAD objects
        prop.SetupRotation = [0.0, 0.0, 0.0] # in degrees . This is a pre-rotation during initialization
        prop.scale = [1.0, 1.0, 1.0]
        
        
    Example:
            from pivy import coin
            from PySide import QtCore,QtGui
            import fr_label_draw as l
            import fr_widget as w
            
            sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
            p=w.propertyValues()
            p.vectors=[App.Vector(20,20,0),App.Vector(0.0, 0.0, 0.0)]
            wl=l.draw_label(["My Label",],p)
            sg.addChild(wl)
    '''
    if text == '' or prop is None:
        return     # Nothing to do here
    try:
        delta = App.Vector(0, 0, 0)
        # You must cast the value or it will fail
        p1 = App.Vector(prop.vectors[0])
        p2 = App.Vector(prop.vectors[1])
        delta.x = p1.x+3
        delta.y = p1.y+3
        delta.z = p1.z
        # get spherical representation of the point(p2)
        #(r, thi, phi) = calculateLineSpherical(prop.vectors)
        xAng = math.radians(prop.SetupRotation[0])
        yAng = math.radians(prop.SetupRotation[1])
        zAng = math.radians(prop.SetupRotation[2])

        _rootTrasnPOS = coin.SoTranslation()  # location
        _rootRotation = coin.SoTransform()
        
        _transRotationX = coin.SoTransform()
        _transRotationY = coin.SoTransform()
        _transRotationZ = coin.SoTransform()
        
        _rootTrasnPOS.translation.setValue(coin.SbVec3f(delta))
        tempRX = coin.SbVec3f()
        tempRX.setValue(1, 0, 0)
        tempRY = coin.SbVec3f()
        tempRY.setValue(0, 1, 0)
        tempRZ = coin.SbVec3f()
        tempRZ.setValue(0, 0, 1)
        
        _transRotationX.rotation.setValue(tempRX, xAng)
        _transRotationY.rotation.setValue(tempRY, yAng)
        _transRotationZ.rotation.setValue(tempRZ, zAng)

        _rootRotation.rotation.setValue(coin.SbVec3f(prop.rotation[0],
                                                     prop.rotation[1],
                                                     prop.rotation[2]),
                                        prop.rotation[3])

        font = coin.SoFont()
        font.size = prop.fontsize  # Font size
        font.Name = prop.fontName  # Font used
        _text3D = coin.SoAsciiText()  # Draw text in the 3D world
        _text3D.string.setValues([l.encode("utf8") for l in text if l])

        coinColor = coin.SoMaterial()  # Font color
        color = prop.labelcolor

        coinColor.diffuseColor.set1Value(0, coin.SbColor(*color))
        #coinColor.diffuseColor.set1Value(0, coin.SbColor(*prop.labelcolor))
        
        _textNode = coin.SoSeparator()   # A Separator to separate the text from the drawing
        
        _textNode.addChild(font)
        _textNode.addChild(coinColor)
        _textNode.addChild(_text3D)
        xSoNod = coin.SoSeparator()   # A Separator to Keep the rotation
        ySoNod = coin.SoSeparator()   # A Separator to Keep the rotation
        zSoNod = coin.SoSeparator()   # A Separator to Keep the rotation
        
        xSoNod.addChild(_transRotationX)
        xSoNod.addChild(_textNode)
        
        ySoNod.addChild(_transRotationY)
        ySoNod.addChild(xSoNod)
        
        zSoNod.addChild(_transRotationZ)
        zSoNod.addChild(ySoNod)
        
        root = coin.SoSeparator()
        root.addChild(_rootRotation)
        root.addChild(_rootTrasnPOS)
        root.addChild(zSoNod)

        return root  # Return the created SoSeparator that contains the text

    except Exception as err:
        App.Console.PrintError("'draw_label' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


# New label draw .. must be better in determining direct, rotation


def draw_newlabel(text=[], prop: propertyValues = None):
    ''' Draw widgets label relative to the vectors given to the function
    The three angel will decide how the text will be rotated based on that
    vectors. 

    '''
    if text == '' or prop is None:
        raise ValueError        # Nothing to do here
    try:
        p1 = prop.vectors[0]
        # if len(prop.vectors) >= 2:
        #     p2 = prop.vectors[1]

        # direction=
        _translation = coin.SoTranslation()  # coin.SoTransform()
        _transform = coin.SoTransform()
        _transformX = coin.SoTransform()
        _transformY = coin.SoTransform()
        _transformZ = coin.SoTransform()
        _transform.scaleFactor.setValue(prop.scale)  # Only for scaling

        _translation.translation.setValue(coin.SbVec3f(p1))
        
        _transformY.rotation.setValue(coin.SbVec3f(
            1, 0, 0), math.radians(prop.SetupRotation[0]))
        _transformX.rotation.setValue(coin.SbVec3f(
            0, 1, 0), math.radians(prop.SetupRotation[1]))
        _transformZ.rotation.setValue(coin.SbVec3f(
            0, 0, 1), math.radians(prop.SetupRotation[2]))
        font = coin.SoFont()
        font.size = prop.fontsize  # Font size
        font.Name = prop.fontName  # Font used
        _text3D = coin.SoAsciiText()  # Draw text in the 3D world
        _text3D.string.setValues(text)#([l.encode("utf8") for l in text if l])
        coinColor = coin.SoMaterial()  # Font color
        coinColor.diffuseColor.setValue(prop.labelcolor)
        coinColor.emissiveColor.setValue(prop.labelcolor)
        root = coin.SoSeparator()    # A Separator to separate the text from the drawing
        _textNodeX = coin.SoSeparator()   # A Separator to Keep the rotation in X Axis
        _textNodeY = coin.SoSeparator()   # A Separator to Keep the rotation in Y Axis
        _textNodeZ = coin.SoSeparator()   # A Separator to Keep the rotation in Z Axis
        
        _textNodeX.addChild(_transformX)
        _textNodeY.addChild(_transformY)
        _textNodeZ.addChild(_transformZ)

        _textNodeX.addChild(coinColor)
        _textNodeX.addChild(font)
        _textNodeX.addChild(_text3D)

        _textNodeY.addChild(_textNodeX)
        _textNodeZ.addChild(_textNodeY)

        root.addChild(_translation)
        root.addChild(_transform)
        root.addChild(_textNodeZ)
        return root  # Return the created SoSeparator that contains the text

    except Exception as err:
        App.Console.PrintError("'draw_label' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
