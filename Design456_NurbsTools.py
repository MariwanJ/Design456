# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import Nurbs_Miscellaneous
import Nurbs_2DDrawingGroup
import Nurbs_3DDrawingGroup
import Nurbs_2DToolsGroup
import Nurbs_3DToolsGroup
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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
# sys.path.append(Design456Init.NURBS_PATH)
sys.path.append(Design456Init.NURBS_WB_PATH)
# sys.path.append(Design456Init.NURBS_PLOT_PATH)


class Design456_NURBSGroup:
    """Design456 Nurbs Toolbar"""
    list = ["Design456_Nurbs_3DToolsGroup",
            "Design456_Nurbs_2DToolsGroup",
            "Design456_Nurbs_3DDrawingGroup",
            "Design456_Nurbs_2DDrawingGroup",
            # "Separator",
            "Design456_Nurbs_Miscellaneous",

            ]

    def GetResources(self):
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'Design456_Nurbs.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

    def IsActive(self):
        """Return True when this command should be available."""
        if Gui.activeDocument():
            return True
        else:
            return False

    def Activated(self):
        self.appendToolbar("Design456_Part_Tools", self.list)

#Gui.addCommand("Design456_NURBSGroup", Design456_NURBSGroup())