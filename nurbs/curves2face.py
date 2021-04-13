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
import Part

import Design456Init
def run():
    allpts = []
    # for obj in Gui.Selection.getSelection():

    for obj in App.ActiveDocument.clones.OutList:
        if obj.Label.startswith('t='):
            exec(obj.Label)
            # print t
            # print y.Placement
            obj.Placement = t  # .inverse()

        print(len(obj.Shape.Edge1.Curve.getPoles()))
        pts = obj.Shape.Edge1.Curve.discretize(30)
        allpts.append(pts)

    bs = Part.BSplineSurface()
    bs.interpolate(allpts)
    sp = App.ActiveDocument.addObject("Part::Spline", "Spline")
    sp.Shape = bs.toShape()
