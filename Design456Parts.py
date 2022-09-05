# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft 
import Part 
import FACE_D as faced
from draftutils.translate import translate   #for translate

import BasicShapes.CommandShapes
import CompoundTools._CommandExplodeCompound

import Design456Parts1
import Design456Parts2
import Design456Parts3
import Design456Init

sys.path.append(Design456Init.PYRAMID_PATH)

__updated__ = '2022-08-13 16:21:26'

class Design456Part:
    import polyhedrons
    list = ["Design456Part_Box",
            "Design456Part_Cylinder",
            "Design456Part_Tube",
            "Design456Part_Sphere",
            "Design456Part_Cone",
            "Design456Part_Torus",
            "Design456Part_Wedge",
            "Design456Part_Prism",
            "Design456Part_Pyramid",
            "Design456Part_Hemisphere",
            "Design456Part_Ellipsoid",
            "Pyramid",
            "Tetrahedron",
            #"Hexahedron",               #No need for this as box is in part.
            "Octahedron",
            "Dodecahedron",
            "Icosahedron",
            "Icosahedron_truncated",
            "Geodesic_sphere",
            "Design456_Seg_Sphere",
            "Design456_Seg_Cylinder", 
            "Design456_Seg_Roof", 
            "Design456_RoundRoof",
            "Design456_Paraboloid", 
            "Design456_Capsule", 
            "Design456_Parallelepiped", 
            "Design456_Housing", 
            "Design456_RoundedHousing", 
            "Design456_EllipseBox", 
            "Design456_NonuniformedBox",
            "Design456_FlowerVase",
            "Design456_CorrugatedSteel",
            "Design456_AcousticFoam",  
            "Design456_Grass",
            "Design456_HoneycombCylinder",
            "Design456_HoneycombFence",
            "Design456_PenHolder",     
            "Design456_Pumpkin",
            "Design456_Fence"
            ]

    """Design456 Part Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'Part_Box.svg',
            'MenuText': 'Box',
                        'ToolTip': 'Box'
        }

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True
        