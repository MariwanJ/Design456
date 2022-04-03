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
import os
import sys
import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft as _draft
import Part as _part
import FACE_D as faced
import Design456Init
from draftutils.translate import translate  # for translation
from pivy import coin
import DirectModeling.Design456_SmartAlignment
import DirectModeling.Design456_SmartMove
import Design456_Magnet
from ThreeDWidgets.constant import FR_SELECTION
# Toolbar class
# Based  on https://forum.freecadweb.org/viewtopic.php?style=4&f=22&t=29138&start=20
__updated__ = '2022-04-03 19:38:11'


#TODO:FIXME: Don't know if this is a useful tool to have
class Design456_ViewInsideObjects:
    """
        View internal walls, core of objects in the 3D view

    """

    def Activated(self):
        try:
            clip_plane = coin.SoClipPlaneManip()
            clip_plane.setValue(coin.SbBox3f(
                4, 4, 4, 8, 8, 8), coin.SbVec3f(-1, -1, -1), 1)
            Gui.ActiveDocument.ActiveView.getSceneGraph().insertChild(clip_plane, 1)
            Gui.ActiveDocument.ActiveView.viewAxonometric()
            Gui.ActiveDocument.ActiveView.fitAll()

        except Exception as err:
            App.Console.PrintError("'View Inside objects' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'ViewInsideObjects.svg',
            'MenuText': 'View Inside objects',
            'ToolTip':  'View Inside objects'
        }


Gui.addCommand('Design456_ViewInsideObjects', Design456_ViewInsideObjects())


"""Design456_Alignment"""

# Object Alignment


class Design456_AlignFlatToPlane:
    """[Align the selected object to the current draft working plane]
    """
    def Activated(self):
        try:
            Selectedobjects = Gui.Selection.getSelectionEx()
            for obj in Selectedobjects:
                #Get the placement of the plane and project location of the object on the plane
                #Use it as new placement
                obj.Object.Placement.Base = App.DraftWorkingPlane.projectPoint(obj.Object.Placement.Base)
                #TODO: FIXME: Should we rotate the objects also? don't think so at the moment 
            App.ActiveDocument.recompute()
            App.ActiveDocument.commitTransaction()  # undo reg.
        except Exception as err:
            App.Console.PrintError("'Align to Plain' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'AlignToPlane.svg',
            'MenuText': 'Align To Plane',
            'ToolTip':  'Align to Plane'
        }


Gui.addCommand('Design456_AlignToPlane', Design456_AlignFlatToPlane())

# Plane Alignments

# Top


class Design456_TopSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 1.0), 0.0)
        Gui.activeDocument().activeView().viewTop()
        Design456Init.DefaultDirectionOfExtrusion = 'z'
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'TopSideView.svg',
            'MenuText': 'Top Side View',
            'ToolTip':  'Top Side View'
        }


Gui.addCommand('Design456_TopSideView', Design456_TopSideView())

# Bottom View


class Design456_BottomView:
    import Design456Init

    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, -1.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'z'
        Gui.activeDocument().activeView().viewBottom()
        Gui.Snapper.grid.on()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'BottomSideView.svg',
            'MenuText': 'Bottom Side View',
            'ToolTip':  'Bottom Side View'
        }


Gui.addCommand('Design456_BottomView', Design456_BottomView())

# Left


class Design456_LeftSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(1.0, 0.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'x'
        Gui.activeDocument().activeView().viewLeft()
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'LeftSideView.svg',
            'MenuText': 'Left Side View',
            'ToolTip':  'Left Side View'
        }


Gui.addCommand('Design456_LeftSideView', Design456_LeftSideView())

# Right


class Design456_RightSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(-1.0, 0.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'x'
        Gui.activeDocument().activeView().viewRight()
        Gui.Snapper.grid.on()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'RightSideView.svg',
            'MenuText': 'Right Side View',
            'ToolTip':  'Right Side View'
        }


Gui.addCommand('Design456_RightSideView', Design456_RightSideView())

# Front


class Design456_FrontSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 1.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'y'
        Gui.activeDocument().activeView().viewFront()
        Gui.Snapper.grid.on()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'FrontSideView.svg',
            'MenuText': 'Front Side View',
            'ToolTip':  'Front Side View'
        }


Gui.addCommand('Design456_FrontSideView', Design456_FrontSideView())

# Back


class Design456_BackSideView:
    import Design456Init

    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, -1.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'y'
        Gui.activeDocument().activeView().viewRear()
        Gui.Snapper.grid.on()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'BackSideView.svg',
            'MenuText': 'Backside View',
            'ToolTip':  'BackSide View'
        }


Gui.addCommand('Design456_BackSideView', Design456_BackSideView())


# Design456 Move
# I need to have these as not always the are in the contex menu
class Design456_MoveObject:

    def Activated(self):
        try:
            # Gui.runCommand('Std_Transform')
            Gui.runCommand('Std_TransformManip')
            return

        except Exception as err:
            App.Console.PrintError("'Design456_loftOnDirection' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'Design456_Move.svg',
            'MenuText': 'Design456 Move',
            'ToolTip':  'Design456 Move'
        }


Gui.addCommand('Design456_MoveObject', Design456_MoveObject())

# Design456 Move Detailed


class Design456_MoveObjectDetailed:

    def Activated(self):
        try:
            Gui.runCommand('Std_Transform')
            return

        except Exception as err:
            App.Console.PrintError("'Design456_loftOnDirection' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'Design456_MoveD.svg',
            'MenuText': 'Design456 Move-Detailed',
            'ToolTip':  'Design456 Move Detailed'
        }


Gui.addCommand('Design456_MoveObjectDetailed', Design456_MoveObjectDetailed())


class Design456_ResetPlacements:
    """[Reset placements of all objects or a specific object]
        Args:
            _objects : Object to reset it's placements to global placement. Default is None.
                        When it is None, all objects are affected in the document.
    """

    def __init__(self, _objects=None):
        self.oldObjects = []
        self.objects = _objects

    def Activated(self):
        try:
            temp = []
            
            self.objects = Gui.Selection.getSelectionEx()
            if len(self.objects) == 0:
                self.objects = App.ActiveDocument.Objects
            App.ActiveDocument.openTransaction(
                translate("Design456", "ResetPlacement"))
            Gui.Selection.clearSelection()
            for sObj in self.objects:
                temp.clear()
                test=""
                if hasattr(sObj,"Object"):
                    test= sObj.Object.PropertiesList
                else:
                    test= sObj.PropertiesList
                if "Placement" in test:
                    newOBJ = App.ActiveDocument.addObject(
                        "Part::Compound", "tempReset")  # Create new compound object
                    newOBJ.Links = sObj.Object
                    minzPoint = sObj.Object.Shape.BoundBox.ZMin
                    # Start to inverse the old placement
                    plOld = sObj.Object.Placement.copy()
                    if (plOld.Base !=App.Vector(0,0,0)):
                        # The object is not at relative origin. 
                        # We need to reset it before doing any action
                        # and we need to keep the old values also.
                        saveTemp=plOld
                        plOld.Base=App.Vector(0,0,0)
                        pl = plOld
                        # Take the first vector of the object as a new placement
                        plOld.Base = sObj.Object.Shape.Vertexes[0].Point
                        plOld.Base.z = minzPoint
                        p = plOld.inverse()
                        sObj.Object.Placement = p
                        # Put the Z axis to be the minimum point
                        newOBJ.Placement = pl
                        newOBJ.Placement.Base= newOBJ.Placement.Base + (saveTemp.Base)
                    else: 
                        pl = plOld
                        # Take the first vector of the object as a new placement
                        plOld.Base = sObj.Object.Shape.Vertexes[0].Point
                        plOld.Base.z = minzPoint
                        p = plOld.inverse()
                        sObj.Object.Placement = p
                        # Put the Z axis to be the minimum point
                        newOBJ.Placement = pl

                    # Make a simple copy of the object
                    App.ActiveDocument.recompute()
                    shp = _part.getShape(
                        newOBJ, '', needSubElement=False, refine=False)
                    simpleNew = App.ActiveDocument.addObject(
                        'Part::Feature', 'Reset')
                    Gui.Selection.addSelection(simpleNew)
                    simpleNew.Shape = shp
                    App.ActiveDocument.recompute()
                    if "Group" in sObj.Object.PropertiesList:
                        for _obj in sObj.Object.Group:
                            App.ActiveDocument.removeObject(_obj.Name)

                    if "Links" in sObj.Object.PropertiesList:
                        for _obj in sObj.Object.Links:
                            App.ActiveDocument.removeObject(_obj.Name)
                    App.ActiveDocument.removeObject(newOBJ.Name)
                    App.ActiveDocument.removeObject(sObj.Object.Name)
            App.ActiveDocument.recompute()
            App.ActiveDocument.commitTransaction()  # undo

        except Exception as err:
            App.Console.PrintError("'Reset Placements failed' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Reset Placements for all objects or specific object")
        return {'Pixmap':  Design456Init.ICON_PATH + 'Design456_ResetPlacements.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Reset Placement"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand('Design456_ResetPlacements', Design456_ResetPlacements())
#####


# Select Tool
class Design456_SelectTool:
    """[Select Tool for selecting faces, edges, vertices]
    """
    def getMainWindow(self):
        """[Create the tab for the tool]

        Returns:
            [QTtab]: [The tab created which should be added to the FreeCAD]
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
            self.dialog.setObjectName("seldialog")
            la = QtGui.QVBoxLayout(self.dialog)   
            v_widget = QtGui.QWidget(self.dialog)
            v_widget.setLayout(la)
            v_widget.setFixedWidth(300)
            v_widget.setFixedHeight(200)
            
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Select")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(325, 450)
            self.dialog.setWindowTitle("Select")
            self.label=QtGui.QLabel(self.dialog)
            
            font = QtGui.QFont()
            font.setFamily("Guttman-Aharoni")
            font.setBold(True)
            self.dialog.setFont(font) 
            self.label.setFont(font)
            self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Europe))
            self.label.setFrameShape(QtGui.QFrame.NoFrame)
            self.label.setFrameShadow(QtGui.QFrame.Sunken)
            self.label.setObjectName("label")
 
            self.combo = QtGui.QComboBox(self.dialog)
            self.combo.setGeometry(QtCore.QRect(20, 60, 240, 20))
            self.combo.setIconSize(QtCore.QSize(40,40))
 
            self.label.setText(translate("self.dialog", "Select Desired subobjects"))
            

            self.combo.addItem(translate("self.dialog", "Preselected"))
            self.combo.setItemData(0, QtGui.QBrush(QtCore.Qt.red), QtCore.Qt.TextColorRole)
            #Face
            self.combo.addItem(translate("self.dialog", "All Faces"))
            self.combo.setItemData(1, QtGui.QBrush(QtCore.Qt.red), QtCore.Qt.TextColorRole)
            
            self.combo.addItem(translate("self.dialog", "Horizontal Faces"))
            self.combo.addItem(translate("self.dialog", "Vertical Faces"))
            self.combo.addItem(translate("self.dialog", "Loop-Faces Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Loop-Faces Perpendicular to XZ"))
            self.combo.addItem(translate("self.dialog", "Loop-Faces Perpendicular to YZ"))
            
            self.combo.setItemData(2, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(3, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(4, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(5, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(6, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            
            #Edges
            self.combo.addItem(translate("self.dialog", "All Edges in the Object"))
            self.combo.addItem(translate("self.dialog", "All Edges in the Face"))
            self.combo.addItem(translate("self.dialog", "All Edges-Horizontal Direction"))
            self.combo.addItem(translate("self.dialog", "All Edges-Vertical Direction"))
            self.combo.addItem(translate("self.dialog", "Loop-Edges Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Loop-Edges Perpendicular to XZ"))
            self.combo.addItem(translate("self.dialog", "Loop-Edges Perpendicular to YZ"))

            self.combo.setItemData(7, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(8 , QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(9 , QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(10, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(11, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(12, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(13, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)

            #Vertexes
            self.combo.addItem(translate("self.dialog", "All Vertexes in the Object"))
            self.combo.addItem(translate("self.dialog", "All Vertexes in the Face"))
            self.combo.addItem(translate("self.dialog", "Loop-Vertexes Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Loop-Vertexes Perpendicular to XZ"))
            self.combo.addItem(translate("self.dialog", "Loop-Vertexes Perpendicular to YZ"))

            self.combo.setItemData(14, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(15, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
            self.combo.setItemData(16, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
            self.combo.setItemData(17, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
            self.combo.setItemData(18, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
          
            # self.combo.setItemIcon(0,icon0)
            # self.combo.setItemIcon(1,icon1)
            # self.combo.setItemIcon(2,icon2)
            self.combo.currentTextChanged.connect(self.activeComboItem)
            
            self.btnRefresh=QtGui.QPushButton(self.dialog)
            self.btnRefresh.setText("Update\nSelection")
            self.btnRefresh.setGeometry(50,80,80,80)
            self.btnRefresh.setStyleSheet("background: cyan;")



            
            self.buttonBox = QtGui.QDialogButtonBox(self.dialog)
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
            self.buttonBox.setObjectName("buttonBox")

            la.addWidget(self.label)            
            la.addWidget(self.btnRefresh)
            la.addWidget(self.combo)
            la.addWidget( self.buttonBox)

            # font = QtGui.QFont()
            # font.setFamily("Caladea")
            # font.setPointSize(10)
            # font.setBold(True)

            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.hideDialog)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.hideDialog)

            self.btnRefresh.clicked.connect(self.refreshSelection)
            return self.dialog
        except Exception as err:
            App.Console.PrintError("'Design456_SelectTool' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    def activeComboItem(self):
        self.currentSelectedItem=self.combo.currentText()
        print(self.currentSelectedItem)

        
    def refreshSelection(self):
        self.selectedObj=Gui.Selection.getSelectionEx()
        self.faces=self.selectedObj[0].Object.Shape.Faces
        self.edges=self.selectedObj[0].Object.Shape.Edges
        self.vertexes=self.selectedObj[0].Object.Shape.Vertexes
        self.Targetobj = self.selectedObj[0].Object
        self.doc=App.ActiveDocument
        if len(self.selectedObj)== 0:
            # An object must be selected
            errMessage = "Select an object, one face or one edge before using the tool"
            faced.errorDialog(errMessage)
            return
        
    def selectObjects(self,obj):
        currentID=self.buttonGroup.id(obj)
        Gui.Selection.clearSelection()
        if ((currentID>=FR_SELECTION.ALL_FACES_IN_OBJECT) and 
           (currentID<=FR_SELECTION.ALL_HORIZONTAL_FACE_LOOP)):
           self.selectFaces(currentID)
        elif ((currentID>=FR_SELECTION.ALL_EDGES_IN_OBJECT) and 
           (currentID<=FR_SELECTION.ALL_EDGES_HORIZONTAL_FACE_LOOP)):
            self.selectEdges(currentID)
        elif ((currentID>=FR_SELECTION.ALL_VERTEXES_IN_OBJECT) and 
          (currentID<=FR_SELECTION.ALL_VERTEXES_HORIZONTAL_FACE_LOOP)):
            self.selectVertexes(currentID)

    def selectFaces_All(self):
        for i in range(0,len(self.faces)):
            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))

    def FacesArePerpendicularToXY(self,face):
        return ((face.Surface.normalAt(1,1)==App.Vector (0,0,1)) or
                 (face.Surface.normalAt(1,1)==App.Vector (0,0,-1)))

    def selectFaces_Horizontal(self):
        for i in range(0,len(self.faces)):
            normal=self.faces[i].normalAt(1,1)
            if not((normal==App.Vector (0.0, 0.0, -1.0) or
                normal==App.Vector (0.0, 0.0, 1.0) or
                (abs(normal.x)==abs(normal.y) and abs(normal.x)==abs(normal.z)))):
                    Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))
    
    def selectFaces_Vertical(self):
        for i in range(0,len(self.faces)):
            normal=self.faces[i].normalAt(1,1)
            if (normal==App.Vector (0.0, 0.0, -1.0) or
                normal==App.Vector (0.0, 0.0, 1.0) or
                (abs(normal.x)==abs(normal.y) and abs(normal.x)==abs(normal.z))):
                Gui.Selection.addSelection(self.doc.Name, self.Targetobj.Name, "Face"+str(i+1))

    def faceHasEdge(self, face, edge):
        for e in face.Edges:
            if edge.isSame(e):
                return True  
        return False

    def selectFaces_Horizontal_faceloop(self):
        firstFace=self.selectedObj[0].SubObjects[0]  #Selected face in the Loop side
        if( hasattr(firstFace, 'curvature')):
            print("Curvature face has only one face")
            return  # cylinder has only one face 

        firstFaceName= self.selectedObj[0].SubElementNames[0] #Selected facename
        shape=self.selectedObj[0].Object.Shape
        Gui.Selection.clearSelection()
        self.selectFaces_Horizontal()
        HorizontalFaces=Gui.Selection.getSelectionEx()[0].SubObjects #all horizontal
        Gui.Selection.clearSelection()
        self.selectEdges_Horizontal()
        HorizontalEdges=Gui.Selection.getSelectionEx()[0].SubObjects
        firstFaceEdges=[]
        for e in HorizontalEdges:
            if self.faceHasEdge(firstFace,e):
                print("found")
                firstFaceEdges.append(e)
        #We have the horizontal edges of first edge
        TotalFaces=[]
        newEdge=firstFaceEdges[1]
        currentFace=firstFace
        currentEdges=[]
        while (not(newEdge.isSame(firstFaceEdges[0]))):
            f=faced.findFaceSHavingTheSameEdge(newEdge,shape)
            if f[0].isSame(currentFace):
                TotalFaces.append(f[1])
                currentFace=f[1]
            else:
                TotalFaces.append(f[0])
                currentFace=f[0]
            #we have new face, find edges
            for e in HorizontalEdges:
                if self.faceHasEdge(currentFace, e):
                    currentEdges.append(e)
            if not(currentEdges[0].isSame(newEdge)):
                newEdge=currentEdges[0]
            else:
                newEdge=currentEdges[1]
            currentEdges.clear()
        Gui.Selection.clearSelection()
        
        for i in range(0, len(self.faces)):
            for j in range(0,len(TotalFaces)):
                f1=self.faces[i]
                f2=TotalFaces[j]
                if(f2.isSame(f1)):
                    Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))
        Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,firstFaceName)

    #Faces
    def selectFaces(self,Seltype): 
        if Seltype == FR_SELECTION.ALL_FACES_IN_OBJECT:
            self.selectFaces_All()
        elif Seltype == FR_SELECTION.ALL_HORIZONTAL_FACES:
            self.selectFaces_Horizontal()
        elif Seltype == FR_SELECTION.ALL_VERTICAL_FACES:
            self.selectFaces_Vertical()
        elif Seltype == FR_SELECTION.ALL_HORIZONTAL_FACE_LOOP:
            self.selectFaces_Horizontal_faceloop()
    
    def selectEdges_All(self):
        for i in range(0,len(self.edges)):
            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Edge"+str(i+1))

    def selectEdges_inFace(self):
        edges=self.selectedObj[0].Object.Shape.Edges
        f=self.selectedObj[0].SubObjects[0]
        for j in enumerate(edges):
            for e in f.Edges:
                if j[1].isSame(e):
                    name="Edge%d" %(j[0]+1)
                    Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                    break

    def selectEdges_Horizontal(self):
        for i in range(0,len(self.faces)):
            normal=self.faces[i].normalAt(1,1)
            if not((normal==App.Vector (0.0, 0.0, -1.0) or
                normal==App.Vector (0.0, 0.0, 1.0) )):
                for e in self.faces[i].Edges:
                    for j in enumerate(self.edges):
                        if j[1].isSame(e):
                                v1=j[1].Vertexes[0]
                                v2=j[1].Vertexes[1]
                                if (v1.Point.z!=v2.Point.z):
                                    name="Edge%d" %(j[0]+1)
                                    Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)

    def selectEdges_Vertical(self):
        for i in range(0,len(self.faces)):
            normal=self.faces[i].normalAt(1,1)
            if (normal==App.Vector (0.0, 0.0, -1.0) or
                    normal==App.Vector (0.0, 0.0, 1.0)):
                    for e in self.faces[i].Edges:
                        for j in enumerate(self.edges):
                            if j[1].isSame(e):
                                name="Edge%d" %(j[0]+1)
                                Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
        
    def selectEdges_Horizontal_Loop(self):
        Gui.Selection.clearSelection()
        self.selectFaces_Horizontal_faceloop()
        faces=Gui.Selection.getSelectionEx()[0].SubObjects
        Gui.Selection.clearSelection()
        self.selectEdges_Horizontal()
        edges=Gui.Selection.getSelectionEx()[0].SubObjects
        foundEdges=[]
        for j in enumerate(edges):
            for f in faces:
                if self.faceHasEdge(f,j[1]):
                    foundEdges.append(j[1])
                    
        Gui.Selection.clearSelection()        
        for j in enumerate(self.edges):
            for e in foundEdges:
                if j[1].isSame(e):
                    name="Edge%d" %(j[0]+1)
                    Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                    break
    #Edges
    def selectEdges(self,Seltype):
        if Seltype == FR_SELECTION.ALL_EDGES_IN_OBJECT:
            self.selectEdges_All()
        elif Seltype == FR_SELECTION.ALL_EDGES_IN_FACE:
            self.selectEdges_inFace()
        elif Seltype == FR_SELECTION.ALL_EDGES_HORIZONTAL:
            self.selectEdges_Horizontal()
        elif Seltype == FR_SELECTION.ALL_EDGES_VERTICAL:
            self.selectEdges_Vertical()
        elif Seltype == FR_SELECTION.ALL_EDGES_HORIZONTAL_FACE_LOOP:
            self.selectEdges_Horizontal_Loop()


    def selectVertexes_All(self):
        for i in range(0,len(self.vertexes)):
            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Vertex"+str(i+1))
    
    def selectVertexes_InFace(self):
        vertex=self.selectedObj[0].Object.Shape.Vertexes
        f=self.selectedObj[0].SubObjects[0]
        for j in enumerate(vertex):
            for e in f.Vertexes:
                if j[1].isSame(e):
                    name="Vertex%d" %(j[0]+1)
                    Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                    break

    def selectVertexes_Horizontal_Loop(self):
        Gui.Selection.clearSelection()
        self.selectEdges_Horizontal_Loop()
        edges=Gui.Selection.getSelectionEx()[0].SubObjects
        Gui.Selection.clearSelection()
        for j in enumerate(self.vertexes):
            for e in edges:
                for v in e.Vertexes :
                    for e in v.Vertexes:
                        if j[1].isSame(e):
                            name="Vertex%d" %(j[0]+1)
                            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                            break


    #Vertexes      
    def selectVertexes(self,Seltype):
        if Seltype==FR_SELECTION.ALL_VERTEXES_IN_OBJECT:
            self.selectVertexes_All()
        if Seltype==FR_SELECTION.ALL_VERTEXES_IN_FACE:
            self.selectVertexes_InFace()
        if Seltype==FR_SELECTION.ALL_VERTEXES_HORIZONTAL_FACE_LOOP:
            self.selectVertexes_Horizontal_Loop()
            

    def hideDialog(self):
        self.dialog.hide()
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
        del self.dialog
        faced.showFirstTab()
        return
        
    def Activated(self):
        self.refreshSelection()
        self.selectedValue=0 # used to identify the user-chosen option of selection
        answer=0
        try:
            answer=self.getMainWindow()

        except Exception as err:
            App.Console.PrintError("'NonuniformedBox' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Select.svg',
            'MenuText': 'SelectTool',
            'ToolTip':  'SelectTool'
        }

Gui.addCommand('Design456_SelectTool', Design456_SelectTool())

##

class Design456_Alignment_Tools:
    list = ["Design456_MoveObject",
            "Design456_MoveObjectDetailed",
            "Separator",
            "Design456_ResetPlacements",
            "Separator",
            "Design456_AlignToPlane",
            "Design456_Magnet",
#            "Design456_SmartMove",
            "Design456_SmartAlignment",
            "Design456_SelectTool"
#            "Design456_ViewInsideObjects",
            ]

    """Design456 Alignments Tools Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'Part_Tools.svg',
            'MenuText': 'Tools',
            'ToolTip':  'Tools'
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if Gui.activeDocument():
            return True
        else:
            return False

    def Activated(self):
        self.appendToolbar("Design456__Alignment", self.list)
