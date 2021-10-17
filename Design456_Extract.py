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
import os ,sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore
import Draft
import Part
import FACE_D as faced
from draftutils.translate import translate   #for translate 

class Design456_Extract:
    """Extract the selected face from the object"""

    def Activated(self):
        try:
            objectCreate=False
            newobj=None
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # An object must be selected
                errMessage = "Select a face from an object to use Extract"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Extract a Face"))
            for o in s:
                objName = o.ObjectName
                sh = o.Object.Shape.copy()
                if hasattr(o.Object, "getGlobalPlacement"):
                    gpl = o.Object.getGlobalPlacement()
                    sh.Placement = gpl
                for name in o.SubElementNames:
                    fullname = objName+"_"+name
                    newobj = o.Document.addObject("Part::Feature", fullname)
                    newobj.Shape = sh.getElement(name)
                    objectCreate=True
            App.ActiveDocument.commitTransaction()
            App.ActiveDocument.recompute()
            if  newobj.isValid()==False:
                if objectCreate==True:
                    App.ActiveDocument.removeObject(newobj.Name)
                # Shape != OK
                errMessage = "Failed to extract the face"
                faced.errorDialog(errMessage)
                return
        except Exception as err:
            App.Console.PrintError("'Design456_Extract' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH +'Extract.svg',
            'MenuText': 'Extract',
            'ToolTip': 'Extract selected face from the object'
        }


Gui.addCommand('Design456_Extract', Design456_Extract())
