# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                         *
# *  This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                         *
# *  Copyright (C) 2022                                                    *
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
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft as _draft
import Part
import Design456Init
import FACE_D as faced
from draftutils.translate import translate  # for translation
from  Design456_2Ddrawing import Design456_SimplifiedFace  
import Mesh
import MeshPart
from Design456_3DTools import Design456_SimplifyCompound

__updated__ = '2022-08-04 21:31:34'


class Design456_CommonFace:
    """[Create a new shape that is the common between two other shapes.]

    """
    def Activated(self):
        App.ActiveDocument.openTransaction(
            translate("Design456", "CommonFace"))
        s=Gui.Selection.getSelectionEx()
        newshape=None
        for obj in s:
            if obj.HasSubObjects:
                sh1=obj.SubObjects[0]
            else:
                sh1=obj.Object.Shape
            if newshape is not None:
                newshape= newshape.common(sh1)
            else:
                newshape= sh1
            App.ActiveDocument.recompute()
        newobj = App.ActiveDocument.addObject("Part::Feature", "CommonFace")
        newobj.Shape=newshape
        App.ActiveDocument.recompute()
        for obj in s:
            App.ActiveDocument.removeObject(obj.Object.Name)
        App.ActiveDocument.recompute()
        App.ActiveDocument.commitTransaction()  # undo reg.de here


    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'CommonFace.svg',
            'MenuText': 'CommonFace',
            'ToolTip':  'CommonFace between 2-2D Faces'
        }


Gui.addCommand('Design456_CommonFace', Design456_CommonFace())


# Subtract faces


class Design456_SubtractFaces:
    def Activated(self):
        App.ActiveDocument.openTransaction(
            translate("Design456", "SubtractFace"))
        s=Gui.Selection.getSelectionEx()
        newshape=None
        for obj in s:
            if obj.HasSubObjects:
                sh1=obj.SubObjects[0]
            else:
                sh1=obj.Object.Shape
            if newshape is not None:
                newshape= newshape.cut(sh1)
            else:
                newshape= sh1
            App.ActiveDocument.recompute()
        newobj = App.ActiveDocument.addObject("Part::Feature", "SubtractFace")
        newobj.Shape=newshape
        App.ActiveDocument.recompute()
        for obj in s:
            App.ActiveDocument.removeObject(obj.Object.Name)
        App.ActiveDocument.recompute()
        App.ActiveDocument.commitTransaction()  # undo reg.de here

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'SubtractFace.svg',
            'MenuText': 'Subtract Faces',
            'ToolTip':  'Subtract 2-2D Faces'
        }


Gui.addCommand('Design456_SubtractFaces', Design456_SubtractFaces())

# Combine two faces


class Design456_CombineFaces:
    def Activated(self):

        App.ActiveDocument.openTransaction(
            translate("Design456", "CombineFaces"))
        s=Gui.Selection.getSelectionEx()
        newshape=None
        for obj in s:
            if obj.HasSubObjects:
                sh1=obj.SubObjects[0]
            else:
                sh1=obj.Object.Shape
            if newshape is not None:
                newshape= newshape.fuse(sh1)
            else:
                newshape= sh1
            App.ActiveDocument.recompute()
        newobj = App.ActiveDocument.addObject("Part::Feature", "CombineFaces")
        newobj.Shape=newshape
        App.ActiveDocument.recompute()
        for obj in s:
            App.ActiveDocument.removeObject(obj.Object.Name)
        App.ActiveDocument.recompute()
        simp= Design456_SimplifiedFace()
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(App.ActiveDocument.Name,newobj.Name)
        simp.Activated()
        App.ActiveDocument.recompute()
        App.ActiveDocument.commitTransaction()  # undo reg.de here

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'CombineFaces.svg',
            'MenuText': 'Combine Face',
            'ToolTip':  'Combine 2-2D Faces'
        }


Gui.addCommand('Design456_CombineFaces', Design456_CombineFaces())
# Surface between two line


class Design456Part_Surface:

    def Activated(self):
        try:

            s = Gui.Selection.getSelectionEx()
            if (len(s) < 1 or len(s) > 2):
                # Two object must be selected
                errMessage = "Select two edges or two wire to make a face or "
                faced.errorDialog(errMessage)
                return
            elementsName = None
            subObj = None
            obj1=None
            obj2=None
            if len(s)==1:
                obj1shp= s[0].SubObjects[0].copy()
                obj1=App.ActiveDocument.addObject('Part::Feature',"E1")
                obj1.Shape=obj1shp
                obj2shp= s[0].SubObjects[1].copy()
                obj2=App.ActiveDocument.addObject('Part::Feature',"E2")
                obj2.Shape=obj2shp
                App.ActiveDocument.recompute()
                elementsName=[obj1.Name, obj2.Name]
                subObj = [obj1, obj2]
            elif len(s)==2 :
                obj1shp= s[0].SubObjects[0].copy()
                obj1=App.ActiveDocument.addObject('Part::Feature',"E1")
                obj1.Shape=obj1shp
                obj2shp= s[1].SubObjects[0].copy()               
                obj2=App.ActiveDocument.addObject('Part::Feature',"E2")
                obj2.Shape=obj2shp
                elementsName=[obj1.Name, obj2.Name]
                subObj = [obj1, obj2]
            for ss in s:
                word = ss.FullName
                if(word.find('Vertex') != -1):
                    # Two lines or curves or wires must be selected
                    errMessage = "Select two edges or two wires not Vertex"
                    faced.errorDialog(errMessage)
                    return
            App.ActiveDocument.openTransaction(
                translate("Design456", "Surface"))

            newObj = App.ActiveDocument.addObject(
                'Part::RuledSurface', 'tempSurface')

            newObj.Curve1 = subObj[0]
            newObj.Curve2 = subObj[1]
            App.ActiveDocument.recompute()
            
            # Make a simple copy of the object
            newShape = Part.getShape(
                newObj, '', needSubElement=False, refine=True)
            tempNewObj = App.ActiveDocument.addObject(
                'Part::Feature', 'Surface')
            tempNewObj.Shape = newShape
            App.ActiveDocument.ActiveObject.Label = 'Surface'
            App.ActiveDocument.recompute()
            if tempNewObj.isValid() is False:
                App.ActiveDocument.removeObject(tempNewObj.Name)
                # Shape != OK
                errMessage = "Failed to create the face"
                faced.errorDialog(errMessage)
            else:
                App.ActiveDocument.removeObject(newObj.Name)
                App.ActiveDocument.commitTransaction()  # undo reg.de here
                App.ActiveDocument.recompute()
                if (obj1 is not None and obj2 is not None):
                    App.ActiveDocument.removeObject(obj1.Name)
                    App.ActiveDocument.removeObject(obj2.Name)

        except Exception as err:
            App.Console.PrintError("'Part Surface' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Surface.svg',
            'MenuText': 'Part_Surface',
            'ToolTip':  'Part Surface'
        }


Gui.addCommand('Design456Part_Surface', Design456Part_Surface())

#########################



class Design456_ArcFace6Points:
    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(
                translate("Design456", "ArcFace6Points"))
            selected = Gui.Selection.getSelectionEx() 
            '''
                Kind of selections: 
                1-Three objects  - 2 Vertexes per each 
                2-mixed objects with different vertexes (2 objects three vertex each, 4 vertex 2-1-3 ..etc)
                3- Six vertexes (6 objects)

                For each object we take first vertex as row 1, second as row 2 if we have more than 1 object
                

            
            '''
            firstRow=[]
            secondRow=[]
            allSelected = []
            if len(selected)==1:
                #We have one object with 6 vertexes selected - 1-3 must be first row, 4-6 must be second row
                firstRow.append(selected[0].SubObjects[0].Point)                
                firstRow.append(selected[0].SubObjects[1].Point)                
                firstRow.append(selected[0].SubObjects[2].Point)                
                secondRow.append(selected[0].SubObjects[3].Point)                
                secondRow.append(selected[0].SubObjects[4].Point)                
                secondRow.append(selected[0].SubObjects[5].Point)                

            elif len(selected)==2:
                # we have two objects, each object must have 3 vertexes which is a row 
                firstRow.append(selected[0].SubObjects[0].Point)                
                firstRow.append(selected[0].SubObjects[1].Point)                
                firstRow.append(selected[0].SubObjects[2].Point)                
                secondRow.append(selected[1].SubObjects[0].Point)                
                secondRow.append(selected[1].SubObjects[1].Point)                
                secondRow.append(selected[1].SubObjects[2].Point)                
            elif len(selected)==3:
                #We have three objects. Must be with 2 vertex each . 
                # First are first row, second vertex for each are second row
                for obj in selected:
                    if len(obj.SubObjects)>1:
                        firstRow.append (obj.SubObjects[0].Point)
                        secondRow.append(obj.SubObjects[1].Point)
                    else:
                        errMessage = "Please select 2 vertexes on each object"
                        faced.errorDialog(errMessage)
                        return                    
            elif len(selected)==4 or len(selected)==5:
                # this can be a combination of different things. 
                #Still we take first vertexes as first row, and second vertexes as second row. 
                first=0
                second=0
                if len(selected[0])>1:
                    firstRow.append(selected[0].SubObjects[0].Point)
                    secondRow.append(selected[0].SubObjects[1].Point)
                    first+=1
                    second+=1
                else:
                    first+=1
                    firstRow.append(selected[0].SubObjects[0].Point)
                if len(selected[1])>1:
                    firstRow.append(selected[1].SubObjects[0].Point)
                    secondRow.append(selected[1].SubObjects[0].Point)
                    first+=1
                    second+=1
                else:
                    first+=1
                    firstRow.append(selected[0].SubObjects[0].Point)
                if len(selected[2])>1:
                    firstRow.append(selected[1].SubObjects[0].Point)
                    secondRow.append(selected[1].SubObjects[0].Point)
                    first+=1
                    second+=1
                else:
                    first+=1
                    firstRow.append(selected[0].SubObjects[0].Point)
                if len(selected[3])>1:
                    if firstRow==3:
                        #First row is finished
                        secondRow.append(selected[3].SubObjects[0].Point)
                        secondRow.append(selected[3].SubObjects[1].Point)
                    else:
                        firstRow.append(selected[3].SubObjects[0].Point)
                        secondRow.append(selected[3].SubObjects[1].Point)
                else:
                    if firstRow==3:
                        #First row is finished
                        secondRow.append(selected[3].SubObjects[0].Point)
                    else:
                        errMessage = "Selection error please try again"
                        faced.errorDialog(errMessage)
                        return 
                            
            elif len(selected)==6:
                if selected[0].HasSubObjects:
                    firstRow.append(selected[0].SubObjects[0].Point)
                    firstRow.append(selected[1].SubObjects[0].Point)
                    firstRow.append(selected[2].SubObjects[0].Point)

                    secondRow.append(selected[3].SubObjects[0].Point)
                    secondRow.append(selected[4].SubObjects[0].Point)
                    secondRow.append(selected[5].SubObjects[0].Point)
                else:
                    firstRow.append(selected[0].Object.Shape.Vertexes[0].Point)
                    firstRow.append(selected[1].Object.Shape.Vertexes[0].Point)
                    firstRow.append(selected[2].Object.Shape.Vertexes[0].Point)
                    secondRow.append(selected[3].Object.Shape.Vertexes[0].Point)
                    secondRow.append(selected[4].Object.Shape.Vertexes[0].Point)
                    secondRow.append(selected[5].Object.Shape.Vertexes[0].Point)
            
            allSelected=firstRow+secondRow
            C1 = Part.Arc(App.Vector(allSelected[0]), App.Vector(
                allSelected[1]), App.Vector(allSelected[2]))
            C2 = Part.Arc(App.Vector(allSelected[3]), App.Vector(
                allSelected[4]), App.Vector(allSelected[5]))
            
            sel1 = C1.toShape()
            sel2 = C2.toShape()
            W1 = Part.Wire(sel1.Edges)
            W2 = Part.Wire(sel2.Edges)
            newObj = App.ActiveDocument.addObject(
                'Part::RuledSurface', 'Test')
            obj1=App.ActiveDocument.addObject('Part::Feature',"E1")
            obj1.Shape=W1
            obj2=App.ActiveDocument.addObject('Part::Feature',"E2")
            obj2.Shape=W2
            newObj.Curve1 = obj1
            newObj.Curve2 = obj2
            App.ActiveDocument.recompute()
            finalObj = App.ActiveDocument.addObject(
                'Part::Feature', 'ArcFace6Points')
            
            finalObj.Shape=newObj.Shape.copy()
            
            App.ActiveDocument.removeObject(newObj.Name)            
            App.ActiveDocument.removeObject(obj1.Name)
            App.ActiveDocument.removeObject(obj2.Name)
            
            App.ActiveDocument.recompute()
            del allSelected[:]
            App.ActiveDocument.commitTransaction()  # undo

        except Exception as err:
            App.Console.PrintError("'ArcFace6Points' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'ArcFace6Points.svg',
            'MenuText': 'ArcFace6Points',
                        'ToolTip':  'ArcFace 6 Points'
        }

Gui.addCommand('Design456_ArcFace6Points', Design456_ArcFace6Points())



# Segment a face from 3D object or 2D object
class Design456_SegmentAFace:
    def __init__(self):
        self.sel=None
        self.Segments=10
        self.SingleFace=False
        self.oldFace=None
        
    def selectedOptions(self):
        from DefeaturingWB.DefeaturingTools import sewShape
        self.Segments=self.inpINTSegments.value()
        if self.radAll.isChecked():
            self.SingleFace=False
        elif self.radOneFace.isChecked():
            self.SingleFace=True
        self.frmMain.hide()
        self.oldFace=None
        try:
            self.sel=Gui.Selection.getSelectionEx()[0]
            if hasattr(self.sel,"HasSubObjects"):
                if self.sel.HasSubObjects:
                   self.oldFace=self.sel.SubObjects
            
            App.ActiveDocument.openTransaction(translate("Design456","SegmentAFace"))
            self.sel.Object.Visibility= False
            mesh = self.divideFace()
            _solid = self.collectFace(mesh) 
            App.ActiveDocument.removeObject(mesh.Name)
            #undo

            newObj=App.ActiveDocument.addObject('Part::Feature', "SegmentAFace")
            result=sewShape([_solid])
            newObj.Shape=result[0].Shape.copy()
            App.ActiveDocument.removeObject(_solid.Name)
            App.ActiveDocument.removeObject(result[0].Name)
            App.ActiveDocument.commitTransaction() #undo reg.
        
        except Exception as err:
            App.Console.PrintError("'Design456_SegmentAFace' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)        
    
    def hide(self):
        self.frmMain.hide()
        return
    
    def createDialog(self):
        self.frmMain=QtGui.QDialog()
        self.frmMain.setObjectName("frmMain")
        self.frmMain.resize(374, 200)
        self.frmMain.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Europe))
        self.frmMain.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(self.frmMain)
        self.buttonBox.setGeometry(QtCore.QRect(30, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonGroup =   QtGui.QButtonGroup(self.frmMain)
        self.buttonGroup.setObjectName("buttonGroup")
        self.radOneFace = QtGui.QRadioButton(self.frmMain)
        self.radOneFace.setGeometry(QtCore.QRect(20, 20, 130, 20))
        self.radOneFace.setObjectName("radOneFace")
        self.radAll = QtGui.QRadioButton(self.frmMain)
        self.radAll.setGeometry(QtCore.QRect(20, 50, 89, 20))
        self.radAll.setObjectName("radAll")
        self.inpINTSegments = QtGui.QSpinBox(self.frmMain)
        self.inpINTSegments.setGeometry(QtCore.QRect(210, 60, 130, 22))
        self.inpINTSegments.setObjectName("inpINTSegments")
        self.label = QtGui.QLabel(self.frmMain)
        self.label.setGeometry(QtCore.QRect(210, 40, 130, 16))
        self.label.setObjectName("label")
        self.buttonGroup.addButton(self.radOneFace)
        self.buttonGroup.addButton(self.radAll)
        self.radAll.setChecked(True)
        self.inpINTSegments.setValue(10)
        self.inpINTSegments.setMaximum (10000)
        self.inpINTSegments.setMinimum(1)
        
        _translate = QtCore.QCoreApplication.translate
        self.frmMain.setWindowTitle(_translate("frmMain", "Select Face and Segments size"))
        self.radOneFace.setText(_translate("frmMain", "Only selected face"))
        self.radAll.setText(_translate("frmMain", "All faces"))
        self.label.setText(_translate("frmMain", "Segments"))
   
        self.buttonBox.accepted.connect(self.selectedOptions)
        self.buttonBox.rejected.connect(self.hide)
        QtCore.QMetaObject.connectSlotsByName(self.frmMain)
        self.frmMain.show()
   
    def Activated(self):
        self.createDialog()

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'SegmentAFace.svg',
            'MenuText': 'SegmentAFace',
            'ToolTip':  'Segment A Face'
        }

    def divideFace(self):
        try:
            mesh = App.ActiveDocument.addObject("Mesh::Feature", "Mesh")
            shp=None
            if self.SingleFace is False:
                shp = self.sel.Object.Shape    
            else:   
                shp = self.sel.SubObjects[0]
            mesh.Mesh = MeshPart.meshFromShape(
                        Shape=shp,
                        LinearDeflection=5/self.Segments,
                        AngularDeflection=10/2.5,
                        Relative=False)

            App.ActiveDocument.recompute()

            return mesh

        except Exception as err:
            App.Console.PrintError("'devideFace' Failed. "
                                    "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def collectFace(self,obj,swe=0.1):
        try:
            #sel=Gui.Selection.getSelectionEx()[0]
            simplify=Design456_SimplifyCompound()
            mesh = obj.Mesh
            shape = Part.Shape()
            shape.makeShapeFromMesh(mesh.Topology, swe) 
            compShp=Part.makeCompound(shape)
            newSolid = App.ActiveDocument.addObject('Part::Feature', "tempSegmentAFace")

            if self.SingleFace is False:
                newObj = App.ActiveDocument.addObject('Part::Feature', "collectFace")
                newObj.Shape = shape
                App.ActiveDocument.recompute()
                temp=simplify.Activated(newObj)[0]
                
                newSolid.Shape = temp.Shape.copy()
                newSolid.Placement=temp.Placement
                App.ActiveDocument.removeObject(temp.Name)
            else:
                tempShape=faced.EqualizeFaces(self.sel.Object,self.sel.SubObjects[0],compShp)
                newSolid.Shape =tempShape.Shape.copy()
                App.ActiveDocument.removeObject(tempShape.Name)
                App.ActiveDocument.recompute()
            return newSolid
            

        except Exception as err:
            App.Console.PrintError("'SegmentAFace' Failed. "
                                    "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

Gui.addCommand('Design456_SegmentAFace', Design456_SegmentAFace())

######################################################################

"""    
        Unfortunately, I couldn't find a solution and I don't want to waste more time at the moment
        on this tool. I leave it for now, and comment the code. Maybe when I find a solution 
        I come back to it. 
        The problem is that there is no way to reset  face's placement. It can have an Axis and a rotation axis
        which means double rotation. Resetting that with the weird rotation mechanism in FreeCAD is not easy. 
"""
# class Design456_EqualizeFaces:
#     def __init__(self):
#         self.dialog= None
#         self.sel1=None
#         self.sel2=None
        
#     """[Use this tool to equalize two faces (copy first, replace second with the copied face).]

#     """
#     def Activated(self):
#         try:
#             from Design456_Alignment import Design456_ResetPlacements 
#             sel=Gui.Selection.getSelectionEx()
#             newshape=None
#             if len(sel)<2 or len(sel)>2 :
#             #error message
#                 # Two object must be selected
#                 errMessage = "Select two faces to use the tool "
#                 faced.errorDialog(errMessage)
#                 return
#             f1=sel[0].SubObjects[0]
#             f2=sel[1].SubObjects[0]
#             if type(f1)!=Part.Face or type(f2)!=Part.Face:
#                 errMessage = "Select two faces to use the tool "
#                 faced.errorDialog(errMessage)
#                 return
#             self.dialog = self.getMainWindow()
#             #We must reset placement for each object otherwise this tool is impossible

#             App.ActiveDocument.openTransaction(translate("Design456", "EqualizeFaces"))
#             restedObj=Design456_ResetPlacements([sel[0].Object,sel[1].Object]).Activated() 
#             self.sel1=restedObj[0]
#             self.sel2=restedObj[1]

#         except Exception as err:
#             App.Console.PrintError("'EqualizeFaces' Failed. "
#                                     "{err}\n".format(err=str(err)))
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
            
        
#     def getMainWindow(self):
#         """[Create the tab for the tool]
#         """
#         try:
#             toplevel = QtGui.QApplication.topLevelWidgets()
#             self.mw = None
#             for i in toplevel:
#                 if i.metaObject().className() == "Gui::MainWindow":
#                     self.mw = i
#             if self.mw is None:
#                 raise Exception("No main window found")
#             dw = self.mw.findChildren(QtGui.QDockWidget)
#             for i in dw:
#                 if str(i.objectName()) == "Combo View":
#                     self.tab = i.findChild(QtGui.QTabWidget)
#                 elif str(i.objectName()) == "Python Console":
#                     self.tab = i.findChild(QtGui.QTabWidget)
#             if self.tab is None:
#                 raise Exception("No tab widget found")
#             oldsize = self.tab.count()
#             self.dialog = QtGui.QDialog()
#             self.tab.addTab(self.dialog, "Replace Face")
#             self.dialog.resize(200, 450)
#             self.lblReplace = QtGui.QLabel(self.dialog)
#             self.lblReplace.setGeometry(QtCore.QRect(10, 0, 191, 61))
#             font = QtGui.QFont()
#             font.setPointSize(10)
#             self.lblTitle = QtGui.QLabel(self.dialog)
#             self.lblTitle.setGeometry(QtCore.QRect(10, 10, 300, 91))
#             font = QtGui.QFont()
#             font.setFamily("Times New Roman")
#             font.setPointSize(10)
#             self.lblTitle.setFont(font)
#             self.lblTitle.setObjectName("lblTitle")
#             _translate = QtCore.QCoreApplication.translate
#             self.dialog.setWindowTitle(_translate("Dialog", "Replace Face"))
#             self.lblTitle.setText(_translate("Dialog", "(Replace Face)\n"
#                                              "Tweak an object by replacing faces or equalize them"))
#             self.formLayoutWidget_2 = QtGui.QWidget(self.dialog)
#             self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 100, 400, 300))
#             self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
#             self.radioXdir = QtGui.QRadioButton(self.formLayoutWidget_2)
#             self.radioXdir.setObjectName("xDir")
#             self.radioYdir = QtGui.QRadioButton(self.formLayoutWidget_2)
#             self.radioYdir.setObjectName("yDir")
#             self.radioZdir = QtGui.QRadioButton(self.formLayoutWidget_2)
#             self.radioZdir.setObjectName("zDir")
#             self.radioXdir.setGeometry(QtCore.QRect(10, 120, 100, 30))
#             self.radioYdir.setGeometry(QtCore.QRect(10, 150, 100, 30))
#             self.radioZdir.setGeometry(QtCore.QRect(10, 180, 100, 30))

#             self.radioXdir.setText(_translate("Dialog", "X-Dir"))
#             self.radioYdir.setText(_translate("Dialog", "Y-Dir"))
#             self.radioZdir.setText(_translate("Dialog", "Z-Dir"))
#             self.radioZdir.setChecked(1)  # default
            
#             font = QtGui.QFont()
#             font.setPointSize(10)
#             font.setBold(True)
#             font.setWeight(75)
#             self.btnOK = QtGui.QDialogButtonBox(self.dialog)
#             self.btnOK.setGeometry(QtCore.QRect(200, 300, 190, 61))
#             self.btnOK.setFont(font)
#             self.btnOK.setObjectName("btnOK")
#             self.btnOK.setStandardButtons(
#                 QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
#             self.btnOK.accepted.connect(self.OK_cb)
#             self.btnOK.rejected.connect(self.Cancel_cb)
            
#             QtCore.QMetaObject.connectSlotsByName(self.dialog)
#             self.tab.setCurrentWidget(self.dialog)
#             return self.dialog

#         except Exception as err:
#             App.Console.PrintError("'Activated' Failed. "
#                                    "{err}\n".format(err=str(err)))
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
            
#     def hide(self):
#         try:
#             self.dialog.hide()
#             del self.dialog
#             dw = self.mw.findChildren(QtGui.QDockWidget)
#             newsize = self.tab.count()
#             self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
#             faced.showFirstTab()
        
#         except Exception as err:
#             App.Console.PrintError("'Hide' Failed. "
#                                    "{err}\n".format(err=str(err)))
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
        
#     def EqualizeFaces(self):
       
#         App.ActiveDocument.openTransaction(
#             translate("Design456", "EqualizeFaces")) #Record undo        
#         newShape= App.ActiveDocument.addObject('Part::Feature',self.sel2.Name)
#         newShape.Shape=self.sel1.Shape.copy()
#         App.ActiveDocument.recompute()
#         pl1=self.sel1.Placement
        
#         # X1min=self.sel1.Shape.BoundBox.XMin
#         # Y1min=self.sel1.Shape.BoundBox.YMin
#         # Z1min=self.sel1.Shape.BoundBox.ZMin
#         # X1max=self.sel1.Shape.BoundBox.XMax
#         # Y1max=self.sel1.Shape.BoundBox.YMax
#         # Z1max=self.sel1.Shape.BoundBox.ZMax

#         # X2min=self.sel2.Shape.BoundBox.XMin
#         # Y2min=self.sel2.Shape.BoundBox.YMin
#         # Z2min=self.sel2.Shape.BoundBox.ZMin
#         # X2max=self.sel2.Shape.BoundBox.XMax
#         # Y2max=self.sel2.Shape.BoundBox.YMax
#         # Z2max=self.sel2.Shape.BoundBox.ZMax

#         newShape.Placement=self.sel2.Placement.copy()
#         newShape.Placement.Rotation.Axis=self.Shape.CenterOfMass
#         newShape.Placement.Rotation.Angle=self.Shape.SubShapes[0].Surface.Rotation.Angle

#         App.ActiveDocument.removeObject(self.sel2.Name)
#         App.ActiveDocument.recompute()
#         App.ActiveDocument.commitTransaction()  # undo reg.de here

    
#     def OK_cb(self):
#         self.EqualizeFaces()
#         self.hide()
        
#     def Cancel_cb(self):
#         self.hide()
    
#     def GetResources(self):
#         return{
#             'Pixmap':   Design456Init.ICON_PATH + 'EqualizeFaces.svg',
#             'MenuText': 'EqualizeFaces',
#             'ToolTip':  'EqualizeFaces between 2-2D Faces'
#         }


# Gui.addCommand('Design456_EqualizeFaces', Design456_EqualizeFaces())



# ##############################
"""Design456 Part 2D Tools"""


class Design456_2DToolsGroup:
    def __init__(self):
        return

    """Gui command for the group of 2D tools."""

    def GetCommands(self):
        """2D Face commands."""
        return ("Design456Part_Surface",
                "Design456_ArcFace6Points",
                "Design456_CombineFaces",
                "Design456_SubtractFaces",
                "Design456_CommonFace",
                "Design456_SegmentAFace",
                "Design456_EqualizeFaces",

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools for modifying 2D Shapes")
        return {'Pixmap':  Design456Init.ICON_PATH + 'Design456_2DTools.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "2Dtools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_2DToolsGroup", Design456_2DToolsGroup())
