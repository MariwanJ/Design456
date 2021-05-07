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

from constant import FR_ALIGN
from constant import FR_COLOR
from fr_widget import propertyValues 
import math
'''
                         Y
                         |
                -X +Y    |   +X +Y
              ___________|_______________X
                         |
                 -X-Y    |    +X -Y
                         |
'''
def calculateLineSpherical(vectors):
    # Calculate the three angles we have ref to xyz axis
    p1 = vectors[0]
    p2 = vectors[1]
    print(p1)
    print(p2)
    px2_px1=p2.x-p1.x
    py2_py1=p2.y-p1.y
    pz2_pz1=p2.z-p1.z
    r=math.sqrt(math.pow(px2_px1,2)+math.pow(py2_py1,2)+math.pow(pz2_pz1,2))
    factor=0
    if p2.x>0 and p2.y>0:          #+X+Y
        factor=0
    elif p2.x>0 and p2.y<0:        #+X-Y
        factor=math.radians(270)
    elif p2.x<0 and p2.y<0 :       #-X -Y
        factor=math.radians(180)
    elif p2.x<0 and p2.y>0 :       #-X +Y
        factor=math.radians(90)

    if(px2_px1==0):
        if(p2.y <0):
            thi=math.radians(180)    
        else:
            thi=math.radians(90)
    else: 
        thi=abs(math.atan(py2_py1/px2_px1))
    if(pz2_pz1==0):
        phi=math.radians(0)
        factor=0
    else: 
        phi=(math.radians(90)+(math.atan(math.sqrt(math.pow(px2_px1,2)+math.pow(py2_py1,2))/pz2_pz1)))
    print (thi)
    print (factor)
    thi=thi + factor
    print  (r,thi,phi)
    return (r,thi,phi)

# todo FIXME
# this should return the lblPosition calculate based on the Vector position.
def calculateAlignment(vectors, align):
    lblPos =coin.SoTransform()    # Use this to put all data needed for the lblPosition
    p1 = p2 = p3 = p4 = None
    # These variables will keep the min value of each coordinations
        # WE HAVE LEFT ALIGNMENT
    p1 = vectors[0]
    p2 = vectors[1]
    FourVector = False
    if len(vectors == 4):
        FourVector = True
        p3 = vectors[0]
        p4 = vectors[1]

    minX = minY = minZ = maxX = minY = minZ = None
    if FourVector == 1:
        minX = min([p1.x, p2.x, p3.x, p4.x])
        minY = min([p1.y, p2.y, p3.y, p4.y])
        minZ = min([p1.z, p2.z, p3.z, p4.z])
    else:
        minX = min([p1.x, p2.x])
        minY = min([p1.y, p2.y])
        minZ = min([p1.z, p2.z])
    if FourVector:
        maxX = max([p1.x, p2.x, p3.x, p4.x])
        maxY = max([p1.y, p2.y, p3.y, p4.y])
        maxZ = max([p1.z, p2.z, p3.z, p4.z])
    else:
        maxX = max([p1.x, p2.x])
        maxY = max([p1.y, p2.y])
        maxZ = max([p1.z, p2.z])

    if len(vectors) < 2:
        return (0, 0, 0)  # We don't have any vectors, return zero
        '''
        The shape is like this
                                p1___________________ p2
                                |                    |
                                |    face            |
                                |                    |
                               p3 ___________________ p4
        not having p3,p4 means it is a line only
        '''
    if align == FR_ALIGN.FR_ALIGN_LEFT or align == FR_ALIGN.FR_ALIGN_LEFT_BOTTOM:

        return (p1)

    elif align == FR_ALIGN.FR_ALIGN_RIGHT or align == FR_ALIGN.FR_ALIGN_RIGHT_BOTTOM:
        # WE HAVE RIGHT ALIGNMENT
        pass
    elif align == FR_ALIGN.FR_ALIGN_CENTER or align == FR_ALIGN.FR_ALIGN_CENTER_BOTTOM:
        # WE HAVE CENTER-BOTTOM ALIGNMENT
        pass
    elif align == FR_ALIGN.FR_ALIGN_LEFT_TOP:
        # Align LEFT-TOP
        pass
    elif align == FR_ALIGN.FR_ALIGN_RIGHT_TOP:
        # Align RIGHT-TOP
        pass
    elif align == FR_ALIGN.FR_ALIGN_CENTER_TOP:
        # Align CENTER-TOP
        pass
    elif align == FR_ALIGN.FR_ALIGN_CENTER_CENTER:
        # Align LEFT-TOP
        pass

def draw_label(text=[], prop: propertyValues=None):
    ''' Draw widgets label relative to the position with alignment'''
    if text=='' or prop ==None: 
        return     # Nothing to do here 
    try:
        delta=App.Vector(0,0,0)
        print (prop.vectors)

        p1=App.Vector(prop.vectors[0])  #You must cast the value or it will fail
        p2=App.Vector(prop.vectors[1])
        delta.x=p1.x+2
        delta.y=p1.y+2
        delta.z=p1.z
        (r,thi,phi)=calculateLineSpherical(prop.vectors)
        _transPositionPOS=coin.SoTransform()
        _transPositionX = coin.SoTransform()
        _transPositionY = coin.SoTransform()
        _transPositionZ = coin.SoTransform()
        _transPositionPOS.translation.setValue(delta)
        _transPositionY.translation.setValue(App.Vector(0,0,0))
        _transPositionZ.translation.setValue(App.Vector(0,0,0))
        print (delta)
        _transPositionY.rotation.setValue(coin.SbVec3f(1,0, 0),phi)
        _transPositionZ.rotation.setValue(coin.SbVec3f(0, 0, 1),thi)

        font = coin.SoFont()
        font.size = prop.fontsize  # Font size
        font.Name = prop.labelfont  # Font used
        _text3D = coin.SoAsciiText()  # Draw text in the 3D world
        _text3D.string.setValues([l.encode("utf8") for l in text if l])
        #_text3D.justification = coin.SoAsciiText.LEFT
        coinColor = coin.SoMaterial()  # Font color
        coinColor.diffuseColor.set1Value(0, coin.SbColor(*prop.labelcolor))
        _textNode = coin.SoSeparator()   # A Separator to separate the text from the drawing
        _textNode.addChild(_transPositionPOS)
        if phi!=0:
            _textNode.addChild(_transPositionY)
        if thi!=0:
            _textNode.addChild(_transPositionZ)
        
        
        _textNode.addChild(coinColor)
        _textNode.addChild(font)
        _textNode.addChild(_text3D)
        return _textNode  # Return the created SoSeparator that contains the text
    except Exception as err:
        App.Console.PrintError("'draw_label' Failed. "
                                   "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)