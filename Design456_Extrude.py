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

__updated__ = '2022-05-26 22:35:47'


class Design456_Extrude:

    def ExtractFace(self, nTObj=None):
        try:
            newlistObj = []
            newObj = None
            if nTObj is None:
                fullname = "ExtractedFace"
                newObj = App.ActiveDocument.addObject(
                    "Part::Feature", fullname)
                if (self.selectedObj[0].HasSubObjects):
                    newObj.Shape = self.selectedObj[0].SubObjects[0].copy()
                else:
                    #We have the whole object selected, take all faces and return a list
                    xx = 0
                    for obj in self.selectedObj[0].Object.Shape.Faces:
                        fullname = "Face"+str(xx)
                        xx = xx+1
                        newObj = App.ActiveDocument.addObject(
                            "Part::Feature", fullname)
                        newObj.Shape = obj.copy()
                        App.ActiveDocument.recompute()
                        newlistObj.append(newObj)  # Extracted Face.
                        return newlistObj
                App.ActiveDocument.recompute()
                return newObj
            else:
                print(type(nTObj))
                if type(nTObj) != list and type(nTObj) != tuple:
                    TObj = [nTObj]
                else:
                    TObj = nTObj
                xx = 0
                for obj in TObj:
                    fullname = "Face"+str(xx)
                    xx = xx+1
                    newObj = App.ActiveDocument.addObject(
                        "Part::Feature", fullname)
                    newObj.Shape = obj.copy()
                    App.ActiveDocument.recompute()
                    newlistObj.append(newObj)  # Extracted Face.
                return newlistObj

        except Exception as err:
            App.Console.PrintError("'Extract Face' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        try:
            AllObjects = []
            self.extrusionLength = -(QtGui.QInputDialog.getDouble(
                None, "Extrusion Length", "Length:", 0, -10000.0, 10000.0, 2)[0])
            if self.extrusionLength == 0.0:
                return

            self.selectedObj = Gui.Selection.getSelectionEx()
            if (len(self.selectedObj) < 1):
                # An object must be selected
                errMessage = "Select a face to use Extrude"
                faced.errorDialog(errMessage)
                return
            if len(self.selectedObj) == 1:
                # It is only one object. But might have different faces
                if (self.selectedObj[0].HasSubObjects):
                    # Here it can be a face with multiple faces
                    # Or a 3D object with multiple faces?
                    result = self.selectedObj[0].SubObjects
                    AllObjects = self.ExtractFace(result)
                else:
                    # Only One object that doesn't have subobjects
                    if isinstance(self.selectedObj[0].Object.Shape, Part.Face):
                        # It is a face. i.e. the object itself is a face only
                        AllObjects = [self.selectedObj[0].Object]
                    else:
                        # It is a face of a 3D object
                        _nResult= self.ExtractFace()
                        if type(_nResult)==list:
                            AllObjects=_nResult
                        else:    
                            AllObjects = [_nResult]
            else:
                # We have multiple objects selected. Could be faces, 3D objects
                # or mixed
                result = []
                result.clear()
                for i in range(0, len(self.selectedObj)):
                    _obj = self.selectedObj[i]
                    if (hasattr(_obj, "HasSubObjects")):
                        if(_obj.HasSubObjects):
                            for nobj in _obj.SubObjects:
                                if type(nobj) == Part.Face:
                                    result.append(nobj)
                        else:
                            result.append(_obj)
                AllObjects = self.ExtractFace(result)
            self.ExtrudeFace(AllObjects)
        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def ExtrudeFace(self, allObjects):
        try:
            for obj in allObjects:
                App.ActiveDocument.openTransaction(
                    translate("Design456", "Extrude"))
                m = obj
                f = App.ActiveDocument.addObject(
                    'Part::Extrusion', 'ExtrudeOriginal')
                # section direction
                yL = m.Shape.Faces[0].CenterOfMass
                uv = m.Shape.Faces[0].Surface.parameter(yL)
                nv = m.Shape.Faces[0].normalAt(uv[0], uv[1])
                direction = yL.sub(nv + yL)
                direction = App.Vector(round(direction.x, 2), round(
                    direction.y, 2), round(direction.z, 2))
                f.Dir = direction
                f.Base = m
                # F.DirMode causes too many failure. Some faces needs custom, other needs Normal.
                # Difficult to know when you use each of them.
                if (f.Dir.x != 1 or f.Dir.y != 1 or f.Dir.z != 1):
                    f.DirMode = "Custom"
                else:
                    f.DirMode = "Normal"
                f.DirLink = None  # Above statement != always correct. Some faces require 'custom'
                f.LengthFwd = self.extrusionLength
                f.LengthRev = 0.0
                f.Solid = True
                f.Reversed = False
                f.Symmetric = False
                f.TaperAngle = 0.0
                f.TaperAngleRev = 0.0
                r = App.Rotation(App.Vector(0, 0, 0), direction)
                f.Dir = direction

                # Make a simple copy of the object
                App.ActiveDocument.recompute()
                newShape = Part.getShape(
                    f, '', needSubElement=False, refine=False)
                newObj = App.ActiveDocument.addObject(
                    'Part::Feature', 'Extrude')
                newObj.Shape = newShape
                App.ActiveDocument.recompute()
                # if something went wrong .. delete all new objects.
                if newObj.isValid() is False:
                    App.ActiveDocument.removeObject(newObj.Name)
                    App.ActiveDocument.removeObject(f.Name)
                    # Shape != OK
                    errMessage = "Failed to extrude the shape"
                    faced.errorDialog(errMessage)
                else:
                    App.ActiveDocument.recompute()
                    App.ActiveDocument.removeObject(f.Name)
                    App.ActiveDocument.removeObject(m.Name)
            App.ActiveDocument.commitTransaction()  # undo reg.
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Extrude.svg',
            'MenuText': 'Extrude',
                        'ToolTip':  'Extrude'
        }

Gui.addCommand('Design456_Extrude', Design456_Extrude())
