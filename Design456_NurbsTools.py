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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
sys.path.append(Design456Init.NURBS_PATH)

from nurbs import *
import nurbs.NURBSinit
import Design456_ALLNURBS

class Design456_NurbsTools:
    list = ["Design456_Nurbs_List1Group",
            "Design456_Nurbs_List2Group",        
            "Design456_Nurbs_List3Group",
            "Design456_Nurbs_List4Group",
            "Design456_Nurbs_List5Group",
            "Design456_Nurbs_List6Group",
            "Design456_Nurbs_List7Group",
            "Design456_Nurbs_List8Group",
            "Design456_Nurbs_List9Group",
            "Design456_Nurbs_List10Group",
            "Design456_Nurbs_List11Group",
            "Design456_Nurbs_List12Group",
            "Design456_Nurbs_List13Group",
            ]

    """Design456 Part Tools Toolbar"""
    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_NURBS_PATH + 'NURBS.svg',
            'MenuText': 'Nurbs Tools',
            'ToolTip':  'Nurbs Tools'
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if Gui.activeDocument():
            return True
        else:
            return False
        
    def Activated(self):
        self.appendToolbar("Design456_NurbsTools", self.list)
