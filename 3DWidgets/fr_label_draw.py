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


def draw_label(labelcolor=(1.0, 0.0, 1.0), labelfont='sans', size=14, trans=(0, 0, 0), text=''):
    global textNode
    _textNode =coin.SoSeparator()   # A Separator to separate the text from the drawing
    font = coin.SoFont()
    _transform=coin.SoTransform()    #determine location
    _text = coin.SoText2()
    _text.string.setValue(text)
    _text.justification = coin.SoText2.LEFT  #This must be as value not fixed #TODO FIXME
    font.Name=labelfont
    font.size=size
    coinColor = coin.SoMaterial()
    binding = coin.SoMaterialBinding()
    binding.value = coin.SoMaterialBinding.PER_PART 
    coinColor.rgb = labelcolor
    transNode = coin.SoTransform()
    _textNode.addChild(font)
    _textNode.addChild(_transform)
    _textNode.addChild(transNode)
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
