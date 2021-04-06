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


def draw_label(labelcolor=(0.0, 0.0, 0.0), labelfont='sans', size=14, trans=(0, 0, 0), text=''):
    global textNode
    _textNode = coin.SoSeparator()   # A Separator to separate the text from the drawing
    _textNode.coinColor = coin.SoMaterial()
    _textNode.binding = coin.SoMaterialBinding()
    _textNode.binding.value = coin.SoMaterialBinding.PER_PART
    _textNode.addChild(_textNode.binding)
    _textNode.addChild(_textNode.coinColor)
    _textNode.coinColor.rgb = labelcolor
    _textNode.fontNode = coin.SoFont()
    _textNode.transNode = coin.SoTransform()
    _textNode.textNode = coin.SoText2()
    _textNode.addChild(_textNode.fontNode)
    _textNode.addChild(_textNode.transNode)
    _textNode.addChild(_textNode.textNode)
    _textNode.font = labelfont
    _textNode.size = size
    _textNode.trans = trans
    _textNode.text = text
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
