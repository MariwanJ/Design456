# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *																		    *
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
import sys
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part


class FACE_D:
    def __init__(self, view):
        self.view = view
        v = Gui.activeDocument().activeView()

    def getDirectionAxis(self):
        try:
            s = Gui.Selection.getSelectionEx()
            obj = s[0]
            faceSel = obj.SubObjects[0]
            dir = faceSel.normalAt(0, 0)
            if dir.z == 1:
                return "z"
            elif dir.y == 1:
                return "y"
            else:
                return "x"
        except Exception as err:
            App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def MousePosition(self, info):
        try:
            down = (info["State"] == "DOWN")
            pos = info["Position"]
            # if (down):
            App.Console.PrintMessage(
                "Clicked on position: ("+str(pos[0])+", "+str(pos[1])+")\n")
            pnt = self.view.getPoint(pos)
            App.Console.PrintMessage(
                "World coordinates: " + str(pnt) + "\n")
            info = self.view.getObjectInfo(pos)
            App.Console.PrintMessage("Object info: " + str(info) + "\n")
            o = self.ViewObserver(self.v)
            c = self.v.addEventCallback("SoMouseButtonEvent", o.logPosition)
            return pnt
        except Exception as err:
            App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def ExtractFace(self):
        try:
            s = Gui.Selection.getSelectionEx()
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
            App.ActiveDocument.recompute()
            return self.newobj
        except Exception as err:
            App.Console.PrintError("'FACE_D.ExtractFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


# This class is from A2P WB modified by Mariwan
""" TODO : There is a bug either it is FreeCAD or this class
            The callback is not removed after click. You
            should use twice ESC
"""


class PartMover(object):
    view = obj = None

    def __init__(self, CallerObject, view, obj, deleteOnEscape):
        self.CallerObject = CallerObject
        self.obj = obj
        self.initialPosition = self.obj.Placement.Base
        self.view = view
        self.deleteOnEscape = deleteOnEscape
        self.callbackMove = self.view.addEventCallback(
            "SoLocation2Event", self.moveMouse)
        self.callbackClick = self.view.addEventCallback(
            "SoMouseButtonEvent", self.clickMouse)
        self.callbackKey = self.view.addEventCallback(
            "SoKeyboardEvent", self.KeyboardEvent)
        self.objectToDelete = None  # object reference when pressing the escape key
        # Gui.Selection.clearSelection()
        # Gui.Selection.addSelection(App.ActiveDocument.Name,
        #                           self.CallerObject.Name)

    def Deactivated(self):
        self.removeCallbacks()

    def moveMouse(self, info):
        try:
            newPos = self.view.getPoint(*info['Position'])
            self.obj.Placement.Base = newPos
            self.newPosition = newPos
        except Exception as err:
            App.Console.PrintError("'Mouse movements error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def removeCallbacks(self):
        try:
            print('Remove callback')
            self.view.removeEventCallback(
                "SoLocation2Event", self.callbackMove)
            self.view.removeEventCallback(
                "SoMouseButtonEvent", self.callbackClick)
            self.view.removeEventCallback("SoKeyboardEvent", self.callbackKey)
            App.closeActiveTransaction(True)
            self.active = False
            self.info = None
            self.view = None
        except Exception as err:
            App.Console.PrintError("'remove callback error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def clickMouse(self, info):
        try:
            if (info['Button'] == 'BUTTON1' and
                    info['State'] == 'DOWN'):
                # if not info['ShiftDown'] and not info['CtrlDown']: #struggles within Inventor Navigation
                print('Mouse click \n')
                newPos = self.view.getPoint(*info['Position'])
                self.obj.Placement.Base = newPos
                self.removeCallbacks()
                self.obj = None
                App.ActiveDocument.recompute()
            return
        except Exception as err:
            App.Console.PrintError("'Mouse click error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def KeyboardEvent(self, info):
        try:
            print('Escape pressed\n')
            if info['State'] == 'UP' and info['Key'] == 'ESCAPE':
                self.removeCallbacks()
                if not self.deleteOnEscape:
                    self.obj.Placement.Base = self.initialPosition
                else:
                    # This can be asked by a timer in a calling func...
                    self.objectToDelete = self.obj

                    # This causes a crash in FC0.19/Qt5/Py3
                    # App.activeDocument().removeObject(self.obj.Name)
        except Exception as err:
            App.Console.PrintError("'Keyboard error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


""" This class will return back info about the
    face selected. Many options are available but
    I will put only what I need. See the note bellow for available info
    Give the class Gui.Selection()[nr] where nr is the face you want to get info

TODO: This class must be updated to be able to move all kind of objects
    Mariwan
"""


class getInfo:
    def __init__(self, object):
        self.obj = object

    def getFaceName(self):
        try:
            Result = (self.obj.SubElementNames[0])
            return Result
        except Exception as err:
            App.Console.PrintError("'getFaceName' Failed. "
                                   "{err}\n".format(err=str(err)))

    def getFullFaceName(self):
        try:
            Result = (self.obj.FullName)
            return Result
        except Exception as err:
            App.Console.PrintError("'getFullFaceName' Failed. "
                                   "{err}\n".format(err=str(err)))

    def getObjectCenterOfMass(self):
        try:
            Result = self.obj.SubObjects[0].CenterOfMass
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectCenterOfMass' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectX(self):
        try:
            Result = self.obj.SubObjects[0].CenterOfMass.x
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectX' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectY(self):
        try:
            Result = self.obj.SubObjects[0].CenterOfMass.y
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectY' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectZ(self):
        try:
            Result = self.obj.SubObjects[0].CenterOfMass.z
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectZ' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectBase(self):
        try:
            Result = self.obj.SubObjects[0].Placement.Base()
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectBase' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectPlacement(self):
        try:
            Result = self.obj.SubObjects[0].Placement()
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectPlacement' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectRotation(self):
        try:
            Result = self.obj.SubObjects[0].Placement.Rotation()
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectX' Failed. "
                                   "{err+}\n".format(err=str(err)))

    def getObjectParameterRange(self):
        try:
            Result = self.obj.SubObjects[0].ParameterRange()
            return Result
        except Exception as err:
            App.Console.PrintError("'getObjectParameterRange' Failed. "
                                   "{err+}\n".format(err=str(err)))

    """Message box (error) """

    def errorDialog(self, msg):
        # Create a simple dialog QMessageBox
        # The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question}
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Error', msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

    def SelectTopFace(self):
        t = self.obj
        faceData = None
        counter = 1
        centerofmass = None
        Highiest = 0
        for fac in t.Object.Shape.Faces:
            if(fac.CenterOfMass.z > Highiest):
                Highiest = fac.CenterOfMass.z
                centerofmass = fac.CenterOfMass
                Result = counter
            counter = counter+1
        # Gui.Selection.addSelection('Unnamed','Shape','Face4',-2.45152,-3.78272,5)
        FaceName = 'Face'+str(Result)
        print(FaceName)
        print(Highiest)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(App.ActiveDocument.Name, t.Object.Name,
                                   FaceName, centerofmass.x, centerofmass.y, centerofmass.z)
        return FaceName

    # From Mario Macro_CenterCenterFace at
    # https://wiki.freecadweb.org/Macro_CenterFace/fr
    def objectRealPlacement3D(self):    # search the real Placement
        try:
            objectPlacement = self.obj.Object.Shape.Placement
            objectPlacementBase = App.Vector(objectPlacement.Base)
            ####
            objectWorkCenter = objectPlacementBase
            ####
            if hasattr(self.obj, "getGlobalPlacement"):
                globalPlacement = self.obj.Object.getGlobalPlacement()
                globalPlacementBase = App.Vector(globalPlacement.Base)
                ####
                objectRealPlacement3D = globalPlacementBase.sub(
                    objectWorkCenter)  # mode=0 adapte pour BBox + Centerpoints
                ####
            else:
                objectRealPlacement3D = objectWorkCenter
            return objectRealPlacement3D
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return self.getObjectCenterOfMass()


"""
You can get these infos from obj.SubObjects[0]. which is a face

Area
BoundBox
CenterOfMass
CompSolids
Compounds
Content
Edges
Faces
Length
Mass
Matrix
MatrixOfInertia
MemSize
Module
Orientation
OuterWire
ParameterRange
Placement
PrincipalProperties
ShapeType
Shells
Solids
StaticMoments
SubShapes
Surface
Tag
Tolerance
TypeId
Vertexes
Volume
Wire
Wires
addWire
ancestorsOfType
check
childShapes
cleaned
common
complement
copy
countElement
curvatureAt
curveOnSurface
cut
cutHoles
defeaturing
derivative1At
derivative2At
distToShape
dumpContent
dumpToString
exportBinary
exportBrep
exportBrepToString
exportIges
exportStep
exportStl
extrude
findPlane
fix
fixTolerance
fuse
generalFuse
getAllDerivedFrom
getElement
getFacesFromSubelement
getTolerance
getUVNodes
globalTolerance
hashCode
importBinary
importBrep
importBrepFromString
inTolerance
isClosed
isCoplanar
isDerivedFrom
isEqual
isInfinite
isInside
isNull
isPartOfDomain
isPartner
isSame
isValid
limitTolerance
makeChamfer
makeFillet
makeHalfSpace
makeOffset
makeOffset2D
makeOffsetShape
makeParallelProjection
makePerspectiveProjection
makeShapeFromMesh
makeThickness
makeWires
mirror
multiFuse
normalAt
nullify
oldFuse
optimalBoundingBox
overTolerance
project
proximity
read
reflectLines
removeInternalWires
removeShape
removeSplitter
replaceShape
restoreContent
reverse
reversed
revolve
rotate
rotated
scale
scaled
section
sewShape
slice
slices
tangentAt
tessellate
toNurbs
transformGeometry
transformShape
transformed
translate
translated
validate
valueAt
writeInventor

        """
