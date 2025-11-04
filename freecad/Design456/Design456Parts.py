# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2025 Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Design456 addon.

from __future__ import unicode_literals

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
import Design456_Fence
import Design456Init

sys.path.append(Design456Init.PYRAMID_PATH)

__updated__ = '2022-09-30 21:51:55'

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
        