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
        
def draw_label(labelcolor=(1.0, 0.0, 1.0), labelfont='sans', size=14,align=FR_ALIGN.FR_NO_ALIGN, trans=(0, 0, 0), text=''):
    global textNode

    _textNode =coin.SoSeparator()   # A Separator to separate the text from the drawing
    font = coin.SoFont()
    _transform=coin.SoTransform()    #determine location
    _text = coin.SoText2()              #Draw text in the 2D world #TODO: Should be 3D world?
    _text.string.setValue(text)         #Actual text
    _transNode = coin.SoTransform()
    font.Name=labelfont                 #Font used
    font.size=size                      #Font size
    coinColor = coin.SoMaterial()       #Font color
    binding = coin.SoMaterialBinding()
    binding.value = coin.SoMaterialBinding.PER_PART 
    coinColor.rgb = labelcolor
    ''' TODO :FIXME
    if align== FR_ALIGN.FR_NO_ALIGN:    #If there is no alignment, 
                               #we use the transNode. trans will not have effect if there is an alignment
        #TODO: Don't know how to do this. Must read, and experiment with this.
        _transNode.translation.setValue(trans)
        _text.justification = coin.SoText2.LEFT  #This must be as value not fixed #TODO FIXME
    else:
        _transNode.translation.setValue(calculateAlignment)
        '''
    _textNode.addChild(font)
    _textNode.addChild(_transform)
    _textNode.addChild(_transNode)
    _textNode.addChild(coinColor)
    _textNode.addChild(binding)
    _textNode.addChild(_text)
    return _textNode  # Return the created SoSeparator that contains the text

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
