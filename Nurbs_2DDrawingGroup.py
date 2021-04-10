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
import Design456Init
#sys.path.append(Design456Init.NURBS_PATH)
sys.path.append(Design456Init.NURBS_WB_PATH)
#sys.path.append(Design456Init.NURBS_PLOT_PATH)

import create_sole_sketch

class Design456_Nurbs_2DDrawingGroup:

    """Design456 Part 2D Drawing"""

    def GetCommands(self):
        """3D Modifying Tools."""
        return ("runSole",
                #These are from the WB definition of Nurbs.
                #From cmds --> i.e. cmd1  : defined in his wb as Nurbs toolbar
                'ZebraTool','ParametricComb','GeomInfo','Nurbs_DraftBSpline Editor',
                'Nurbs_Create Shoe','Nurbs_Create Sole','Nurbs_Sole Change Model',
                'Nurbs_scanbackbonecut','Nurbs_createsketchspline','Nurbs_Curves to Face', 'Nurbs_facedraw',

                'Part_Cone', 'Part_Cylinder','Draft_Move','Draft_Rotate','Draft_Point','Draft_ToggleGrid',
                'My_Test2','Sketcher_NewSketch',
                'Nurbs_facedraws','Nurbs_patcha','Nurbs_patchb','Nurbs_folda',# WAS COMMENTED
                
                #from cmd2
                'Nurbs_facedraw','Nurbs_patcha','Nurbs_patchb','Nurbs_folda',
                #from cmd4  defined in his WB as "Points Workspaces and Views"
                'Nurbs_pta','Nurbs_ptb','Nurbs_ptc','Nurbs_ptd','Nurbs_pte',
                #from cmd5 
                'Nurbs_geodesic1','Nurbs_geodesic2','Nurbs_geodesic3','Nurbs_geodesic4','Nurbs_geodesic5','Nurbs_geodesic6',
                #from cmd5 nextline defined i his WB as "Geodesic Patch Tests"
                'Nurbs_multiEdit', 'Nurbs_AA','Nurbs_BB' 


                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  Design456Init.NURBS_ICON_PATH + 'Nurbs1.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsTools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_2DDrawingGroup", Design456_Nurbs_2DDrawingGroup())