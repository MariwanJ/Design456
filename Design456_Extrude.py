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
# ***************************************************************************
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore
import Draft
import Part
import FACE_D as faced
from time import time as _time, sleep as _sleep
from draftutils.translate import translate  # for translation
import math

__updated__ = '2022-01-25 20:08:11'


class Design456_Extrude:

    def ExtractFace(self, Tobj=None):
        try:
            if TObj is None:
                sh = self.selectedObj[0].SubObjects[0].copy()
            else:
                sh = Tobj.SubObjects[0].copy()
            fullname = "ExtractedFace"
            newobj = s[0].Document.addObject("Part::Feature", fullname)
            newobj.Shape = sh
            App.ActiveDocument.recompute()
            return newObj  # Extracted Face.

        except Exception as err:
            App.Console.PrintError("'ExtrudeFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        try:
            self.selectedObj = Gui.Selection.getSelectionEx()
            if (len(self.selectedObj) < 1):
                # An object must be selected
                errMessage = "Select a face to use Extrude"
                faced.errorDialog(errMessage)
                return
            AllObjects = []
            if len(self.selectedObj) == 1:
                # It is only one object. But might have different faces
                if (self.selectedObj[0].HasSubObjects):
                    # Here it can be a face with multiple faces
                        # Or a 3D object with multiple faces?
                        AllObjects =self.selectedObj[0].SubObjects
                else:
                    # Only One object that doesn't have subobjects
                    if isinstance(self.selectedObj[0].Object.Shape, Part.Face):
                        # It is a face. i.e. the object itself is a face only
                        AllObjects = [self.selectedObj[0]]
                    else:
                        # It is a face of a 3D object
                        AllObjects = [self.ExtractFace()]
            else:
                # We have multiple objects selected. Could be faces, 3D objects
                # or mixed
                for obj in self.selectedObj:
                    if (obj.HasSubObjects):
                        # Here it can be a face with multiple faces
                            # Or a 3D object with multiple faces?
                        for nobj in obj.subObjects:
                            if type(nobj) == Part.Face:
                                AllObjects.append(nobj)
                    else:
                        # Only One object that doesn't have subobjects
                        if isinstance(obj.Object.Shape, Part.Face):
                            # It is a face. i.e. the object itself is a face only
                            AllObjects.append(obj)
                        else:
                            # It is a face of a 3D object
                            AllObjects.append(self.ExtractFace(obj))
            self.ExtrudeFace( AllObjects)
            
        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb=sys.exc_info()
            fname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def ExtrudeFace(self, allObjects):
        try:
            print("allObjects",allObjects)
            extrusionLength=-(QtGui.QInputDialog.getDouble(
                    None, "Extrusion Length", "Length:", 0, -10000.0, 10000.0, 2)[0])
            while(extrusionLength == 0):
                _sleep(.1)
                Gui.updateGui()
            
            for obj in allObjects: 
                App.ActiveDocument.openTransaction(
                    translate("Design456", "Extrude"))
                m=obj
                f=App.ActiveDocument.addObject(
                    'Part::Extrusion', 'ExtrudeOriginal')
                print(m,type(m))
                f.Base=m
                # F.DirMode causes too many failure. Some faces needs custom, other needs Normal.
                # Difficult to know when you use each of them.
                f.DirMode="Normal"  
                f.DirLink=None  # Above statement != always correct. Some faces require 'custom'
                # Extrude must get a negative number ???
                
                f.LengthFwd=extrusionLength
                f.LengthRev=0.0
                f.Solid=True
                f.Reversed=False
                f.Symmetric=False
                f.TaperAngle=0.0
                f.TaperAngleRev=0.0
                # section direction
                yL=m.Shape.Faces[0].CenterOfMass
                uv=m.Shape.Faces[0].Surface.parameter(yL)
                nv=m.Shape.Faces[0].normalAt(uv[0], uv[1])
                direction=yL.sub(nv + yL)
                direction=App.Vector(round(direction.x, 2), round(
                    direction.y, 2), round(direction.z, 2))
                f.Dir=direction
                print(direction, "direction")
                r=App.Rotation(App.Vector(0, 0, 0), direction)
                f.Dir=direction
                if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                    f.DirMode="Custom"
                # Make a simple copy of the object
                App.ActiveDocument.recompute()
                newShape=Part.getShape(
                    f, '', needSubElement=False, refine=False)
                newObj=App.ActiveDocument.addObject(
                    'Part::Feature', 'Extrude').Shape=newShape
                App.ActiveDocument.recompute()
                # if something went wrong .. delete all new objects.
                if newObj.isValid() is False:
                    App.ActiveDocument.removeObject(newObj.Name)
                    App.ActiveDocument.removeObject(f.Name)
                    # Shape != OK
                    errMessage="Failed to extrude the shape"
                    faced.getInfo(m).errorDialog(errMessage)
                else:
                    # Remove old objects
                    # App.ActiveDocument.clearUndos()
                    App.ActiveDocument.recompute()
                    App.ActiveDocument.removeObject(f.Name)
                    App.ActiveDocument.removeObject(m.Name)
                    return
                App.ActiveDocument.commitTransaction()  # undo reg.
                App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb=sys.exc_info()
            fname=os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Extrude.svg',
            'MenuText': 'Extrude',
                        'ToolTip':  'Extrude'
        }


Gui.addCommand('Design456_Extrude', Design456_Extrude())
