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
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit



class Nurbs_ApplyLabeledPlacement:
    
    def Activated(self):
        ''' auxiliary method applies placement from the label,
        to move objects (sketch) to the desired place in the room'''

        for y in Gui.Selection.getSelection():
            if y.Label.startswith('t='):
                exec(y.ObjectName)
                print(t)
                print(y.Placement)
                y.Placement = t  # .inverse()       #t is undefined .. what is this? Mariwan

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs Apply Labeled Placement")
        return {'Pixmap': NURBSinit.ICONS_PATH+'drawing.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_ApplyLabeledPlacement"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456  Nurbs_ApplyLabeledPlacement", _tooltip)}


Gui.addCommand("Nurbs_ApplyLabeledPlacement", Nurbs_ApplyLabeledPlacement())
