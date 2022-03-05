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
import sys
import FreeCAD as App
import FreeCADGui as Gui
import Part
from pivy import coin
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
from typing import List
import math

#if 0:
#    import OCC
#    
#    from OCC.Core import BRepTools
#    from OCC.Core.BOPAlgo import BOPAlgo_RemoveFeatures as rf
#    from OCC.Core.ShapeFix import ShapeFix_Shape,ShapeFix_FixSmallSolid  

__updated__ = '2022-03-05 22:04:40'

# TODO : FIXME BETTER WAY?
def getDirectionAxis(s=None):
    """[Get Direction of the selected face/Edge]

    Raises:
        Exception: [description]
        NotImplementedError: [description]
        Exception: [description]

    Returns:
        [str]: [Returns +x,-x,+y,-y,+z,-z]
    """
    try:
        if s is None:
            s = Gui.Selection.getSelectionEx()

        if len(s) == 0:
            print("Nothing was selected")
            return ""  # nothing to do we cannot calculate the direction
        obj = s[0]
        faceSel = None
        if (hasattr(obj, "SubObjects")):

            if len(obj.SubObjects) != 0:
                if (len(obj.SubObjects[0].Faces) == 0):
                    # it is an edge not a face:
                    f = findFacehasSelectedEdge()
                    if f is None:
                        raise Exception("Face not found")
                    faceSel = f
                else:
                    faceSel = obj.SubObjects[0]
            else:
                faceSel = obj.Object.Shape.Faces[0]  # Take the first face
        else:
            raise NotImplementedError
        try:
            direction = faceSel.normalAt(0, 0)  # other faces needs 2 arguments
        except:
            try:
                # Circle has not two arguments, only one
                direction = faceSel.normalAt(0)
            except:
                ftt = findFacehasSelectedEdge()
                if ftt is None:
                    raise Exception("Face not found")
                direction = ftt.normalAt(0, 0)

        if direction.z == 1:
            return "+z"
        elif direction.z == -1:
            return "-z"
        elif direction.y == 1:
            return "+y"
        elif direction.y == -1:
            return "-y"
        elif direction.x == 1:
            return "+x"
        elif direction.x == -1:
            return "-x"
        else:
            # We have an axis that != 1,0:
            if(abs(direction.x) == 0):
                return "+z"
            elif (abs(direction.y) == 0):
                return "+z"
            elif (abs(direction.z) == 0):
                return "+x"
            else:
                return "+z"  # this is to avoid having NONE .. Don't know when this happen TODO: FIXME!

    except Exception as err:
        App.Console.PrintError("'getDirectionAxis' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


# TODO: This might be wrong


class mousePointMove:

    def __init__(self, obj, view):
        self.obj = obj
        self.view = view
        self.callbackClicked = self.view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.mouseClick)  # "SoLocation2Event"
        self.callbackMove = self.view.addEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.mouseMove)
        self.direction = 'A'

    def convertToVector(self, pos):
        try:
            import Design456Init
            point = None
            tempPoint = self.view.getPoint(pos[0], pos[1])
            print(Design456Init.DefaultDirectionOfExtrusion ,"Design456Init.DefaultDirectionOfExtrusion")
            if Design456Init.DefaultDirectionOfExtrusion == 'x':
                point = App.Vector(0.0, tempPoint[1], tempPoint[2])
            elif Design456Init.DefaultDirectionOfExtrusion == 'y':
                point = App.Vector(tempPoint[0], 0.0, tempPoint[2])
            elif Design456Init.DefaultDirectionOfExtrusion == 'z':
                point = App.Vector(tempPoint[0], tempPoint[1], 0.0)
            else:
                point = tempPoint
            return point

        except Exception as err:
            App.Console.PrintError("'converToVector' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def mouseMove(self, events):
        try:
            event = events.getEvent()
            pos = event.getPosition().getValue()
            self.obj.Object.End = self.convertToVector(pos)
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Extend' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def mouseClick(self, events):
        try:
            event = events.getEvent()
            eventState = event.getState()
            getButton = event.getButton()
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                pos = event.getPosition()
                point = self.convertToVector(pos)
                _point = self.obj.Object.Points
                _point[len(_point) - 1] = point
                # self.obj.Object.End= point
                App.ActiveDocument.recompute()
                self.remove_callbacks()

        except Exception as err:
            App.Console.PrintError("'converToVector' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        except Exception as err:
            App.Console.PrintError("'Mouse click ' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return None

    def remove_callbacks(self):
        try:
            print('Remove Mouse callback')
            self.view.removeEventCallbackPivy(
                coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClicked)
            self.view.removeEventCallbackPivy(
                coin.SoLocation2Event.getClassTypeId(), self.callbackMove)

        except Exception as err:
            App.Console.PrintError("'Mouse move point' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class PartMover:

    def __init__(self, view, obj, deleteOnEscape):
        self.obj = obj
        self.initialPosition = self.obj.Placement.Base
        self.view = view
        self.deleteOnEscape = deleteOnEscape
        self.callbackMove = self.view.addEventCallbackPivy(
            coin.SoLocation2Event.getClassTypeId(), self.moveMouse)
        self.callbackClick = self.view.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.MouseClick)
        self.callbackKey = self.view.addEventCallbackPivy(
            coin.SoKeyboardEvent.getClassTypeId(), self.KeyboardEvent)
        self.objToDelete = None  # when pressing the escape key
        self.Direction = 'A'

    def convertToVector(self, pos):
        try:
            import Design456Init
            tempPoint = self.view.getPoint(pos[0], pos[1])
            tempPoint = [int(tempPoint[0]),
                         int(tempPoint[1]),
                         int(tempPoint[2])]
            if(self.Direction == 'A'):
                if Design456Init.DefaultDirectionOfExtrusion == 'x':
                    point = (App.Vector(0.0, tempPoint[1], tempPoint[2]))
                elif Design456Init.DefaultDirectionOfExtrusion == 'y':
                    point = (App.Vector(tempPoint[0], 0.0, tempPoint[2]))
                elif Design456Init.DefaultDirectionOfExtrusion == 'z':
                    point = (App.Vector(tempPoint[0], tempPoint[1], 0.0))
            else:
                if (self.Direction == 'X'):
                    point = (App.Vector(
                        tempPoint[0], self.obj.Placement.Base.y, self.obj.Placement.Base.z))
                elif (self.Direction == 'Y'):
                    point = (App.Vector(self.obj.Placement.Base.x,
                             tempPoint[1], self.obj.Placement.Base.z))
                elif (self.Direction == 'Z'):
                    point = (App.Vector(self.obj.Placement.Base.x,
                             self.obj.Placement.Base.y, tempPoint[2]))
            return point

        except Exception as err:
            App.Console.PrintError("'Mouse click error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def moveMouse(self, events):
        try:
            event = events.getEvent()
            self.newPosition = self.convertToVector(
                event.getPosition().getValue())
            if self.newPosition is not None:
                self.obj.Placement.Base = self.newPosition

        except Exception as err:
            App.Console.PrintError("'Mouse movements error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def remove_callbacks(self):
        try:
            print('Remove callback')
            self.view.removeEventCallbackPivy(
                coin.SoLocation2Event.getClassTypeId(), self.callbackMove)
            self.view.removeEventCallbackPivy(
                coin.SoMouseButtonEvent.getClassTypeId(), self.callbackClick)
            self.view.removeEventCallbackPivy(
                coin.SoKeyboardEvent.getClassTypeId(), self.callbackKey)
            self.view = None

        except Exception as err:
            App.Console.PrintError("'remove callback error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def MouseClick(self, events):
        try:
            event = events.getEvent()
            eventState = event.getState()
            getButton = event.getButton()
            if eventState == coin.SoMouseButtonEvent.DOWN and getButton == coin.SoMouseButtonEvent.BUTTON1:
                pos = event.getPosition()
                self.obj.Placement.Base = self.convertToVector(pos)
                self.remove_callbacks()
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

    def KeyboardEvent(self, events):
        try:
            event = events.getEvent()
            eventState = event.getState()
            if (type(event) == coin.SoKeyboardEvent):
                key = event.getKey()

            if key == coin.SoKeyboardEvent.X and eventState == coin.SoButtonEvent.UP:
                self.Direction = 'X'
            if key == coin.SoKeyboardEvent.Y and eventState == coin.SoButtonEvent.UP:
                self.Direction = 'Y'
            if key == coin.SoKeyboardEvent.Z and eventState == coin.SoButtonEvent.UP:
                self.Direction = 'Z'
            if key == coin.SoKeyboardEvent.ESCAPE and eventState == coin.SoButtonEvent.UP:
                if not self.deleteOnEscape:
                    self.obj.Placement.Base = self.initialPosition
                self.remove_callbacks()

        except Exception as err:
            App.Console.PrintError("'Keyboard error' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


def getFaceName(sel):
    try:
        if(hasattr(sel, 'SubElementNames')):
            Result = (sel.SubElementNames[0])
            return Result
        else:
            return None
    except Exception as err:
        App.Console.PrintError("'getFaceName' Failed. "
                               "{err}\n".format(err=str(err)))


def getObjectFromFaceName(obj, face_name):
    try:
        faceName = face_name
        if(obj.SubElementNames[0].startswith('Face')):
            faceNumber = int(faceName[4:]) - 1
        return obj.Object.Shape.Faces[faceNumber]

    except Exception as err:
        App.Console.PrintError("'getObjectFromFaceName' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def errorDialog(msg):
    # Create a simple dialog QMessageBox
    # The first argument indicates the icon used:
    # one of QtGui.QMessageBox.{NoIcon, Information,
    # Warning, Critical, Question}
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Error', msg)
    diag.setWindowModality(QtCore.Qt.ApplicationModal)
    diag.exec_()


class SelectTopFace:

    def __init__(self, obj):
        self.obj = obj
        self.name_facename = ""

    def Activated(self):
        try:
            if self.obj is None:

                return
            counter = 1
            centerofmass = None
            Highest = 0
            Result = 0
            for fac in self.obj.Shape.Faces:
                if(fac.CenterOfMass.z > Highest):
                    Highest = fac.CenterOfMass.z
                    centerofmass = fac.CenterOfMass
                    Result = counter
                counter = counter + 1
            self._facename = 'Face' + str(Result)
            if centerofmass is None:
                #TODO: FIXME: Don't know when this happens
                return
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(App.ActiveDocument.Name, self.obj.Name,
                                       self._facename, centerofmass.x, centerofmass.y, centerofmass.z)
            return self._facename
        except Exception as err:
            App.Console.PrintError("'SelectTopFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


class GetInputValue:
    def __init__(self):
        self.value = 0.0
    """
    get Input value from user. Either Text, INT or Float
    """

    def getIntValue(self):
        valueDouble, ok = (QtGui.QInputDialog.getInt(
            None, "Input new Value", "Change size:", self.value, -10000, 10000))
        if ok:
            return float(valueDouble)
        else:
            return None

    def getTextValue(self):
        text, ok = QtGui.QInputDialog.getText(
            None, 'Input new Value', 'Change size:')
        if ok:
            return str(text)
        else:
            return None

    def getDoubleValue(self):
        valueDouble, ok = (QtGui.QInputDialog.getDouble(
            None, 'Input new Value', 'Change size:', self.value, -10000.0, 10000.0, 2))
        if ok:
            return float(valueDouble)
        else:
            return None

    def Activated(self):
        text, ok = QtGui.QInputDialog.getText(
            None, 'Input new Value', 'Change size')
        if ok:
            return str(text)
        else:
            return None

# Visual progress indicator


class StatusBarProgress:
    """
    Visual progress indicator. 
    Use this class to visually show the progress 
    of a process you are implementing. 
    Or it could be used also with Wizard widget
    as step indicator
    Use stop to stop the progress. 
    Use stepUp   to step Up   the progress indicator
    Use stepDown to step down the progress indicator
    """

    def __init__(self, title="", Steps=10):
        self.ProgressTitle = title
        self.NoOfsteps = Steps
        self.progress_bar = None

    def Activated(self):
        self.progress_bar = App.Base.ProgressIndicator()

    def start(self):
        self.progress_bar.start(self.ProgressTitle, 9)

    def stepUp(self):
        self.progress_bar.next()

    def stepDown(self):
        self.progress_bar.prev()

    def stopProgress(self):
        self.progress_bar.stop()


class createActionTab:

    def __init__(self, Title):
        self.title = Title
        self.mw = None
        self.dw = None
        self.dialog = None

    def Activated(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                self.mw = i
        if self.mw is None:

            raise Exception("No main window found")
        dw = self.mw.findChildren(QtGui.QDockWidget)
        for i in dw:
            if str(i.objectName()) == "Combo View":
                self.tab = i.findChild(QtGui.QTabWidget)
            elif str(i.objectName()) == "Python Console":
                self.tab = i.findChild(QtGui.QTabWidget)
        if self.tab is None:
            raise Exception("No tab widget found")
        self.dialog = QtGui.QDialog()
        #oldsize = self.tab.count()
        self.tab.addTab(self.dialog, self.title)

        self.tab.setCurrentWidget(self.dialog)
        self.dialog.setWindowTitle(self.title)
        return (self.mw, self.dialog, self.tab)


def findnormalAtforEdge():
    """[Find Directions of an edge]

    Returns:
        [(float,float,float)]: [Returns the results
        of normalAt for the faces 
        containing the edge.]
    """
    results = []
    for f in findFacehasSelectedEdge():
        u0, u1, v0, v1 = f.ParameterRange
        results.append(f.normalAt(0.5 * (u0 + u1), 0.5 * (v0 + v1)))
    return results


def distanceBetweenTwoVectors(p1=App.Vector(0, 0, 0), p2=App.Vector(10, 10, 10), n=App.Vector(0, 0, 1)):
    """[Measure the distance between two points,
        first point is optional if not provided,
        the function will measure the distance to origin ]

    Args:
        p1 ([FreeCAD.Vector], optional): [description]. Defaults to App.Vector(0.0, 0.0, 0.0).
        p2 ([FreeCAD.Vector], Required): [description]. Defaults to App.Vector(10,10,10).

    Returns:
        [float]: [Deistance measured between the two vertices]
    """
    results = (p2 - p1).dot(n)  # p1.distanceToPoint(p2)
    return results


def EnableAllToolbar(value):
    """[Disable or Enable all toolbars.
    This is useful to disallow using any
    other tool while an instans of a tool is active]

    Args:  value ([Boolean]): [False : to disable all toolbars,
     True  : to re-enable all toolbars ]
    """
    mw = Gui.getMainWindow()
    tbs = mw.findChildren(QtGui.QToolBar)
    for i in tbs:
        i.setEnabled(value)


def DisableEnableAllMenus(value):
    """[
    Disable or Enable all menus. This is useful
    to disallow using any other tool while an instans
    of a tool is active]

    Args:
        value ([Boolean]): [False : to disable all menus, 
                            True  : to re-enable all menus 
                            ]
    """
    mw = Gui.getMainWindow()
    tbs = mw.findChildren(QtGui.menuBar)
    for i in tbs:
        i.setEnabled(value)


def disableEnableOnlyOneCommand(toolName: str = "", value: bool = False):
    mw = Gui.getMainWindow()
    t = mw.findChildren(QtCore.QTimer)
    t[2].stop()
    a = mw.findChild(QtGui.QAction, toolName)  # for example "Std_New"
    a.setDisabled(value)


def clearReportView(name: str = ""):
    """[Clear Report View console]

    Args:
        name ([type]): [description]
    """
    mw = Gui.getMainWindow()
    r = mw.findChild(QtGui.QTextEdit, "Report view")
    r.clear()
    import time
    now = time.ctime(int(time.time()))
    App.Console.PrintWarning("Cleared Report view " +
                             str(now) + " by " + name + "\n")


def clearPythonConsole(name: str = ""):
    """[Clear Python console]
    Args:
        name ([type]): [Message to  print on console]
    """
    mw = Gui.getMainWindow()
    r = mw.findChild(QtGui.QPlainTextEdit, "Python console")
    r.clear()
    import time
    now = time.ctime(int(time.time()))
    App.Console.PrintWarning(
        "Cleared Python console " + str(now) + " by " + name + "\n")


def findMainListedObjects():
    """[
        Find and return main objects in the active document
        - no children will be return
        And must be solid - no 2D or group should be included
        and must be visible
        ]

    Returns:
        [list]: [list of objects found]
    """
    results = []
    for i in App.ActiveDocument.Objects:
        name = i.Name
        if (Gui.ActiveDocument.getObject(name).Visibility == False):
            continue # We shouldn't touch objects that are invisible.
        Gui.ActiveDocument.getObject(name).Visibility = False
        inlist = i.InList
        if len(inlist) == 0:
            if hasattr(i, "Shape") and i.Shape.Solids:  # Must be solid and has shape
                results.append(i)
                Gui.ActiveDocument.getObject(name).Visibility = True
    return results


def Overlapping(Sourceobj1, Targetobj2):
    """[Check if two objects overlap each other]
    Args:
        Sourceobj1 ([3D selection object]): [description]
        Targetobj2 ([3D selection object]): [description]
    Returns:
        [type]: [description]
    """
    if (Sourceobj1.Shape.Volume == 0 or Targetobj2.Shape.Volume == 0):
        return False
    elif (Sourceobj1 == Targetobj2):
        return False  # The same object
    elif (Sourceobj1.Shape == Targetobj2.Shape):
        return False
    common_ = Sourceobj1.Shape.common(Targetobj2.Shape)
    if (common_.Area != 0.0):
        return True
    else:
        return False


def checkCollision(newObj):
    """[Find a list of objects from the active
    document that is/are intersecting with newObj]
    Args:
        newObj ([3D Selection Object]): [Object checked with document objects]
    Returns:
        [type]: [Document objects]
    """
    objList = findMainListedObjects()  # get the root objects - no children
    for obj in objList:
        if obj.Name == newObj.Name:
            objList.remove(obj)
            break

    results = []
    for obj in objList:
        o = None
        if (Overlapping(newObj, obj) is True):
            if (hasattr(obj, "Name")):
                o = App.ActiveDocument.getObject(obj.Name)
            elif (hasattr(obj, "Obj.Name")):
                o = App.ActiveDocument.getObject(obj.Object.Name)
            else:
                o = None
        if(o is not None):
            results.append(o)
    return results  # Return document objects


# Function to find the angle
# between the two lines with ref to the origin
# This here is to make it clear how you do that
def calculateAngle(v1, v2=App.Vector(1, 1, 0)):
    """[Find angle between a vector and the origin
        Assuming that the angle is between the line-vectors 
        (0.0, 0.0, 0.0) and (1,1,0)
    ]

    Args:
        v1 ([App.Vector]): [Vector to find angle with App.Vector(1,1,0) or with v2]
        v2 
    Returns:
        [float]: [Angle to the Z Axis in degrees]
    """
    return math.degrees(v1.getAngle(v2))


# The rotation below is inspired by https://wiki.freecadweb.org/Macro_Rotate_To_Point
# Thanks Mario
def RealRotateObjectToAnAxis(SelectedObj=None, RealAxis=App.Vector(0.0, 0.0, 0.0),
                             rotAngleX=0.0, rotAngleY=0.0, rotAngleZ=0.0):
    """[Rotate object ref to the given axis (Real rotation)]

    Args:
        SelectedObj ([Gui.Selection.Object], Required): [The object(s) to rotate].
        RealAxis ([App.Vector], optional): [Real axis used to rotate the object]. Defaults to App.Vector(0.0, 0.0, 0.0).
        rotAngleX (float, optional): [Angle of rotation - X Axis]. Defaults to 0.0.
        rotAngleY (float, optional): [Angle of rotation - Y Axis]. Defaults to 0.0.
        rotAngleZ (float, optional): [Angle of rotation - Z Axis]. Defaults to 0.0.
    """

    if (SelectedObj == None):
        raise ValueError("SelectedObj must be (a) selection object(s) ")

    if (type(SelectedObj) == list):
        for obj in SelectedObj:
            obj.Placement = App.Placement(App.Vector(0.0, 0.0, 0.0),
                                          App.Rotation(
                                              rotAngleX, rotAngleY, rotAngleZ),
                                          App.Vector(RealAxis.x, RealAxis.y, RealAxis.z)).multiply(
                App.ActiveDocument.getObject(obj.Name).Placement)
            textRota = ("[Rot=(" + str(round(SelectedObj.Placement.Rotation.toEuler()[0], 2)) + " , " +
                        str(round(obj.Placement.Rotation.toEuler()[1], 2)) + " , " +
                        str(round(obj.Placement.Rotation.toEuler()[2], 2)) + ")] " +
                        "[Axis=(" + str(round(RealAxis.x, 2))+" , " + str(round(RealAxis.y, 2))+" , " +
                        str(round(RealAxis.z, 2))+")]")
            # print(textRota)
    else:

        SelectedObj.Placement = App.Placement(App.Vector(0.0, 0.0, 0.0),
                                              App.Rotation(
                                                  rotAngleX, rotAngleY, rotAngleZ),
                                              App.Vector(RealAxis.x, RealAxis.y, RealAxis.z)).multiply(
            App.ActiveDocument.getObject(SelectedObj.Name).Placement)

        textRota = ("[Rot=(" + str(round(SelectedObj.Placement.Rotation.toEuler()[0], 2)) + " , " +
                    str(round(SelectedObj.Placement.Rotation.toEuler()[1], 2)) + " , " +
                    str(round(SelectedObj.Placement.Rotation.toEuler()[2], 2)) + ")] " +
                    "[Axis=(" + str(round(RealAxis.x, 2))+" , " + str(round(RealAxis.y, 2))+" , " + str(round(RealAxis.z, 2))+")]")

# The rotation below is inspired by https://wiki.freecadweb.org/Macro_Rotate_To_Point
# Thanks Mario


def RotateObjectToCenterPoint(SelectedObj=None, XAngle=0, YAngle=45, ZAngle=0):
    """[Rotate object ref to it's center point]

    Args:
        SelectedObj ([Gui.Selection.Object], Required): [description]. Defaults to None.
        XAngle (int, optional): [description]. Defaults to 0.
        YAngle (int, optional): [description]. Defaults to 45.
        ZAngle (int, optional): [description]. Defaults to 0.
    """
    # The object will rotate at it's place
    if (SelectedObj == None):
        raise ValueError("SelectedObj must be (a) selection object(s) ")
    if (type(SelectedObj) == list):
        for obj in SelectedObj:
            axisX = obj.Shape.BoundBox.Center.x
            axisY = obj.Shape.BoundBox.Center.y
            axisZ = obj.Shape.BoundBox.Center.z
        RealRotateObjectToAnAxis(SelectedObj, App.Vector(
            axisX, axisY, axisZ), math.radians(XAngle), math.radians(YAngle), math.radians(ZAngle))
    else:
        axisX = SelectedObj.Shape.BoundBox.Center.x
        axisY = SelectedObj.Shape.BoundBox.Center.y
        axisZ = SelectedObj.Shape.BoundBox.Center.z
        # RealRotateObjectToAnAxis(SelectedObj, App.Vector(
        #    axisX, axisY, axisZ), math.radians(XAngle), math.radians( YAngle), math.radians(ZAngle))
        RealRotateObjectToAnAxis(SelectedObj, App.Vector(
            axisX, axisY, axisZ), (XAngle), (YAngle), (ZAngle))


def getSortedXYZFromVertices(vertices=None):
    """[Sort vertices in list by returning 3 lists
        for the 3 axis X,Y,Z separated and sorted]

    Args:
        vertices ([type]): [description]

    Returns:
        [type]: [description]
    """
    if vertices is None:
        raise ValueError("Vertices must be valid")
    try:
        allZ = []
        allY = []
        allX = []
        for i in range(0, len(vertices)):
            allX.append(vertices[i].x)
            allY.append(vertices[i].y)
            allZ.append(vertices[i].z)
        if (allX == [] or allY == [] or allZ == []):
            raise ValueError("Vertices must be valid")
        allX.sort()
        allY.sort()
        allZ.sort()
        return (allX, allY, allZ)

    except Exception as err:
        App.Console.PrintError("'getSortedXYZFromVertices -Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def getLowestEdgeInAFace(selectedObj=None):
    """[Find lower Edge from a face ]

    Args:
        selectedObj ([Face Object], Required): [Face to find the lowest edg for].

    Raises:
        ValueError: [When the face is not given to the function]
        Exception: [If something went wrong]

    Returns:
        [Edge Object]: [Lower edge in the face (z is lowest)]
    """
    try:
        if selectedObj is None:
            raise ValueError("SelectedObj must be a face")
        ss = selectedObj.Shape
        allZ = []
        allY = []
        allX = []
        vert = ss.Vertexes
        for i in range(0, len(ss.Vertexes)):
            allX.append(vert[i].Point.x)
            allY.append(vert[i].Point.y)
            allZ.append(vert[i].Point.z)

        allX.sort()
        allY.sort()
        allZ.sort()

        result = None
        testAllX = allX.count(allX[0]) == len(allX)
        testAllY = allY.count(allY[0]) == len(allY)
        testAllZ = allZ.count(allZ[0]) == len(allZ)

        if(testAllZ):
            for edge in ss.Edges:
                if edge.SubShapes[0].Point.y == allY[0] or edge.SubShapes[0].Point.y == allY[1]:
                    if edge.SubShapes[1].Point.y == allY[0] or edge.SubShapes[1].Point.y == allY[1]:
                        return edge
        else:
            # This is correcto for all faces but not for top or bottom.
            for edge in ss.Edges:
                if edge.SubShapes[0].Point.z == allZ[0] or edge.SubShapes[0].Point.z == allZ[1]:
                    if edge.SubShapes[1].Point.z == allZ[0] or edge.SubShapes[1].Point.z == allZ[1]:
                        return edge
        # We shouldn't be here
        raise Exception("Not found")  # Don't know when this happens

    except Exception as err:
        App.Console.PrintError("'getLowestEdgeInAFace -Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def getNormalized(selectedObj=None):
    if selectedObj is None:
        raise ValueError("SelectedObj must be a face")
    edg = getLowestEdgeInAFace(selectedObj)
    v1 = edg.Vertexes[0].Point
    v2 = edg.Vertexes[1].Point
    vt = v1.sub(v2)
    vt = vt
    p1 = edg.valueAt(edg.FirstParameter)
    p2 = edg.valueAt(edg.LastParameter)

    vnormal = p2-p1
    return vnormal


def getBase(selectedObj, radius=1, thickness=1):
    edg = getLowestEdgeInAFace(selectedObj)
    nor = getNormalized(selectedObj)
    basePoint = edg.valueAt(edg.FirstParameter) + nor*(radius+thickness)
    return basePoint

#TODO: FIXME : ALLOW SENDING THE EDGE AND SHAPE TO THIS FUNCTION
# See https://forum.freecadweb.org/viewtopic.php?style=1&p=527043
def findFaceSHavingTheSameEdge(edge=None,shape=None):
    """[Find Faces that have the selected edge]
    Returns:
        [Face Objects]: [Return the faces having
        the selected edge or None if not found/error occur]
    """
    if edge is None:
        s = Gui.Selection.getSelectionEx()[0]
        edge = s.SubObjects[0]
        shape = s.Object.Shape
    else:
        edge = edge
        shape = shape
    result = shape.ancestorsOfType(edge, Part.Face)
    if len(result)>=1:
        return result
    else: 
        return None 


def findFacehasSelectedEdge(_edge=None,_shape=None):
    """[Find Face that has the selected edge]
    Returns:
        [Face Object]: [Return the face of the selected
        edge or None if error occurs]
    """
    if _edge is None:
        obj = Gui.Selection.getSelectionEx()[0]
        edge = obj.SubObjects[0]
        Faces = obj.Object.Shape.Faces
    else:
        edge=_edge
        Faces=_shape.Faces
    for fa in Faces:
        for ed in fa.Edges:
            if edge.isEqual(ed):
                return fa
    return None

def calculateMouseAngle(val1, val2):
    """[Calculate Angle of two coordinates ( xy, yz or xz).
        This function is useful to calculate mouse position
        in Angle depending on the mouse position.
    ]

    Args:
        val1 ([Horizontal coordinate]): [x, y]
        val2 ([Vertical coordinate ]): [y or z]

    Returns:
        [int]: [Calculated value in degrees]
    """
    if(val2 == 0):
        return None  # divide by zero
    result = 0
    if (val1 > 0 and val2 > 0):
        result = int(math.degrees(math.atan2(float(val1),
                                             float(val2))))
    if (val1 < 0 and val2 > 0):
        result = int(math.degrees(math.atan2(float(val1),
                                             float(val2))))+360
    if (val1 > 0 and val2 < 0):
        result = int(math.degrees(math.atan2(float(val1),
                                             float(val2))))
    if (val1 < 0 and val2 < 0):
        result = int(math.degrees(math.atan2(float(val1),
                                             float(val2))))+360
    return result



# This code is by by Roy_043 from the forum
# https://forum.freecadweb.org/viewtopic.php?p=557404#p557404
#But it didn't work prefectly and I leave it here for future usage. I need to understand which I DON'T NOW :(
# def get_global_placement (point, angle=0.0):
#    """[Get global placement for a point ona a active Draft working plane.
#        And rotate the object by the angle given in degrees
#    ]

#    Args:
#        point ([Mouse Position or any position to convert]): [Given point to place on the Draft Plane]
#        angle ([type]): [Rotating angle for placement rotation.]

#    Returns:
#        [type]: [description]
#    """
#    # point (vector) and angle (degrees) relative to Draft working plane
#    import WorkingPlane
#    if not hasattr(App, "DraftWorkingPlane"):
#        App.DraftWorkingPlane = WorkingPlane.plane()
#    App.DraftWorkingPlane.setup()
#    place_plane = App.DraftWorkingPlane.getPlacement()
#    place_rel = App.Placement()
#    place_rel.Base = point
#    place_rel.Rotation.Angle = math.radians(angle)
#    return place_plane.multiply(place_rel)

''' 

Convert global point to DraftWorkingPlane with rotation.

import FreeCAD as App
import Part
import math
import WorkingPlane

if not hasattr(App, "DraftWorkingPlane"):
    App.DraftWorkingPlane = WorkingPlane.plane()

def get_global_placement (point, angle):
    # point (vector) and angle (degrees) relative to Draft working plane
    App.DraftWorkingPlane.setup()
    place_plane = App.DraftWorkingPlane.getPlacement()
    place_rel = App.Placement()
    place_rel.Base = point
    place_rel.Rotation.Angle = math.radians(angle)
    return place_plane.multiply(place_rel)

place = get_global_placement(App.Vector(3,4,0), 60)
box = App.ActiveDocument.addObject("Part::Box", "myBox")
box.Placement = place
App.ActiveDocument.recompute()

 '''

#look at 
# https://dev.opencascade.org/content/brepoffsetapimakethicksolid-some-characters-can-be-hollowed-out-some-cant-help-pythonocc
# 
# Class to remove surface,edge, wire,line,vertex from a shape
'''Some api hits

DraftGeomUtils.findIntersection()


#'''
#class removeSubShapes:
#
#    def __init__(self, subObj, OriginalShape):
#        self.SubObj = subObj
#        self.targetShape = OriginalShape
#    def removeShapes(self):
#        Removal=rf()
#        Removal.AddFacesToRemove(Part.__toPythonOCC__(self.SubObj))
#        Removal.SetShape(Part.__toPythonOCC__(self.targetShape))
#       
#        Removal.Perform()
#        if not Removal.HasErrors():
#            return Part.__fromPythonOCC__(Removal.Shape())
#        else:
#            return None
# 
# A class that will revers engineer
# surfaces and recreate it with 
# new vertices
 
# A class that will revers engineer
# surfaces and recreate it with 
# new vertices
class reversEngSurface(object):
    
    __slots__= ['newObject', 
                'oldNewVertices'
                
                
                ]
    def __init__ (self, _oldNewVertices = [[]]):
        self.newObject=None
        self.oldNewVertices = _oldNewVertices

        pass
    def isCylinder(self,obj):
        pass
    
    def checkPlanar(self,obj):
        pass
    
    def checkCurve(self,obj):
        pass
    
    def checkLine(self,obj):
        pass
    
    def reversEng(self,obj):
        pass
    
    def recreateSurface(self):
        return (self.newObject)


def isFaceOf3DObj(selectedObj):
    """[Check if the selected object is a face from
        a 3D object or is a 2D object.

        Face of 3D Object = True
        2D Object= False
    Returns:
        [Boolean]: [Return True if the selected
        object is a face from 3D object, otherwise False]
    """
    # TODO: How accurate is this function?
    if hasattr(selectedObj.Object, "Shape") and len(selectedObj.Object.Shape.Solids) > 0:
        return True
    if hasattr(selectedObj.Object, "Shape") and selectedObj.Object.Shape.ShapeType == "Shell":
        return True
    if hasattr(selectedObj.Object, "Shape") and selectedObj.Object.Shape.ShapeType == "Compound":
        return True
    else:
        return False



def showFirstTab():
    """Return back the view of the tab 
        to 'Model'
    """
    mw=Gui.getMainWindow()
    dw=mw.findChildren(QtGui.QDockWidget)
    for i in dw:
        if i.objectName() == "Combo View":
            tab = i.findChild(QtGui.QTabWidget)
            break
    tab.setCurrentIndex(0)