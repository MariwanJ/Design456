# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# **************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
from pivy import coin
import FACE_D as faced
from PySide.QtCore import QT_TRANSLATE_NOOP
from typing import List
import Design456Init
from PySide import QtGui, QtCore
from ThreeDWidgets.fr_arrow_widget import Fr_Arrow_Widget
from ThreeDWidgets import fr_arrow_widget
from ThreeDWidgets.constant import FR_EVENTS
from ThreeDWidgets.constant import FR_COLOR
from draftutils.translate import translate  # for translation
import math
import Part
from ThreeDWidgets import fr_label_draw
from Design456Pref import Design456pref_var
# The ration of delta mouse to mm
MouseScaleFactor = 1
__updated__ = '2022-10-09 20:33:13'

'''
    How it works: 
    We have to recreate the object each time we change the length. 
    This means that the redrawing must be optimized
    
    1-If we have a 2D face, we just extrude it 
    2-If we have a face from a 3D object, we extract that face and extrude it
    3-Created object: either it will remain as a new object or would be merged. 
      But if it is used as a tool to cut another 3D object, the object will disappear. 
'''


def callback_move(userData: fr_arrow_widget.userDataObject = None):
    """[ Callback for the arrow movement. 
    This will be used to calculate the length of the Extrude operation.]
    Args:
        userData (fr_arrow_widget.userDataObject, optional): 
        [Userdata contain link to several variable and the arrow widget]. Defaults to None.

    Returns:
        [type]: [Nothing is returned] None.
    """
    try:
        
        if userData is None:
            return  # Nothing to do here - shouldn't be None

        ArrowObject = userData.ArrowObj
        events = userData.events
        linktocaller = userData.callerObject
        linktocaller.ExtrusionStepSize=Design456pref_var.MouseStepSize
        if type(events) != int:
            return

        clickwdgdNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                     ArrowObject.w_pick_radius, ArrowObject.w_widgetSoNodes)
        clickwdglblNode = ArrowObject.w_parent.objectMouseClick_Coin3d(ArrowObject.w_parent.w_lastEventXYZ.pos,
                                                                       ArrowObject.w_pick_radius, ArrowObject.w_widgetlblSoNodes)
        linktocaller.endVector = App.Vector(ArrowObject.w_parent.w_lastEventXYZ.Coin_x,
                                            ArrowObject.w_parent.w_lastEventXYZ.Coin_y,
                                            ArrowObject.w_parent.w_lastEventXYZ.Coin_z)

        if clickwdgdNode is None and clickwdglblNode is None:
            if linktocaller.run_Once is False:
                return   # Nothing to do

        if linktocaller.run_Once is False:
            linktocaller.run_Once = True
            # only once
            linktocaller.startVector = linktocaller.endVector
            linktocaller.mouseToArrowDiff = (linktocaller.endVector.sub(userData.ArrowObj.w_vector[0])/linktocaller.ExtrusionStepSize)
        
        deltaChange=(linktocaller.endVector - linktocaller.startVector).dot(linktocaller.normalVector)
        linktocaller.extrudeLength = linktocaller.ExtrusionStepSize* (int(deltaChange/linktocaller.ExtrusionStepSize))
        
        linktocaller.resizeArrowWidgets(
            linktocaller.endVector.sub(linktocaller.mouseToArrowDiff))
        linktocaller.ExtrudeLBL.setText(
            "Length= " + str(round(linktocaller.extrudeLength,2)))
        userData.ArrowObj.changeLabelstr(
            "  Length= " + str(round(linktocaller.extrudeLength,2)))
        if linktocaller.CylindricalFace is True:
            linktocaller.recreateCylinderObject()
        else:
            linktocaller.reCreateExtrudeObject()
        
        linktocaller.lblExtrudeSize.setText("Extrude Step Size = " + str(linktocaller.ExtrusionStepSize))
        App.ActiveDocument.recompute()

    except Exception as err:
        App.Console.PrintError("'callback_move' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def createFusionObjectBase(linktocaller):
    """
        Create Fusion object to collect 
        several object then use them in other processes. 
        This is a Base Fusion
    """
    allObjects = []
    for i in range(0, len(linktocaller.objChangedTransparency)):
        allObjects.append(App.ActiveDocument.getObject(
            linktocaller.objChangedTransparency[i].Object.Name))
        Gui.ActiveDocument.getObject(
            linktocaller.objChangedTransparency[i].Object.Name).Transparency = 0
    if(linktocaller.OperationOption == 1):
        # we have to add the tools also
        if(linktocaller.WasFaceFrom3DObject is True):
            # 3D objects consist of old object + extruded face
            allObjects.append(linktocaller.selectedObj.Object)
            allObjects.append(linktocaller.newObject)
        else:
            # 2D object consist of only the new object as the old object was only 2D face
            allObjects.append(linktocaller.newObject)
        BaseObj = App.ActiveDocument.addObject("Part::MultiFuse", "Merged")
        BaseObj.Refine = True
        BaseObj.Shapes = allObjects
        return BaseObj
    elif(linktocaller.OperationOption == 2):
        if(len(allObjects) > 1):
            BaseObj = App.ActiveDocument.addObject("Part::MultiFuse", "Merged")
            BaseObj.Refine = True
            BaseObj.Shapes = allObjects
            return BaseObj
        else:
            return allObjects[0]


def createFusionObjectTool(linktocaller):
    """
        Create Fusion object which is used as tool in other process.
    """
    Transparency = False
    for obj in linktocaller.objChangedTransparency:
        if obj.Object == linktocaller.selectedObj.Object:
            # The object is Base not tool
            Transparency = True

    if(linktocaller.WasFaceFrom3DObject is True
       and Transparency is True):
        # The face is from a 3D object that extruded to cut
        return linktocaller.newObject
    else:
        # We have extracted a face from 3D object. Therefore it must be included
        MERGEallObjects = []
        MERGEallObjects.append(linktocaller.selectedObj.Object)
        MERGEallObjects.append(linktocaller.newObject)
        ToolObj = App.ActiveDocument.addObject("Part::MultiFuse", "MergedTool")
        ToolObj.Refine = True
        ToolObj.Shapes = MERGEallObjects
        # BUG in FreeCAD doesn't work
        Gui.ActiveDocument.getObject(ToolObj.Name).Transparency = 0
        Gui.ActiveDocument.getObject(ToolObj.Name).ShapeColor = (
            FR_COLOR.FR_BISQUE)  # Transparency doesn't work, bug in FREECAD
        return ToolObj


    
def callback_release(userData: fr_arrow_widget.userDataObject = None):
    """
       Callback after releasing the left mouse button. 

    """
    try:
        #Final touch moved from the callback to another function. This allow the tool to do final touch 
        #at the time of pressing OK button not the release of the arrow widget. 
        #I keep this function for future use but it is not doing anything at the moment
        pass

    except Exception as err:
        faced.EnableAllToolbar(True)
        App.Console.PrintError("'Design456_Extrude' Release Filed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


class Design456_SmartExtrude:
    """
        Apply Extrude to any 3D/2D object by
        selecting the object's face, Length of
        the Extrude is counted by dragging the
        arrow towards the negative Z axis.
    """

    def __init__(self):
        self._vector = App.Vector(0.0, 0.0, 0.0)
        self.mw = None
        self.dialog = None
        self.tab = None
        self.smartInd = None
        self._mywin = None
        self.b1 = None
        self.ExtrudeLBL = None
        self.run_Once = False
        self.endVector = None
        self.startVector = None
        self.extrudeLength = 0.001  # This will be the Delta-mouse position
        # We will make two object, one for visual effect and
        # the other is the original
        self.selectedObj = None
        self.direction = None
        # We use this to simplify the code - for both, 2D and
        # 3D object, the face variable is this
        self.targetFace = None
        self.newObject = None
        self.DirExtrusion = App.Vector(0, 0, 0)  # No direction if all are zero
        self.OperationOption = 0  # default is zero
        self.objChangedTransparency = []
        self.WasFaceFrom3DObject = False
        self.mouseToArrowDiff = None

        # Extrusion checkboxes
        self.radSubtract = None
        self.radAsIs = None
        self.radSubtract = None
        self.axis=App.Vector(0, 0,1)
        
        # 
        self.Symmetric=None
        
        #Cylindrical Face 
        self.plcBase=None
        self.height=None
        self.OriginalRadius=None
        self.CylindricalFace=False

        # Extrusion step
        self.ExtrusionStepSize = Design456pref_var.MouseStepSize
    
    #Used only with cylindrical face
    def recreateCylinderObject(self):
        """
            This function creates the cylinder object 
            after each change in the extrusion length
        """
        try:
            if self.extrudeLength <0:
                newInnerRadius=self.OriginalRadius
                newOuterRadius=self.OriginalRadius+self.extrudeLength
            else:
                newInnerRadius=self.OriginalRadius+self.extrudeLength
                newOuterRadius=self.OriginalRadius
           
            innerObj=None
            outerObj=None
            if newInnerRadius>0:                
                innerObj=Part.makeCylinder(newInnerRadius, self.height,self.center,self.axis,360)
            if newOuterRadius>0:
                outerObj=Part.makeCylinder(newOuterRadius, self.height,self.center,self.axis,360)
            newObj= App.ActiveDocument.addObject('Part::Feature', "CyExtrude")

            if innerObj is not None and outerObj is not None:
                if newInnerRadius>newOuterRadius:
                    newObj.Shape=innerObj.cut(outerObj)
                elif newInnerRadius<newOuterRadius:
                    newObj.Shape=innerObj.cut(outerObj)
            elif innerObj is None and outerObj is not None:
                newObj.Shape=outerObj
            elif outerObj is None and innerObj is not None:
                newObj.Shape=innerObj
            else:
                #DON'T KNOW WHAT TODO : TODO: FIXME:
                newObj=None
            App.ActiveDocument.recompute()
            #Now decide wether we leave as it is or merge, or cut. 
            if newObj is not None:
                if self.newObject is not None:
                    App.ActiveDocument.removeObject(self.newObject.Name)
                    self.newObject =None
                self.newObject=newObj
            if self.OperationOption == 2 or self.OperationOption == 1:
                self.objChangedTransparency.clear()
                result = faced.checkCollision(self.newObject)
                if result != []:
                    for obj in result:
                        # should be GUI object not App object!!!
                        TE = Gui.ActiveDocument.getObject(obj.Name)
                        TE.Transparency = 80
                        self.objChangedTransparency.append(TE)
        except Exception as err:
            App.Console.PrintError("'recreateNewObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def reCreateExtrudeObject(self):
        """
        [
         Recreate the object after changing the length of the extrusion
         This will also change the Transparency of object if subtraction
         is selected.
        ]
        """
        try:
            self.newObject.LengthFwd = self.extrudeLength
            if self.OperationOption == 2 or self.OperationOption == 1:
                self.objChangedTransparency.clear()
                result = faced.checkCollision(self.newObject)
                if result != []:
                    for obj in result:
                        # should be GUI object not App object!!!
                        TE = Gui.ActiveDocument.getObject(obj.Name)
                        TE.Transparency = 80
                        self.objChangedTransparency.append(TE)
                App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'reCreateExtrudeObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def resizeArrowWidgets(self, endVec):
        """[Resize the arrow widget. The widget will be moved to the new position]
        Args:
            endVec ([App.Vector]): [New position]
        """
        currentLength = self.extrudeLength
        # to let the arrow be outside the object
        self.extrudeLength = self.extrudeLength + 15
        self.smartInd.w_vector = self.calculateNewVector()
        self.extrudeLength = currentLength  # return back the value.
        self.smartInd.redraw()

    def getArrowPosition(self):
        """"
         Find out the vector and rotation of the arrow to be drawn.
        """
        # For now the arrow will be at the top
        try:
            rotation = [0.0, 0.0, 0.0, 0.0]
            face1 = None
            if(self.WasFaceFrom3DObject):
                # The whole object is selected
                sub1 = self.selectedObj
                face1 = sub1.SubObjects[0]
            else:
                face1 = self.selectedObj.Object.Shape.Faces[0]

            self.extrudeLength = 5
            self._vector = self.calculateNewVector()
            self.extrudeLength = 0.0
            if (face1.Surface.Rotation.Axis==App.Vector(0,0,1) or 
                face1.Surface.Rotation.Axis==App.Vector(1,0,0) or 
                face1.Surface.Rotation.Axis==App.Vector(0,1,0) or
                face1.Surface.Rotation.Axis==App.Vector(0,0,0) or
                face1.Surface.Rotation.Axis==App.Vector(1,1,0) or
                face1.Surface.Rotation.Axis==App.Vector(1,1,1) ):
                # section direction. When the face doesn't have a Rotation
                yL = face1.CenterOfMass
                uv = face1.Surface.parameter(yL)
                nv = face1.normalAt(uv[0], uv[1])
                direction = yL.sub(nv + yL)
                t=direction.x
                direction.x=direction.y
                direction.y=t
                rotation = (direction.x,direction.y,direction.z, math.degrees(nv.getAngle(App.Vector(0,0,10))))
            else:
                rotation = (face1.Surface.Rotation.Axis.x,
                            face1.Surface.Rotation.Axis.y,
                            face1.Surface.Rotation.Axis.z,
                            math.degrees(face1.Surface.Rotation.Angle))
            return rotation

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' getArrowPosition-Failed"
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def isFaceOf3DObj(self):
        """[Check if the selected object is a face from
            a 3D object or is a 2D object.
            A face from a 3D object, cannot be extruded directly.
            We have to extract a Face and them Extrude]
            Face of 3D Object = True
            2D Object= False
        Returns:
            [Boolean]: [Return True if the selected
            object is a face from 3D object, otherwise False]
        """
        # TODO: How accurate is this function?
        if hasattr(self.selectedObj.Object, "Shape") and len(self.selectedObj.Object.Shape.Solids) > 0:
            return True
        if hasattr(self.selectedObj.Object, "Shape") and self.selectedObj.Object.Shape.ShapeType == "Shell":
            return True
        if hasattr(self.selectedObj.Object, "Shape") and self.selectedObj.Object.Shape.ShapeType == "Compound":
            return True
        else:
            return False

    def extractFace(self):
        """[Extract a face from a 3D object as it cannot be extruded otherwise]

        Returns:
            [Face]: [Face created from the selected face of the 3D object]
        """
        newobj = "eFace"
        sh = self.selectedObj.Object.Shape.copy()
        if hasattr(self.selectedObj.Object, "getGlobalPlacement"):
            gpl = self.selectedObj.Object.getGlobalPlacement()
            sh.Placement = gpl
        else:
            pass  # TODO: WHAT SHOULD WE DO HERE ?

        name = self.selectedObj.SubElementNames[0]
        newobj = App.ActiveDocument.addObject(
            "Part::Feature", newobj)  # create face
        newobj.Shape = sh.getElement(name)
        App.ActiveDocument.recompute()
        newobj.Visibility = False
        return newobj

    def calculateNewVector(self):
        """[Calculate the new position that will be used for the arrow drawing]

        Returns:
            [App.Vector]: [Position where the arrow will be moved to]
        """
        try:
            if(self.WasFaceFrom3DObject):
                ss = self.selectedObj.SubObjects[0]
            else:
                ss = self.selectedObj.Object.Shape
            if hasattr(ss, "CenterOfMass"):
                yL = ss.CenterOfMass
                uv = ss.Surface.parameter(yL)
                nv = ss.normalAt(uv[0], uv[1])

            elif hasattr(ss.SubObjects[0], "CenterOfMass") :
                yL = ss.SubObjects[0].CenterOfMass
                uv = ss.SubObjects[0].Surface.parameter(yL)
                nv = ss.SubObjects[0].normalAt(uv[0], uv[1])
            else:
                yL = self.selectedObj.Object.Shape.Faces[0].centerOfMass  #TODO This is wrong. FIXME: Don't know when and why this happens
                uv = self.selectedObj.Object.Shape.Faces[0].Surface.parameter(yL)
                nv = self.selectedObj.Object.Shape.Faces[0].normalAt(uv[0], uv[1])
                print("oh no it is wrong")
            
            self.normalVector = nv

            if (self.extrudeLength == 0):
                d = self.extrudeLength = 1
            else:
                d = self.extrudeLength
            point = yL + d * nv
            return ([point, App.Vector(0, 0, 0)])  # Must be two vectors always

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' calculateNewVector-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def Activated(self):
        """[Executes when the tool is used]
        """
        import ThreeDWidgets.fr_coinwindow as win
        try:
            print("Smart Extrusion")
            sel = Gui.Selection.getSelectionEx()
            self.ExtrusionStepSize=Design456pref_var.MouseStepSize            
            
            if len(sel) == 0:
                # An object must be selected
                errMessage = "Select a face to Extrude"
                faced.errorDialog(errMessage)
                return
            self.selectedObj = sel[0]
            # Whole object is selected TODO: FIXME: Check if this works always.
            if len(self.selectedObj.SubObjects) == 0:
                errMessage = "Select a face to Extrude"
                faced.errorDialog(errMessage)
                return
            faced.EnableAllToolbar(False)
            # Undo
            App.ActiveDocument.openTransaction(
                translate("Design456", "SmartExtrude"))
            self.WasFaceFrom3DObject = self.isFaceOf3DObj()
           
            rotation = self.getArrowPosition()
            self.smartInd = Fr_Arrow_Widget(self._vector,
                                            ["  Length 0.0", ],
                                            1,
                                            FR_COLOR.FR_RED,
                                            FR_COLOR.FR_WHITE,
                                            rotation, [1.2, 1.2, 1.2],
                                            3,
                                            0.0)

            self.smartInd.w_callback_ = callback_release
            self.smartInd.w_move_callback_ = callback_move
            self.smartInd.w_userData.callerObject = self
            if self._mywin is None:
                self._mywin = win.Fr_CoinWindow()

            self._mywin.addWidget(self.smartInd)
            mw = self.getMainWindow()
            mw.setFocus()
            self._mywin.show()

            #TODO :FIXME : CONTINUE DEVELOPING HERE. 
            '''
                CHECK IF IT IS CYLINDRICAL
                IF YES SKIP THE OTHER LINES AND MAKE PREPARATION FOR THE RECREATING THE OBJECT
            '''
            if (hasattr(self.selectedObj.SubObjects[0].Surface,"Radius")):
                #We have a cylinder shape 
                self.CylindricalFace=True
                self.OriginalRadius = self.selectedObj.SubObjects[0].Surface.Radius
                self.height=self.selectedObj.Object.Shape.BoundBox.ZLength
                self.center=self.selectedObj.SubObjects[0].Surface.Center
                # we put slightly bigger radius just to net error from OCC : TODO:FIXME: Is it correct?
                self.extrudeLength=0.01 
                self.recreateCylinderObject() 
                
            else:
                self.CylindricalFace=False
                if self.WasFaceFrom3DObject is True:  # We must know if the selection is a 2D face or a face from a 3D object
                    # We have a 3D Object. Extract a face and start to Extrude
                    self.targetFace = self.extractFace()
                else:
                    # We have a 2D Face - Extract it directly
                    self.targetFace = self.selectedObj.Object

                self.newObject = App.ActiveDocument.addObject(
                    'Part::Extrusion', 'Extrude')
                self.newObject.Base = self.targetFace
                self.newObject.DirMode = "Normal"  # Don't use Custom as it causes a PROBLEM!
                # Above statement is not always correct. Some faces require 'custom'
                self.newObject.DirLink = None
                self.newObject.LengthFwd = self.extrudeLength  # Must be negative
                self.newObject.LengthRev = 0.0
                self.newObject.Solid = True
                self.newObject.Reversed = False
                self.newObject.Symmetric = False
                self.newObject.TaperAngle = 0.0
                self.newObject.TaperAngleRev = 0.0
                self.newObject.Dir = Gui.ActiveDocument.getObject(
                    self.targetFace.Name).Object.Shape.Faces[0].normalAt(0, 0)
                if (self.newObject.Dir.x != 1 or
                    self.newObject.Dir.y != 1 or
                        self.newObject.Dir.z != 1):
                    self.newObject.DirMode = "Custom"

            App.ActiveDocument.recompute()

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' Activated-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def __del__(self):
        """ 
            class destructor
            Remove all objects from memory even fr_coinwindow
        """
        faced.EnableAllToolbar(True)
        try:
            self.smartInd.hide()
            self.smartInd.__del__()  # call destructor
            if self._mywin is not None:
                self._mywin.hide()
                del self._mywin
                self._mywin = None
            App.ActiveDocument.commitTransaction()  # undo reg.
            self.extrudeLength = 0
            self.OperationOption = 0
            self.selectedObj = None
            self.targetFace = None
            self.newObject = None
            del self

        except Exception as err:
            App.Console.PrintError("'Design456_Extrude' __del__-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def getMainWindow(self):
        """[Create the tab for the tool]

        Raises:
            Exception: [If no tabs were found]
            Exception: [If something unusual happen]

        Returns:
            [dialog]: [the new dialog which will be added as a tab to the tab section of FreeCAD]
        """
        try:
            toplevel = QtGui.QApplication.topLevelWidgets()
            self.mw = None
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
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Smart Extrude")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(200, 450)
            self.dialog.setWindowTitle("Smart Extrude")
            self.la = QtGui.QVBoxLayout(self.dialog)
            self.e1 = QtGui.QLabel(
                "(Smart Extrude)\nFor quicker\nApplying Extrude")

            commentFont = QtGui.QFont("Times", 14, True)
            self.ExtrudeLBL = QtGui.QLabel("Extrude Length=")
            self.e1.setFont(commentFont)

            okbox = QtGui.QDialogButtonBox(self.dialog)
            okbox.setOrientation(QtCore.Qt.Horizontal)
            okbox.setStandardButtons(QtGui.QDialogButtonBox.Ok)

            self.lblExtrudeSize = QtGui.QLabel(
                "Extrude Step Size = " + str(self.ExtrusionStepSize))
            self.lblExtrudeSize.setObjectName("lblExtrudeSize")
            comboFont = QtGui.QFont("Times", 13, True)

            self.lblExtrudeSize.setFont(comboFont)

            self.groupBox = QtGui.QGroupBox(self.dialog)
            self.groupBox.setGeometry(QtCore.QRect(60, 130, 120, 80))
            self.groupBox.setObjectName("Extrusion Type")

            self.radAsIs = QtGui.QRadioButton(self.groupBox)
            self.radAsIs.setObjectName("radAsIs")
            self.radAsIs.setText("As Is")

            self.radMerge = QtGui.QRadioButton(self.groupBox)
            self.radMerge.setObjectName("radMerge")
            self.radMerge.setText("Merge")

            self.radSubtract = QtGui.QRadioButton(self.groupBox)
            self.radSubtract.setObjectName("radSubtract")
            self.radSubtract.setText("Subtract")

            self.Symmetric=QtGui.QCheckBox(self.dialog)
            self.Symmetric.setObjectName("Symmetric")
            self.Symmetric.setText("Symmetric")
            self.Symmetric.toggled.connect(lambda: self.symmetric_cb(self.Symmetric.isChecked()))
            
  
  
            self.la.addWidget(self.e1)
            self.la.addWidget(self.ExtrudeLBL)
            self.la.addWidget(self.lblExtrudeSize)
            self.la.addWidget(self.Symmetric)
            self.la.addWidget(okbox)

            # Adding checkbox for Merge, Subtract Or just leave it "As is"
            self.la.addWidget(self.radAsIs)
            self.la.addWidget(self.radMerge)
            self.la.addWidget(self.radSubtract)

            self.radAsIs.setChecked(True)
            self.radAsIs.toggled.connect(lambda: self.btnState(self.radAsIs))
            self.radMerge.toggled.connect(lambda: self.btnState(self.radMerge))
            self.radSubtract.toggled.connect(
                lambda: self.btnState(self.radSubtract))

            QtCore.QObject.connect(
                okbox, QtCore.SIGNAL("accepted()"), self.hide)
            QtCore.QMetaObject.connectSlotsByName(self.dialog)

            return self.dialog

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def symmetric_cb(self,state):
        """ Activate or deactivate the symmetric for the created object

        Args:
            state (_type_): If True , Symmetric will be added to the created object
            otherwise no change will happen to the object
        """
        if self.CylindricalFace is True:
            # An object must be selected
            errMessage = "For cylindrical face, Symmetric is not supported"
            faced.errorDialog(errMessage)
            self.Symmetric.setChecked(False)
            return
        self.newObject.Symmetric = state
        
        
    def btnState(self, button):
        """ When radio buttons clicked this callback will executes
            It decide whether the created object is merged, cut or 
            left "as is" without modification

        Args:
            button (_type_): Which button is clicked and get the value
        """
        if button.text() == "As Is":
            if button.isChecked() is True:
                self.OperationOption = 0  # 0 as Is default, 1 Merged, 2 Subtracted
        elif button.text() == "Merge":
            if button.isChecked() is True:
                self.OperationOption = 1
        elif button.text() == "Subtract":
            if button.isChecked() is True:
                self.OperationOption = 2


    def doFinalJob(self):
        """   
        This function will finalize the Extrude operation. 
        Deleting the original object will be done when the user press 'OK' button
        """
        try:
            # Undo
            App.ActiveDocument.openTransaction(
                translate("Design456", "SmartExtrude"))
            App.ActiveDocument.recompute()
            self.startVector = None
            App.ActiveDocument.commitTransaction()  # undo reg.
            newObjcut = []
            # Do final operation. Either leave it as it is, merge or subtract
            if(self.OperationOption == 1):
                createFusionObjectBase(self)
                App.ActiveDocument.recompute()
                # subtraction will continue to work here
            elif self.OperationOption == 2:
                # Subtraction is complex. I have to cut from each object the same extruded part.
                if (self.objChangedTransparency != []):
                    base = createFusionObjectBase(self)
                    # Create a cut object for each transparency object
                    if(self.WasFaceFrom3DObject is True):
                        # It is a 3D drawing object
                        tool = createFusionObjectTool(self)
                        for i in range(0, len(self.objChangedTransparency)):
                            newObjcut.append(App.ActiveDocument.addObject(
                                "Part::Cut", "CUT" + str(i)))
                            newObjcut[i].Base = base
                            # Subtracted shape/object
                            newObjcut[i].Tool = tool
                            newObjcut[i].Refine = True
                        tool.Visibility = False
                    else:
                        for i in range(0, len(self.objChangedTransparency)):
                            newObjcut.append(App.ActiveDocument.addObject(
                                "Part::Cut", "CUT" + str(i)))
                            newObjcut[i].Base = base
                            # Subtracted shape/object
                            newObjcut[i].Tool = self.newObject
                            newObjcut[i].Refine = True

                    App.ActiveDocument.recompute()

            elif self.OperationOption == 0:
                # is here just to make the code more readable.
                pass  # nothing to do .
            self.run_Once =False 
            App.ActiveDocument.recompute()
            App.ActiveDocument.commitTransaction()  # undo reg.

        except Exception as err:
            faced.EnableAllToolbar(True)
            App.Console.PrintError("'Design456_Extrude' Release Filed. "
                                "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            

    def hide(self):
        """
        Hide the widgets. Remove also the tab.
        TODO:
        For this tool, I decide to choose "hide" to (merge, subtract or leave it as) here. 
        I might allow a "simple copy" in the future.
        TODO: If there will be a discussion about this, we might change this behavior!!
        """
        self.doFinalJob() #Do final job
        self.dialog.hide()
        del self.dialog
        dw = self.mw.findChildren(QtGui.QDockWidget)
        NewSize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(NewSize - 1)  # it ==0,1,2,3 ..etc
        App.ActiveDocument.commitTransaction()  # undo reg.

        for i in range(0, len(self.objChangedTransparency)):
            Gui.ActiveDocument.getObject(self.objChangedTransparency[i].Object.Name).Transparency = 0

        App.ActiveDocument.recompute()
        self.__del__()  # Remove all smart Extrude 3dCOIN widgets

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_SmartExtrude.svg',
            'MenuText': ' Smart Extrude',
                        'ToolTip':  ' Smart Extrude'
        }


Gui.addCommand('Design456_SmartExtrude', Design456_SmartExtrude())

