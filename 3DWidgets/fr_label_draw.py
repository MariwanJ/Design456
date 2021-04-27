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

#todo continue fixing this code 2021-04-23 Mariwan
def calculateAlignment(vectors,align):
    p1=p2=p3=p4=None
    #These variables will keep the min value of each coordinations
        #WE HAVE LEFT ALIGNMENT
    p1=vectors[0]
    p2=vectors[1]
    FourVector=False
    if len(vectors==4):
        FourVector=True
        p3=vectors[0]
        p4=vectors[1]
        
    minX=minY=minZ=maxX=minY=minZ=None
    if FourVector==1:
        minX=min([p1.x,p2.x,p3.x,p4.x])
        minY=min([p1.y,p2.y,p3.y,p4.y])
        minZ=min([p1.z,p2.z,p3.z,p4.z])
    else:
        minX=min([p1.x,p2.x])
        minY=min([p1.y,p2.y])
        minZ=min([p1.z,p2.z])
    if FourVector:
        maxX=max([p1.x,p2.x,p3.x,p4.x])
        maxY=max([p1.y,p2.y,p3.y,p4.y])
        maxZ=max([p1.z,p2.z,p3.z,p4.z])
    else:
        maxX=max([p1.x,p2.x])
        maxY=max([p1.y,p2.y])
        maxZ=max([p1.z,p2.z])

    if len(vectors)<2:
        return (0,0,0)  #We don't have any vectors, return zero 
        '''
        The shape is like this
                                p1___________________ p2  
                                |                    |
                                |    face            |
                                |                    |
                               p3 ___________________ p4
        not having p3,p4 means it is a line only
        '''
    if align==FR_ALIGN.FR_ALIGN_LEFT or align==FR_ALIGN.FR_ALIGN_LEFT_BOTTOM:

        
        
        return (p1)
        
    elif align==FR_ALIGN.FR_ALIGN_RIGHT or align==FR_ALIGN.FR_ALIGN_RIGHT_BOTTOM:
        #WE HAVE RIGHT ALIGNMENT
        pass
    elif align==FR_ALIGN.FR_ALIGN_CENTER or align==FR_ALIGN.FR_ALIGN_CENTER_BOTTOM:
        #WE HAVE CENTER-BOTTOM ALIGNMENT
        pass
    elif align==FR_ALIGN.FR_ALIGN_LEFT_TOP:
        #Align LEFT-TOP
        pass
    elif align==FR_ALIGN.FR_ALIGN_RIGHT_TOP:
        #Align RIGHT-TOP
        pass
    elif align==FR_ALIGN.FR_ALIGN_CENTER_TOP:
        #Align CENTER-TOP
        pass
    elif align==FR_ALIGN.FR_ALIGN_CENTER_CENTER:
        #Align LEFT-TOP
        pass
        
def draw_label(labelcolor=(1, 0, 1), labelfont='sans', size=20,align=FR_ALIGN.FR_NO_ALIGN, trans=App.Vector(0.0, 0.0, 0.0), text=''):
    # try:
    global _textNode
    _transPosition = coin.SoTransform()
    pos=App.Vector(30,30,0)
    p=pos
    _transPosition.translation.setValue(p.x+10,p.y+10,p.z+10)
    #_transPosition.translation.setValue(trans)
    font = coin.SoFont()
    font.size=size                      #Font size   
    #font.Name=labelfont                 #Font used
    _text3D = coin.SoAsciiText()           #Draw text in the 3D world 
    #_text3D.string.setValues(text)         #Actual text
    _text3D.string.setValues([l.encode("utf8") for l in text if l])
    print(labelcolor)
    color=(1,0,0)
    coinColor = coin.SoMaterial()       #Font color
    coinColor.diffuseColor.set1Value(0, coin.SbColor(*color))
    _textNode =coin.SoSeparator()   # A Separator to separate the text from the drawing
    _textNode.addChild(_transPosition)
    _textNode.addChild(coinColor)
    _textNode.addChild(font)
    _textNode.addChild(_text3D)
    root=Gui.ActiveDocument.ActiveView.getSceneGraph()
    newNode=coin.SoSeparator()
    newNode.addChild(_textNode)
    root.addChild(newNode)
    return newNode  # Return the created SoSeparator that contains the text
    # except Exception as err:
    #     App.Console.PrintError("'Design456_Extract' Failed. "
    #                                "{err}\n".format(err=str(err)))
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)


    """@property
    def font(self):
        return self.fontNode.name.getValue()

    @font.setter
    def font(self, name):
        self.fontNode.name = name

    @property
    def size(self):
        return self.fontNode.size.getValue()

    @size.setter
    def size(self, size):
        self.fontNode.size.setValue(size)

    @property
    def trans(self):
        return self.transNode.translation.getValue().getValue()

    @trans.setter
    def trans(self, trans):
        self.transNode.translation.setValue([trans[0],trans[1],trans[2]])

    @property
    def text(self):
        return self.textNode.string.getValues()[0]

    @text.setter
    def text(self, text):
        self.textNode.string = text
    """
