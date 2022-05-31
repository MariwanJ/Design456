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
__updated__ = '2022-04-20 17:32:33'


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
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 1.0), 0.0)
        Gui.activeDocument().activeView().viewTop()
        Design456Init.DefaultDirectionOfExtrusion = 'z'
        Gui.Snapper.grid.on()

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'TopSideView.svg',
            'MenuText': 'Top Side View',
            'ToolTip':  'Top Side View'
        }


Gui.addCommand('Design456_TopSideView', Design456_TopSideView())

# Bottom View


class Design456_BottomView:

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
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'BottomSideView.svg',
            'MenuText': 'Bottom Side View',
            'ToolTip':  'Bottom Side View'
        }


Gui.addCommand('Design456_BottomView', Design456_BottomView())

# Left


class Design456_LeftSideView:
    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(1.0, 0.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'x'
        Gui.activeDocument().activeView().viewLeft()
        Gui.Snapper.grid.on()

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'LeftSideView.svg',
            'MenuText': 'Left Side View',
            'ToolTip':  'Left Side View'
        }


Gui.addCommand('Design456_LeftSideView', Design456_LeftSideView())

# Right


class Design456_RightSideView:
    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(-1.0, 0.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'x'
        Gui.activeDocument().activeView().viewRight()
        Gui.Snapper.grid.on()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'RightSideView.svg',
            'MenuText': 'Right Side View',
            'ToolTip':  'Right Side View'
        }


Gui.addCommand('Design456_RightSideView', Design456_RightSideView())

# Front


class Design456_FrontSideView:
    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 1.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion = 'y'
        Gui.activeDocument().activeView().viewFront()
        Gui.Snapper.grid.on()
        Gui.runCommand("Draft_ToggleGrid")
        Gui.runCommand("Draft_ToggleGrid")

    def GetResources(self):
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'FrontSideView.svg',
            'MenuText': 'Front Side View',
            'ToolTip':  'Front Side View'
        }


Gui.addCommand('Design456_FrontSideView', Design456_FrontSideView())

# Back


class Design456_BackSideView:

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
        return{
            'Pixmap':    Design456Init.ICON_PATH + 'BackSideView.svg',
            'MenuText': 'Backside View',
            'ToolTip':  'BackSide View'
        }


Gui.addCommand('Design456_BackSideView', Design456_BackSideView())


# Design456 Move
# I need to have these as not always the are in the context menu
class Design456_MoveObject:

    def Activated(self):
        try:
            Gui.runCommand('Std_TransformManip')
            return

        except Exception as err:
            App.Console.PrintError("'Design456_loftOnDirection' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
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
    def __init__(self):
        self.selectedObj = None
        self.firstFace=None
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
            
            self.combo.addItem(translate("self.dialog", "Faces-Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Faces-Parallel to XY"))
            self.combo.addItem(translate("self.dialog", "Loop-Faces Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Loop-Faces Perpendicular to XZ"))
            self.combo.addItem(translate("self.dialog", "Loop-Faces Perpendicular to YZ"))
            
            self.combo.setItemData(2, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(3, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(4, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(5, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(6, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            
            #Edges
            self.combo.addItem(translate("self.dialog", "Edges in the Object"))
            self.combo.addItem(translate("self.dialog", "Edges in the Face"))
            self.combo.addItem(translate("self.dialog", "Edges-Parallel to XY"))
            self.combo.addItem(translate("self.dialog", "Edges Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Edges Perpendicular to XZ"))
            self.combo.addItem(translate("self.dialog", "Edges Perpendicular to YZ"))

            self.combo.setItemData(7, QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.TextColorRole)
            self.combo.setItemData(8 , QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(9 , QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(10, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(11, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(12, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(13, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)

            #Vertexes
            self.combo.addItem(translate("self.dialog", "Vertexes in the Object"))
            self.combo.addItem(translate("self.dialog", "Vertexes in the Face"))
            self.combo.addItem(translate("self.dialog", "Vertexes Perpendicular to XY"))
            self.combo.addItem(translate("self.dialog", "Vertexes Perpendicular to XZ"))
            self.combo.addItem(translate("self.dialog", "Vertexes Perpendicular to YZ"))

            self.combo.setItemData(14, QtGui.QBrush(QtCore.Qt.blue), QtCore.Qt.TextColorRole)
            self.combo.setItemData(15, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
            self.combo.setItemData(16, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
            self.combo.setItemData(17, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
            self.combo.setItemData(18, QtGui.QBrush(QtCore.Qt.black), QtCore.Qt.TextColorRole)
          
            # self.combo.setItemIcon(0,icon0)
            # self.combo.setItemIcon(1,icon1)
            # self.combo.setItemIcon(2,icon2)
            self.combo.currentTextChanged.connect(self.activeComboItem_cb)
            
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
    
    def activeComboItem_cb(self):
        """Combobox callback. It will execute the chosen selection type
        """
        self.currentSelectedItem=self.combo.currentText()
        print(self.currentSelectedItem)
        currentID=self.combo.currentIndex()
        Gui.Selection.clearSelection()
        if currentID==0:
            #Only preselected item
            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,self.firstFaceName)
            return
        if ((currentID>=FR_SELECTION.FACES_IN_OBJECT) and (currentID<=FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_YZ)):
            self.selectFaces(currentID)
        elif ((currentID>=FR_SELECTION.EDGES_IN_OBJECT) and (currentID<=FR_SELECTION.EDGES_PERPENDICULAR_TO_YZ)):
            self.selectEdges(currentID)
        elif ((currentID>=FR_SELECTION.VERTEXES_IN_OBJECT) and (currentID<=FR_SELECTION.VERTEXES_PERPENDICULAR_TO_YZ)):
            self.selectVertexes(currentID)
    
    
    def refreshSelection(self):
        """ Update selected object and it's sub objects
            This allow user to use the tool continuously without
            closing the tool.
        """
        self.selectedObj=Gui.Selection.getSelectionEx()
        self.firstFace=self.selectedObj[0].SubObjects[0]
        if len(self.selectedObj)== 0:
            # An object must be selected
            errMessage = "Select a face before using the tool"
            faced.errorDialog(errMessage)
            return
            
        self.firstFaceName= self.selectedObj[0].SubElementNames[0]   
        self.faces=self.selectedObj[0].Object.Shape.Faces
        self.edges=self.selectedObj[0].Object.Shape.Edges
        self.vertexes=self.selectedObj[0].Object.Shape.Vertexes
        self.Targetobj = self.selectedObj[0].Object
        self.doc=App.ActiveDocument

    def selectFaces_All(self):
        """Select all faces found in the 3D object
        """
        for i in range(0,len(self.faces)):
            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))

    #FACE : check face is  perpendicular XY, XZ and YZ 
    def FaceIsPerpendicularToXY(self,face):
        return (not( (face.normalAt(1,1)==App.Vector (0,0,1)) or
                    (face.normalAt(1,1)==App.Vector (0,0,-1))))
    
    def FaceIsPerpendicularToXZ(self,face):
        return (not((face.normalAt(1,1)==App.Vector (0,1,0)) or
                 (face.normalAt(1,1)==App.Vector (0,-1,0))))

    def FaceIsPerpendicularToYZ(self,face):
        return (not((face.normalAt(1,1)==App.Vector (1,0,0)) or
                 (face.normalAt(1,1)==App.Vector (-1,0,0))))

    #EDGE : check edge is perpendicular XY, XZ and YZ 
    def EdgeIsPerpendicularToXY(self,edge):
        if(faced.roundVector(edge.tangentAt(edge.FirstParameter)) == App.Vector(0,0,1) or
           faced.roundVector(edge.tangentAt(edge.FirstParameter)) == App.Vector(0,0,-1)):
            return True
        else:
            return False
    def EdgeIsPerpendicularToXZ(self,edge):
        if( faced.roundVector(edge.tangentAt(edge.FirstParameter)) == App.Vector(0,1,0) or
           faced.roundVector(edge.tangentAt(edge.FirstParameter)) == App.Vector(0,-1,0)):
            return True
        else:
            return False
        
    def EdgeIsPerpendicularToYZ(self,edge):
        if(faced.roundVector(edge.tangentAt(edge.FirstParameter)) == App.Vector(1,0,0) or
           faced.roundVector(edge.tangentAt(edge.FirstParameter)) == App.Vector(-1,0,0) ):
            return True
        else:
            return False

    def selectFaces_PerpendicularToXY(self):
        for i in range(0,len(self.faces)):
            if self.FaceIsPerpendicularToXY(self.faces[i]):
                Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))
 
    def selectFaces_PerpendicularToXZ(self):
        for i in range(0,len(self.faces)):
            if self.FaceIsPerpendicularToXZ(self.faces[i]):
                Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))

    def selectFaces_PerpendicularToYZ(self):
        for i in range(0,len(self.faces)):
            if self.FaceIsPerpendicularToYZ(self.faces[i]):
                Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))
                   
    def selectFaces_ParallelToXY(self):
        for i in range(0,len(self.faces)):
            if (not (self.FaceIsPerpendicularToXY(self.faces[i]))):    
                Gui.Selection.addSelection(self.doc.Name, self.Targetobj.Name, "Face"+str(i+1))


    def faceHasEdge(self, face, edge):
        for e in face.Edges:
            if edge.isSame(e):
                return True  
        return False

    def selectFaces_faceloop(self,typeOfFaces):
        try:
            if( hasattr(self.firstFace, 'curvature')):
                print("Curvature face has only one face")
                return  # cylinder has only one face 

            shape=self.selectedObj[0].Object.Shape
            Gui.Selection.clearSelection()
            if(typeOfFaces == FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_XY):
                self.selectEdges_PerpendicularToXY()
            elif(typeOfFaces == FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_XZ):
                self.selectEdges_PerpendicularToXZ()
            elif(typeOfFaces == FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_YZ):
                self.selectEdges_PerpendicularToYZ()     
        
            HorizontalEdges=Gui.Selection.getSelectionEx()[0].SubObjects
            if len(HorizontalEdges)==0:
                print("nothing found")
                return
            #print(len(HorizontalEdges),"HorizontalEdges")
            firstFaceEdges=[]
            for e in HorizontalEdges:
                if self.faceHasEdge(self.firstFace,e):
                    firstFaceEdges.append(e)
            
            print("found - edges-len",len(firstFaceEdges))
            #We have the horizontal edges of first edge
            TotalFaces=[]
            if (len(firstFaceEdges)<2):
                print("not found")
                Gui.Selection.clearSelection()
                return
            else:
                pass
                #print("Edges of the first face found",len(firstFaceEdges))                
            
            newEdge=firstFaceEdges[1]  #second edge of the face1
            currentFace=self.firstFace
            currentEdges=[]

            xx=-1
            while (not(newEdge.isSame(firstFaceEdges[0]))):
                xx=xx+1
                print(xx)
                Gui.updateGui()
                f=faced.findFaceSHavingTheSameEdge(newEdge,shape)
                if (f is not None):
                    if f[0].isSame(currentFace):
                        TotalFaces.append(f[1])
                        currentFace=f[1]
                    elif f[1].isSame(currentFace):
                        TotalFaces.append(f[0])
                        currentFace=f[0]
                    else:
                        print("NOT FOUND! out")
                        break #go out
                else:
                    currentFace=None
                if currentFace is None:
                    break
                #we have new face, find edges
                tempcurrentEdges=currentFace.Edges
                currentEdges.clear()
                for end in tempcurrentEdges:
                    for ed in HorizontalEdges:
                        if ed.isSame(end):
                            currentEdges.append(ed)
                            break              
                if (currentEdges[0].isSame(newEdge) ):
                    newEdge=currentEdges[1]
                elif (currentEdges[1].isSame(newEdge)):
                    newEdge=currentEdges[0]
                else:
                    print("not found")
                    break
                if newEdge.isSame(firstFaceEdges[1]) or newEdge.isSame(firstFaceEdges[0]): 
                    break
                currentEdges.clear()
            Gui.Selection.clearSelection()

            for i in range(0, len(self.faces)):
                for j in range(0,len(TotalFaces)):
                    f1=self.faces[i]
                    f2=TotalFaces[j]
                    if(f2.isSame(f1)):
                        Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,"Face"+str(i+1))
                        break
            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,self.firstFaceName)
            
        except Exception as err:
            App.Console.PrintError("'selectFaces_faceloop' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    #Faces
    def selectFaces(self,Seltype): 
        if Seltype == FR_SELECTION.FACES_IN_OBJECT:
            self.selectFaces_All()
        elif Seltype == FR_SELECTION.FACES_PERPENDICULAR_TO_XY:
            self.selectFaces_PerpendicularToXY()
        elif Seltype == FR_SELECTION.FACES_PARALLEL_TO_XY:
            self.selectFaces_ParallelToXY()
        elif Seltype == FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_XY:
            self.selectFaces_faceloop(Seltype)
        elif Seltype == FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_XZ:
            self.selectFaces_faceloop(Seltype)
        elif Seltype == FR_SELECTION.LOOP_FACES_PERPENDICULAR_TO_YZ:
            self.selectFaces_faceloop(Seltype)
    
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

    def selectEdges_PerpendicularToXY(self):
        try:
            for i in range(0,len(self.edges)):
                if self.EdgeIsPerpendicularToXY(self.edges[i]):
                    e=self.edges[i]
                    for j in enumerate(self.edges):
                        if j[1].isSame(e):
                            name="Edge%d" %(j[0]+1)
                            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                            break

        except Exception as err:
            App.Console.PrintError("'selectEdges_ParallelToXY' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 
    
    def selectEdges_PerpendicularToXZ(self):
        try:
            for i in range(0,len(self.edges)):
                if self.EdgeIsPerpendicularToXZ(self.edges[i]):
                    e=self.edges[i]
                    for j in enumerate(self.edges):
                        if j[1].isSame(e):
                            name="Edge%d" %(j[0]+1)
                            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                            break

        except Exception as err:
            App.Console.PrintError("'selectEdges_ParallelToXY' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 

    def selectEdges_PerpendicularToYZ(self):
        try:
            for i in range(0,len(self.edges)):
                if self.EdgeIsPerpendicularToYZ(self.edges[i]):
                    e=self.edges[i]
                    for j in enumerate(self.edges):
                        if j[1].isSame(e):
                            name="Edge%d" %(j[0]+1)
                            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                            break

        except Exception as err:
            App.Console.PrintError("'selectEdges_ParallelToXY' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 


    def selectEdges_ParallelToXY(self):
        try:
            for i in range(0,len(self.edges)):
                e=self.edges[i]
                if not(self.EdgeIsPerpendicularToXY(self.edges[i])):
                    for j in enumerate(self.edges):
                        if j[1].isSame(e):
                            name="Edge%d" %(j[0]+1)
                            Gui.Selection.addSelection(self.doc.Name,self.Targetobj.Name,name)
                            break
        except Exception as err:
            App.Console.PrintError("'selectEdges_ParallelToXY' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)    
                    
    def selectEdges_Loop(self,typeOfEdges):
        try:
            Gui.Selection.clearSelection()

            if typeOfEdges==FR_SELECTION.EDGES_PERPENDICULAR_TO_XY:
                self.selectEdges_PerpendicularToXY()
            elif typeOfEdges==FR_SELECTION.EDGES_PERPENDICULAR_TO_XZ:
                self.selectEdges_PerpendicularToXZ()
            elif typeOfEdges==FR_SELECTION.EDGES_PERPENDICULAR_TO_YZ:
                self.selectEdges_PerpendicularToYZ()
            
            if(len(Gui.Selection.getSelectionEx())==0):
                print("Selection of edges failed -out")
            
        except Exception as err:
            App.Console.PrintError("'selectEdges_Loop' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)                   
    #Edges
    def selectEdges(self,Seltype):
        if Seltype == FR_SELECTION.EDGES_IN_OBJECT:
            self.selectEdges_All()
        elif Seltype == FR_SELECTION.EDGES_IN_FACE:
            self.selectEdges_inFace()
        elif Seltype == FR_SELECTION.EDGES_PERPENDICULAR_TO_XY:
            self.selectEdges_PerpendicularToXY()
        elif Seltype == FR_SELECTION.EDGES_PARALLEL_TO_XY:
            self.selectEdges_ParallelToXY()
        elif Seltype == FR_SELECTION.EDGES_PERPENDICULAR_TO_XY:
            self.selectEdges_Loop(Seltype)
        elif Seltype == FR_SELECTION.EDGES_PERPENDICULAR_TO_XZ:
            self.selectEdges_Loop(Seltype)
        elif Seltype == FR_SELECTION.EDGES_PERPENDICULAR_TO_YZ:
            self.selectEdges_Loop(Seltype)


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

    def selectVertexes_In_Loop(self,selType):
        Gui.Selection.clearSelection()
        self.selectEdges_Loop(selType)
        if len(Gui.Selection.getSelectionEx())==0:
            print("not found")
            return
        
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
        if Seltype==FR_SELECTION.VERTEXES_IN_OBJECT:
            self.selectVertexes_All()
        if Seltype==FR_SELECTION.VERTEXES_IN_FACE:
            self.selectVertexes_InFace()
        if Seltype==FR_SELECTION.VERTEXES_PERPENDICULAR_TO_XY:
            self.selectVertexes_In_Loop(FR_SELECTION.EDGES_PERPENDICULAR_TO_XY)
        if Seltype==FR_SELECTION.VERTEXES_PERPENDICULAR_TO_XZ:
            self.selectVertexes_In_Loop(FR_SELECTION.EDGES_PERPENDICULAR_TO_XZ)            
        if Seltype==FR_SELECTION.VERTEXES_PERPENDICULAR_TO_YZ:
            self.selectVertexes_In_Loop(FR_SELECTION.EDGES_PERPENDICULAR_TO_YZ)
            
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
