# -*- coding: utf-8 -*-
from Design456_2Ddrawing import Design456_2Ddrawing
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

import os,sys
import FreeCAD as App
import FreeCADGui as Gui
import Draft as _draft
import Part as _part
import Design456Init
from pivy import coin
import FACE_D as faced
import math as _math
from PySide.QtCore import QT_TRANSLATE_NOOP

class Design456_SmartScale:

    def getXYZdimOfSelectedObject(self,selected):
        #Max object length in all directions
        lengthX = selected.Shape.BoundBox.XLength
        lengthY =selected.Shape.BoundBox.YLength
        lengthY =selected.Shape.BoundBox.ZLength
        
        #Make the end 10 mm longer/after the object
        NewX= selected.Shape.BoundBox.XMax+10
        NewY= selected.Shape.BoundBox.YMax+10
        NewZ= selected.Shape.BoundBox.ZMax+10
        
        #Make the start 10 mm before the object is placed
        startX= selected.Shape.BoundBox.XMin-10
        startY= selected.Shape.BoundBox.YMin-10
        startZ= selected.Shape.BoundBox.ZMin-10

        
    def Activated(self):
        try:
            sel = Gui.Selection.getSelection()
            if len(sel) != 1:
                # Only one object must be selected
                errMessage = "Select one object to scale"
                faced.getInfo().errorDialog(errMessage)
                return 
        
        # we have a selected object. Try to show the dimentions. 
        except Exception as err:
            App.Console.PrintError("'Design456_SmartScale' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)