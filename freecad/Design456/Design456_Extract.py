# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2025 Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Design456 addon.

from __future__ import unicode_literals

import os ,sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore
import Draft
import Part
import FACE_D as faced
from draftutils.translate import translate   #for translate 

__updated__ = '2021-12-31 08:56:16'

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
