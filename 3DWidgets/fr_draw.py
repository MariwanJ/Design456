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
import Design456Init

#draw a line in 3D world
def draw_line(p1, p2,color,LineWidth):
    try:
        dash = coin.SoSeparator()
        v = coin.SoVertexProperty()
        v.vertex.set1Value(0, p1)
        v.vertex.set1Value(1, p2)
        line = coin.SoLineSet()
        line.vertexProperty = v
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        dash.addChild(style)
        col1= coin.SoBaseColor()  #must be converted to SoBaseColor
        col1.rgb=color
        dash.addChild(col1)
        dash.addChild(line)
        return dash
    
    except Exception as err:
        App.Console.PrintError("'makeIt' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        
# Draw a square 3D World
def draw_square(p1, p2,p3,p4,color,LineWidth):
    try:
        dash = coin.SoSeparator()
        v = coin.SoVertexProperty()
        square = coin.SbBox3f(p1,p2,p3,p4)
        square.vertexProperty = v
        style = coin.SoDrawStyle()
        style.lineWidth = LineWidth
        dash.addChild(style)
        dash.addChild(color)
        dash.addChild(square)
        return draw_square

    except Exception as err:
        App.Console.PrintError("'makeIt' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        