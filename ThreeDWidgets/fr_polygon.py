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

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import ThreeDWidgets.fr_widget
import Design456Init
import ThreeDWidgets.fr_draw
import ThreeDWidgets.constant
from typing import List

#


class Fr_Polygon(fr_widget.Fr_Widget):
    # def __init__(self, args:fr_widget.VECTOR=[],l=""):
    def __init__(self, args: List[App.Vector] = [], label: str = "",lineWidth=1):
        if args == None:
            args = []
        self.WidgetType = constant.FR_WidgetType.FR_EDGE
        self.w_lineWidth = lineWidth  # default line width
        super().__init__(args, label)

    def Activated(self):
        raise NotImplementedError()

    def Deactivate(self):
        raise NotImplementedError()

    def draw(self, vectors):
        mynormal = coin.SoNormal
        mynormal.vector.set1Values(0, 8, norms)
        
