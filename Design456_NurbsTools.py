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

# import nurbs.analyse_topology_v2
# import nurbs.apply_labeled_placement
# import nurbs.approximator
# import nurbs.berings
# import nurbs.blender_grid
# import nurbs.configuration
# import nurbs.controlpanel
# import nurbs.createbitmap
# import nurbs.createcloverleaf
# import nurbs.createshoerib
# import nurbs.createsketchspline
# import nurbs.create_sole_sketch
# import nurbs.curvedistance
# import nurbs.curves
# import nurbs.curves2face
# import nurbs.datatools
# import nurbs.demoshapes
# import nurbs.DraftBSplineEditor
# import nurbs.dynamicoffset
# import nurbs.facedraw
# import nurbs.facedraw_segments
# import nurbs.feedbacksketch
# import nurbs.fem_edgelength_mesh
# import nurbs.filledface
# import nurbs.folding
# import nurbs.gen_random_dat
# import nurbs.geodesic_lines
# import nurbs.GuiWBDef
# import nurbs.helmet
# import nurbs.helper
# import nurbs.holes
# import nurbs.isodraw
# import nurbs.isomap
# import nurbs.knotsandpoles
# import nurbs.load_sole_profile_height
# import nurbs.load_sole_profile_width
# import nurbs.loft_selection
# import nurbs.mesh_generator
# import nurbs.miki
# import nurbs.miki_g
# import nurbs.monitor
# import nurbs.morpher
# import nurbs.move_along_curve
# import nurbs.multiedit
# import nurbs.needle
# import nurbs.needle_change_model
# import nurbs.needle_cmds
# import nurbs.needle_models
# import nurbs.nurbs
# import nurbs.nurbsGUI
# import nurbs.nurbs_dialog
# import nurbs.nurbs_tools
# import nurbs.orderpoints
# import nurbs.param_bspline
# import nurbs.patch
# import nurbs.pattern_v2
# import nurbs.Plot2
# import nurbs.points
# import nurbs.points_to_face
# import nurbs.project_edge2face
# import nurbs. pyob
# import nurbs.removeknot
# import nurbs.say
# import nurbs.scanbackbonecut
# import nurbs.scancut
# import nurbs.sculpter
# import nurbs.segment
# import nurbs.shoe
# import nurbs.shoedata
# import nurbs.shoe_importSVG
# import nurbs.shoe_tools
# import nurbs.simplecurve
# import nurbs.simplehood
# import nurbs.skdriver
# import nurbs.sketchclone
# import nurbs.sketcher_grids
# import nurbs.sketchmanager
# import nurbs.sketch_to_bezier
# import nurbs.smooth
# import nurbs.sole
# import nurbs.sole_change_model
# import nurbs.sole_models
# import nurbs.spreadsheet_lib
# import nurbs.tangentsurface
# import nurbs.transform_spline
# import nurbs.tripod_2
# import nurbs.unroll_curve
# import nurbs.uvgrid_generator
# import nurbs.views
# import nurbs.weighteditor
# import nurbs.wheel_event

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
