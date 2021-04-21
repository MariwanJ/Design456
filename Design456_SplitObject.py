# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *                                                                         *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************
import os
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import BOPTools.SplitFeatures as SPLIT
from FreeCAD import Base
from time import time as _time, sleep as _sleep
import FACE_D as faced

class Design456_SplitObject:
    """Devide object in to two parts"""

    def Activated(self):
        try:
            # Save object name that will be divided.
            selection = Gui.Selection.getSelectionEx()
            if (len(selection) < 1):
                # An object must be selected
                errMessage = "Select an object to use Split Tool"
                faced.getInfo(selection).errorDialog(errMessage)
                return
            shape = selection[0].Object.Shape
            bb = shape.BoundBox
            length = max(bb.XLength, bb.YLength, bb.ZLength)

            nameOfselectedObject = selection[0].ObjectName
            totalName = nameOfselectedObject+'_cs'

            """ slow function . . you need to use wait before getting 
                the answer as the execution is continuing down """
            Gui.runCommand('Part_CrossSections', 0)
            gcompund = App.ActiveDocument.addObject(
                "Part::Compound", "Compound")

            App.ActiveDocument.recompute()

            # get object name
            # We need this delay to let user choose the split form. And
            getExtrude_cs = None  # Dummy variable used to wait for the Extrude_cs be made
            while (getExtrude_cs is None):
                getExtrude_cs = App.ActiveDocument.getObject(totalName)
                _sleep(.1)
                Gui.updateGui()
            # Begin command Part_Compound
            gcompund.Links = [getExtrude_cs, ]

            # Begin command Part_BooleanFragments
            j = SPLIT.makeBooleanFragments(name='BooleanFragments')
            j.Objects = [gcompund, App.ActiveDocument.getObject(
                nameOfselectedObject)]
            j.Mode = 'Standard'
            j.Proxy.execute(j)
            j.purgeTouched()
            App.ActiveDocument.recompute()
            if j.isValid() == False:
                App.ActiveDocument.removeObject(j.Name)
                # Shape is not OK
                errMessage = "Failed to fillet the objects"
                faced.getInfo(selection).errorDialog(errMessage)
            else:
                # Make a simple copy
                newShape = Part.getShape(j, '', needSubElement=False, refine=False)
                NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'SplitedObject').Shape = newShape
                # Remove Old objects
                for obj in j.Objects:
                    App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(totalName)
                App.ActiveDocument.removeObject(j.Name)

            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'SplitObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + '/SplitObject.svg',
            'MenuText': 'Split Object',
            'ToolTip': 'Divide object in to two parts'
        }


Gui.addCommand('Design456_SplitObject', Design456_SplitObject())
