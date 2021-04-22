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

'''
create a bspline surface over a list of curves
the curves are expected in the clones group

'''


import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit
import Part



class Nurbs_DrawCurves2Face:
    def Activated(self):
        allpts = []
        # for obj in Gui.Selection.getSelectionEx():
        t=""
        for obj in App.ActiveDocument.clones.OutList:
            if obj.Label.startswith('t='):
                exec(obj.Label)
                # print (t)
                # print (y.Placement)
                obj.Placement = t  # .inverse()
    
            print(len(obj.Shape.Edge1.Curve.getPoles()))
            pts = obj.Shape.Edge1.Curve.discretize(30)
            allpts.append(pts)
    
        bs = Part.BSplineSurface()
        bs.interpolate(allpts)
        sp = App.ActiveDocument.addObject("Part::Spline", "Spline")
        sp.Shape = bs.toShape()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_DrawCurves2Face")
        return {'Pixmap':  NURBSinit.ICONS_PATH + 'DrawCurves2Face.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_DrawCurves2Face"),
                'ToolTip': QT_TRANSLATE_NOOP("Nurbs_DrawCurves2Face", _tooltip)}

Gui.addCommand("Nurbs_DrawCurves2Face", Nurbs_DrawCurves2Face())
Nurbs_DrawCurves2Face.__doc__ = """Nurbs Draw Curves to Face: Tobe written later
                            """