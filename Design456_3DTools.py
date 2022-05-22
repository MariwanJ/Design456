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
# * Author :Mariwan Jalal    mariwan.jalal@gmail.com                       *
# ***************************************************************************
import sys
import os
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init
import FACE_D as faced
import Design456_loftOnDirection
import Design456_Extrude
import Design456_Extract
import Design456_SplitObject
import Design456_unifySplitFuse
from PySide import QtCore, QtGui
from draftutils.translate import translate   #for translate
import math

__updated__ = '2022-05-22 20:57:53'

# Merge
class Design456_Part_Merge:

    def Activated(self):
        mergedObj = None
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Merge"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Part Merge"))
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))

            newObj = App.ActiveDocument.addObject("Part::MultiFuse", "MergedTemp")
            newObj.Shapes = allObjects
            newObj.Refine = True
            App.ActiveDocument.recompute()
            if newObj.isValid() is False:
                App.ActiveDocument.removeObject(newObj.Name)
                # Shape != OK
                errMessage = "Failed to Merge"
                faced.errorDialog(errMessage)
            else:

                # Make a simple copy
                newShape = Part.getShape(
                    newObj, '', needSubElement=False, refine=True)
                mergedObj=App.ActiveDocument.addObject('Part::Feature', 'Merged')
                mergedObj.Shape = newShape
                App.ActiveDocument.recompute()
                #Preserve color and other properties of the old obj
                faced.PreserveColorTexture(s[0].Object,mergedObj)
                # Remove Old objects
                for obj in allObjects:
                   App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(newObj.Name)
                App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
            del allObjects[:]
            return mergedObj
        
        except Exception as err:
            App.Console.PrintError("'Part::Merge' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Merge.svg',
            'MenuText': 'Part_Merge',
            'ToolTip':  'Part Merge'
        }


Gui.addCommand('Design456_Part_Merge', Design456_Part_Merge())


# Subtract
class Design456_Part_Subtract:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Subtract"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Part Subtract"))
            newObj = App.ActiveDocument.addObject("Part::Cut", "tempSubtract")
            newObj.Base = App.ActiveDocument.getObject(s[0].ObjectName)  # Target  must be Application object
            newObj.Tool = App.ActiveDocument.getObject(s[1].ObjectName)  # Subtracted shape/object must be Application object
            App.ActiveDocument.recompute()
            newObj.Refine = True
            App.ActiveDocument.recompute()
            # Make a simple copy
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=False)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Subtract')
            NewJ.Shape = newShape
            App.ActiveDocument.recompute()
            #Preserve color and other properties of the old obj
            faced.PreserveColorTexture(s[0].Object,NewJ)

            if newObj.isValid() is False:
                App.ActiveDocument.removeObject(NewJ.Name)
                # Shape != OK
                errMessage = "Failed to subtract objects"
                faced.errorDialog(errMessage)
            else:
                # Remove Old objects
                allObjects = []
                for o in s:
                    allObjects.append(
                        App.ActiveDocument.getObject(o.ObjectName))
                for obj in allObjects:
                    App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Subtract' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Subtract.svg',
            'MenuText': 'Part_Subtract',
            'ToolTip':  'Part Subtract'
        }


Gui.addCommand('Design456_Part_Subtract', Design456_Part_Subtract())


# Intersect
class Design456_Part_Intersect:
    """Message box (error) """

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            App.ActiveDocument.openTransaction(translate("Design456","Part Intersect"))
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Intersect"
                faced.errorDialog(errMessage)
                return
            newObj = App.ActiveDocument.addObject("Part::MultiCommon", "tempIntersect")
            newObj.Shapes = [App.ActiveDocument.getObject(
                s[0].ObjectName), App.ActiveDocument.getObject(s[1].ObjectName)]
            App.ActiveDocument.recompute()
            # Make a simple copy
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=False)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Intersect')
            NewJ.Shape = newShape
            App.ActiveDocument.recompute()
            # Remove Old objects
            allObjects = []
            #Preserve color and other properties of the old obj
            faced.PreserveColorTexture(s[0].Object,NewJ)
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Intersect' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Intersect.svg',
            'MenuText': 'Part_Intersect',
            'ToolTip':  'Part Intersect'
        }


Gui.addCommand('Design456_Part_Intersect', Design456_Part_Intersect())
# Group


class Design456_Part_Group:
    """Message box (error) """

    def errorDialog(self, msg):
        # Create a simple dialog QMessageBox
        # The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question}
        diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Tools ', msg)
        diag.setWindowModality(QtCore.Qt.ApplicationModal)
        diag.exec_()

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2):
                # Two object must be selected
                #App.ActiveDocument.openTransaction(translate("Design456","Part Group")) TODO: Doesn't work
                errMessage = "Select two or more objects to create a group"
                faced.errorDialog(errMessage)
                return

            newObj = App.ActiveDocument.addObject('App::Part', 'Group')
            newObj.Label = 'Group'
            for obj_ in s:
                obj = App.ActiveDocument.getObject(obj_.ObjectName)

            #App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Part::Part' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Group.svg',
            'MenuText': 'Part_Group',
            'ToolTip':  'Part Group'
        }


Gui.addCommand('Design456_Part_Group', Design456_Part_Group())


# Compound
class Design456_Part_Compound:
    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to Merge"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Part Compound"))
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))

            newObj = App.ActiveDocument.addObject("Part::Compound", "TempCompound")
            newObj.Links = allObjects
            # Make a simple copy
            App.ActiveDocument.recompute()
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=True)
            NewJ = App.ActiveDocument.addObject(
                'Part::Feature', 'Compound')
            NewJ.Shape = newShape
            
            #Preserve color and other properties of the old obj
            faced.PreserveColorTexture(s[0].Object,NewJ)
            
            # Remove Old objects
            for obj in allObjects:
                App.ActiveDocument.removeObject(obj.Name)
            App.ActiveDocument.removeObject(newObj.Name)
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Compound' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Part_Compound.svg',
            'MenuText': 'Part Compound',
            'ToolTip':  'Part Compound'
        }


Gui.addCommand('Design456_Part_Compound', Design456_Part_Compound())

# Shell


class Design456_Part_Shell:
    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # Two object must be selected
                errMessage = "Select two or more objects to use Shell Tool"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Part Shell"))
            thickness = QtGui.QInputDialog.getDouble(
                None, "Thickness", "Value:", 0, -1000.0, 1000.0, 2)[0]
            if(thickness ==0):
                return  # Nothing to do
            allObjects = []
            for o in s:
                allObjects.append(App.ActiveDocument.getObject(o.ObjectName))
            currentObj = App.ActiveDocument.getObject(s[0].ObjectName)
            currentObjLink = currentObj.getLinkedObject(True)
            thickObj = App.ActiveDocument.addObject(
                "Part::Thickness", "Thickness")
            thickObj.Value = thickness
            thickObj.Join = 0
            thickObj.Mode = 0
            thickObj.Intersection = False
            thickObj.SelfIntersection = False
            getfacename = faced.getFaceName(s[0])
            thickObj.Faces = (currentObj, getfacename,)
            if thickObj.isValid() is False:
                App.ActiveDocument.removeObject(thickObj.Name)
                # Shape != OK
                errMessage = "Failed create shell"
                faced.errorDialog(s,errMessage)
            else:
                App.ActiveDocument.recompute()
                NewJ = App.ActiveDocument.addObject(
                    'Part::Feature', 'Shell')
                NewJ.Shape = thickObj.Shape
                App.ActiveDocument.recompute()
                
                #Preserve color and other properties of the old obj
                faced.PreserveColorTexture(s[0].Object,NewJ)
                
                # Remove Old objects
                for obj in allObjects:
                    App.ActiveDocument.removeObject(obj.Name)
                App.ActiveDocument.removeObject(thickObj.Name)
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
            del allObjects[:]
        except Exception as err:
            App.Console.PrintError("'Part::Shell' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'PartDesign_Shell.svg',
            'MenuText': 'Part_Shell',
            'ToolTip':  'Part Shell'
        }

Gui.addCommand('Design456_Part_Shell', Design456_Part_Shell())


# fillet
class Design456_Part_Fillet:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # One object must be selected at least
                errMessage = "Select a face or an edge use Fillet"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Part Fillet"))
            Radius = QtGui.QInputDialog.getDouble(
                None, "Fillet Radius", "Radius:", 0, 1.0, 20.0, 2)[0]
            if (Radius ==0):
                return
            tempNewObj = App.ActiveDocument.addObject(
                "Part::Fillet", "tempFillet")
            sub1 = s[0]
            tempNewObj.Base = sub1.Object
            names = sub1.SubElementNames
            EdgesToBeChanged = []
            if (len(names) != 0):
                """ we need to take the rest of the string
                            i.e. 'Edge15' --> take out 'Edge'-->4 bytes
                            len('Edge')] -->4
                """
                for name in names:
                    edgeNumbor = int(name[4:len(name)])
                    EdgesToBeChanged.append((edgeNumbor, Radius, Radius))
                print(EdgesToBeChanged)
                tempNewObj.Edges = EdgesToBeChanged
            else:
                errMessage = "Fillet failed. No subelements found"
                faced.errorDialog(errMessage)
                return

            if tempNewObj.isValid() is False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape != OK
                errMessage = "Failed to fillet the objects"
                faced.errorDialog(errMessage)
            else:
                # Make a simple copy of the object
                App.ActiveDocument.recompute()
                newShape = Part.getShape(tempNewObj, '', needSubElement=False, refine=False)
                newObj = App.ActiveDocument.addObject('Part::Feature', 'Fillet')
                newObj.Shape = newShape
                App.ActiveDocument.recompute()
                App.ActiveDocument.ActiveObject.Label = 'Fillet'
                
                #Preserve color and other properties of the old obj
                faced.PreserveColorTexture(s[0].Object,newObj)

                App.ActiveDocument.removeObject(sub1.Object.Name)
                App.ActiveDocument.removeObject(tempNewObj.Name)
            App.ActiveDocument.commitTransaction() #undo reg.
            del EdgesToBeChanged[:]
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Fillet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Fillet.svg',
            'MenuText': 'Part_Fillet',
            'ToolTip':  'Part Fillet'
        }


Gui.addCommand('Design456_Part_Fillet', Design456_Part_Fillet())


# chamfer
class Design456_Part_Chamfer:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1):
                # One object must be selected at least
                errMessage = "Select a face or an edge use Chamfer"
                faced.errorDialog(errMessage)
                return
            App.ActiveDocument.openTransaction(translate("Design456","Part Chamfer"))
            Radius = QtGui.QInputDialog.getDouble(
                None, "Radius", "Radius:", 0, -10000.0, 10000.0, 2)[0]
            if (Radius ==0):
                return  # Nothing to do here
            sub1 = s[0]
            tempNewObj = App.ActiveDocument.addObject(
                "Part::Chamfer", "tempChamfer")
            tempNewObj.Base = sub1.Object
            names = sub1.SubElementNames
            EdgesToBeChanged = []
            if (len(names) != 0):
                for name in names:
                    edgeNumbor = int(name[4:len(name)])
                    EdgesToBeChanged.append((edgeNumbor, Radius, Radius))
                tempNewObj.Edges = EdgesToBeChanged
            else:
                errMessage = "Chamfer failed. No subelements found"
                faced.errorDialog(errMessage)
                return
            # Make a simple copy of the object
            App.ActiveDocument.recompute()
            if tempNewObj.isValid() is False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape != OK
                errMessage = "Failed to fillet the objects"
                faced.errorDialog(errMessage)
            else:
                newShape = Part.getShape(
                    tempNewObj, '', needSubElement=False, refine=False)
                newObj = App.ActiveDocument.addObject(
                    'Part::Feature', 'Chamfer')
                newObj.Shape = newShape
                App.ActiveDocument.recompute()
                App.ActiveDocument.ActiveObject.Label = 'Chamfer'
                
                #Preserve color and other properties of the old obj
                faced.PreserveColorTexture(s[0].Object,newObj)
                                
                App.ActiveDocument.removeObject(sub1.Object.Name)
                App.ActiveDocument.removeObject(tempNewObj.Name)
            del EdgesToBeChanged[:]
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()

        except Exception as err:
            App.Console.PrintError("'Chamfer' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Chamfer.svg',
            'MenuText': 'Part_Chamfer',
            'ToolTip':  'Part Chamfer'
        }


Gui.addCommand('Design456_Part_Chamfer', Design456_Part_Chamfer())


# Simplify Compound
class Design456_SimplifyCompound:
    """[simplify compound object by connecting, refining and simplifying them]

    Argument:
        [Object] :[A compound object to simplify ]. Default is None.
    Returns:
        [Object]: [new simplified and created object(s)]
    """
    def Activated(self,input_object = None):
        try:

            import BOPTools.JoinFeatures
            s=Gui.Selection.getSelection()
            ss=None
            if input_object is None:
                if (len(s) < 1):
                    # One object must be selected at least
                    errMessage = "Select a face or an edge use SimplifyCompound"
                    faced.errorDialog(errMessage)
                    return None
            else:
                s = input_object
            if type(s)==list:
                if len(s)==1:
                    ss = [s[0]]
                else:
                    ss=[s]
            else:
                ss=[s]
            result=[]
            App.ActiveDocument.openTransaction(translate("Design456","SimplifyCompound"))
            for obj in ss:
                #connect Object
                con =  BOPTools.JoinFeatures.makeConnect(name= 'tempConnect') 
                con.Objects=[obj]
                con.Refine=True
                con.Tolerance = 0.0
                con.Proxy.execute(con)
                con.purgeTouched()
                #simple copy of connect. 
                newShape = con.Shape.copy()
                newPart = App.ActiveDocument.addObject('Part::Feature', "Simplified")
                newPart.Shape=newShape
                App.ActiveDocument.recompute()                
                #Preserve color and other properties of the old obj
                faced.PreserveColorTexture(obj,newPart)
                
                App.ActiveDocument.removeObject(con.Name)
                App.ActiveDocument.removeObject(obj.Name)
                result.append(newPart)
            App.ActiveDocument.commitTransaction()  # undo
            return result
            
        except Exception as err:
            App.Console.PrintError("'SimplifyCompound' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'SimplifyCompound.svg',
            'MenuText': 'SimplifyCompound',
            'ToolTip':  'Simplify Compound'
        }

Gui.addCommand('Design456_SimplifyCompound', Design456_SimplifyCompound())


class Design456_DivideCylinder:

    def Activated(self):
        self.frmSlice=None
        self.spinSections=None
        self.spinAngel=None
        self.spinAxisX=None
        self.spinAxisY=None
        self.spinAxisZ=None
        self.Axis=App.Vector(0.0,0.0,1.0)
        self.XY_Angle=0
        self.Sections=1
        pl = App.Placement()
        pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        pl.Base = App.Vector(0.0, 0.0, 0.0)
        self.selected=Gui.Selection.getSelectionEx()
        self.selObj=self.selected[0].Object
        if len(self.selected)==0:
            errMessage="Please select an object"
            faced.errorDialog(errMessage)
            return
        self.createDialog()
        
    def createSplittedObj(self):
        import BOPTools.SplitFeatures
        try:
            slicedObj = BOPTools.SplitFeatures.makeSlice(name= 'Slice')
            self.boundary=self.selObj.Shape.BoundBox
            x1=self.boundary.XMin
            y1=self.boundary.Center.y 
            x2=self.boundary.XMax
            y2=self.boundary.Center.y+self.boundary.YLength/2
            z1=self.boundary.ZMin
            z2=self.boundary.ZMax
            plS = App.Placement()
            plS.Rotation= (0.0, 0.0, 1.0,0.0)
            plS.Rotation.Angle=self.XY_Angle
            plS.Base = App.Vector(x1,y1,z1)
            
            p=Part.makePolygon([App.Vector(x1,y1,z1),
                                App.Vector(x1,y1,z2),
                                App.Vector(x2,y1,z2),
                                App.Vector(x2,y1,z1),
                                App.Vector(x1,y1,z1)])
            f=Part.Face(Part.Wire(p))
            fObj=App.ActiveDocument.addObject('Part::Feature', "cutterF")
            fObj.Placement=plS
            fObj.Shape = f

            rectangles=[]
            print(self.Sections)
            if (self.Sections>1):
                angleSliced=360/self.Sections     
                for i in range(0,self.Sections):
                    fObj=App.ActiveDocument.addObject('Part::Feature', "cutterF")
                    fObj.Placement=plS
                    fObj.Placement.Rotation.Axis=self.Axis
                    fObj.Placement.Rotation.Angle=math.radians(self.XY_Angle+angleSliced*i)
                    fObj.Shape=f.copy()
                    rectangles.append(fObj)
            else:
                rectangles.append(fObj)
                fObj.Placement.Rotation.Axis=self.Axis
                fObj.Placement.Rotation.Angle=math.radians(self.XY_Angle)

            slicedObj.Base = self.selObj
            slicedObj.Tools = rectangles
            objFinal=App.ActiveDocument.addObject('Part::Feature', "Splitted")
            objFinal.Placement=self.selObj.Placement
            App.ActiveDocument.recompute()
            objFinal.Shape=slicedObj.Shape.copy()
            self.selObj.Visibility=False
            App.ActiveDocument.recompute()
            # for obj in rectangles:
            #     App.ActiveDocument.removeObject(obj.Name)

            # App.ActiveDocument.removeObject(slicedObj.Name)
            
        except Exception as err:
            App.Console.PrintError("'createDialog' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def createDialog(self):
        try:
            self.frmSlice=QtGui.QDialog()
            self.frmSlice.setObjectName("frmSlice")
            self.frmSlice.resize(379, 126)
            self.spinSections = QtGui.QSpinBox(self.frmSlice)
            self.spinSections.setGeometry(QtCore.QRect(70, 10, 91, 22))
            self.spinSections.setProperty("value", 1)
            self.spinSections.setObjectName("spinSections")
            self.spinAngel = QtGui.QDoubleSpinBox(self.frmSlice)
            self.spinAngel.setGeometry(QtCore.QRect(70, 40, 91, 22))
            self.spinAngel.setObjectName("spinAngel")
            self.label_2 = QtGui.QLabel(self.frmSlice)
            self.label_2.setGeometry(QtCore.QRect(10, 40, 49, 16))
            self.label_2.setObjectName("label_2")
            self.label_4 = QtGui.QLabel(self.frmSlice)
            self.label_4.setGeometry(QtCore.QRect(10, 10, 49, 16))
            self.label_4.setObjectName("label_4")
            self.label_3 = QtGui.QLabel(self.frmSlice)
            self.label_3.setGeometry(QtCore.QRect(10, 90, 49, 16))
            self.label_3.setObjectName("label_3")
            self.spinAxisX = QtGui.QDoubleSpinBox(self.frmSlice)
            self.spinAxisX.setGeometry(QtCore.QRect(60, 90, 51, 22))
            self.spinAxisX.setObjectName("spinAxisX")
            self.spinAxisY = QtGui.QDoubleSpinBox(self.frmSlice)
            self.spinAxisY.setGeometry(QtCore.QRect(110, 90, 51, 22))
            self.spinAxisY.setObjectName("spinAxisY")
            self.spinAxisZ = QtGui.QDoubleSpinBox(self.frmSlice)
            self.spinAxisZ.setGeometry(QtCore.QRect(160, 90, 51, 22))
            self.spinAxisZ.setProperty("value", 1.0)
            self.spinAxisZ.setObjectName("spinAxisZ")
            self.label_5 = QtGui.QLabel(self.frmSlice)
            self.label_5.setGeometry(QtCore.QRect(70, 70, 21, 16))
            self.label_5.setObjectName("label_5")
            self.label_6 = QtGui.QLabel(self.frmSlice)
            self.label_6.setGeometry(QtCore.QRect(120, 70, 21, 16))
            self.label_6.setObjectName("label_6")
            self.label_7 = QtGui.QLabel(self.frmSlice)
            self.label_7.setGeometry(QtCore.QRect(170, 70, 21, 16))
            self.label_7.setObjectName("label_7")
            self.buttonBox = QtGui.QDialogButtonBox(self.frmSlice)
            self.buttonBox.setGeometry(QtCore.QRect(220, 90, 156, 24))
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
            self.buttonBox.setObjectName("buttonBox")

            self.spinAngel.valueChanged.connect(self.Angel_cb)
            self.spinSections.valueChanged.connect(self.Section_cb)
            
            self.spinAxisX.valueChanged.connect(self.XYZ_cb)
            self.spinAxisY.valueChanged.connect(self.XYZ_cb)
            self.spinAxisZ.valueChanged.connect(self.XYZ_cb)
            
            self.buttonBox.accepted.connect(self.OK_cb)
            self.buttonBox.rejected.connect(self.Cancel_cb)

            _translate = QtCore.QCoreApplication.translate
            self.frmSlice.setWindowTitle(_translate("frmSlice", "Slice Object"))
            self.label_2.setText(_translate("frmSlice", "Angel"))
            self.label_4.setText(_translate("frmSlice", "Sections"))
            self.label_3.setText(_translate("frmSlice", "Axis"))
            self.label_5.setText(_translate("frmSlice", "X"))
            self.label_6.setText(_translate("frmSlice", "Y"))
            self.label_7.setText(_translate("frmSlice", "Z"))
            self.frmSlice.show()
            
        except Exception as err:
            App.Console.PrintError("'createDialog' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)    
            
    #callbacks
    def OK_cb(self):
        self.Sections=self.spinSections.value()
        self.XY_Angle=self.spinAngel.value()
        self.Axis=App.Vector(self.spinAxisX.value(),
                             self.spinAxisY.value(),
                             self.spinAxisZ.value())
        self.frmSlice.hide()
        del self.frmSlice
        self.createSplittedObj()
            
    def Cancel_cb(self):
        self.frmSlice.hide()
        del self.frmSlice
    
    def Section_cb(self):
        print("changed")
        print(self.spinSections.value())
        self.Sections=self.spinSections.value()
    
    def Angel_cb(self):
        self.XY_Angle=self.spinAngel.value()
    
    def XYZ_cb(self):
        self.Axis=App.Vector(self.spinAxisX.value(),
                             self.spinAxisY.value(),
                             self.spinAxisZ.value())

    def GetResources(self):
        return {'Pixmap':Design456Init.ICON_PATH + 'DivideCylinder.svg',
                'MenuText': "DivideCylinder",
                'ToolTip': "Generate a DivideCylinder"}

Gui.addCommand('Design456_DivideCylinder', Design456_DivideCylinder())
##########################################################################


class Design456_3DToolsGroup:
        
    """Design456 Part 3D Tools"""

    def GetCommands(self):
        """3D Modifying Tools."""
        return ("Design456_Extrude",
                "Design456_Extract",
                "Design456_Part_Merge",
                "Design456_SimplifyCompound",
                "Design456_Part_Subtract",
                "Design456_Part_Intersect",
                "Design456_loftOnDirection",
                "Design456_Part_Group",
                "Design456_Part_Compound",
                "Design456_Part_Shell",
                "Design456_DivideCylinder",
                "Design456_SplitObject",
                "Design456_Part_Fillet",
                "Design456_Part_Chamfer",
                "Design456_LoftBetweenFaces",
                "Design456_unifySplitFuse2",
                "Design_ColorizeObject"
                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools for modifying 3D Shapes")
        return {'Pixmap':  Design456Init.ICON_PATH+ 'Design456_3DTools.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "3Dtools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_3DToolsGroup", Design456_3DToolsGroup())

