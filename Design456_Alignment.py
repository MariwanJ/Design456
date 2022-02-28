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

# Toolbar class
# Based  on https://forum.freecadweb.org/viewtopic.php?style=4&f=22&t=29138&start=20
__updated__ = '2022-02-28 22:09:10'


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
            oldsize = self.tab.count()
            self.tab.addTab(self.dialog, "Select")
            self.tab.setCurrentWidget(self.dialog)
            self.dialog.resize(325, 450)
            self.dialog.setWindowTitle("Select")
            self.buttonGroup = QtGui.QButtonGroup(self.dialog)
            la = QtGui.QVBoxLayout(self.dialog)
              
            font = QtGui.QFont()
            font.setFamily("Guttman-Aharoni")
            font.setBold(True)
            self.dialog.setFont(font)
            self.dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Europe))
            self.radSel_1 = QtGui.QRadioButton(self.dialog)
            self.radSel_1.setGeometry(QtCore.QRect(20, 60, 240, 20))
            self.radSel_1.setObjectName("radSel_1")
            self.radSel_2 = QtGui.QRadioButton(self.dialog)
            self.radSel_2.setGeometry(QtCore.QRect(20, 80, 240, 20))
            self.radSel_2.setObjectName("radSel_2")
            self.radSel_3 = QtGui.QRadioButton(self.dialog)
            self.radSel_3.setGeometry(QtCore.QRect(20, 100, 240, 20))
            self.radSel_3.setObjectName("radSel_3")
            self.radSel_4 = QtGui.QRadioButton(self.dialog)
            self.radSel_4.setGeometry(QtCore.QRect(20, 120, 240, 20))
            self.radSel_4.setObjectName("radSel_4")
            self.radSel_5 = QtGui.QRadioButton(self.dialog)
            self.radSel_5.setGeometry(QtCore.QRect(20, 140, 240, 20))
            self.radSel_5.setObjectName("radSel_5")
            self.radSel_6 = QtGui.QRadioButton(self.dialog)
            self.radSel_6.setGeometry(QtCore.QRect(20, 160, 240, 20))
            self.radSel_6.setObjectName("radSel_6")
            self.radSel_7 = QtGui.QRadioButton(self.dialog)
            self.radSel_7.setGeometry(QtCore.QRect(20, 180, 241, 20))
            self.radSel_7.setObjectName("radSel_7")
            self.radSel_8 = QtGui.QRadioButton(self.dialog)
            self.radSel_8.setGeometry(QtCore.QRect(20, 200, 240, 20))
            self.radSel_8.setObjectName("radSel_8")
            self.radSel_9 = QtGui.QRadioButton(self.dialog)
            self.radSel_9.setGeometry(QtCore.QRect(20, 220, 240, 20))
            self.radSel_9.setObjectName("radSel_9")
            self.radSel_10 = QtGui.QRadioButton(self.dialog)
            self.radSel_10.setGeometry(QtCore.QRect(20, 240, 240, 20))
            self.radSel_10.setObjectName("radSel_10")
            self.radSel_11 = QtGui.QRadioButton(self.dialog)
            self.generalBox = QtGui.QGroupBox(u'Selection Type')
            self.label = QtGui.QLabel(self.dialog)
            self.label.setGeometry(QtCore.QRect(20, 10, 361, 41))
            
            self.buttonGroup.addButton(self.radSel_1 )
            self.buttonGroup.addButton(self.radSel_2 )
            self.buttonGroup.addButton(self.radSel_3 )
            self.buttonGroup.addButton(self.radSel_4 )
            self.buttonGroup.addButton(self.radSel_5 )
            self.buttonGroup.addButton(self.radSel_6 )
            self.buttonGroup.addButton(self.radSel_7 )
            self.buttonGroup.addButton(self.radSel_8 )
            self.buttonGroup.addButton(self.radSel_9 )
            self.buttonGroup.addButton(self.radSel_10)

            self.label.setFont(font)
            self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Europe))
            self.label.setFrameShape(QtGui.QFrame.NoFrame)
            self.label.setFrameShadow(QtGui.QFrame.Sunken)
            self.label.setObjectName("label")
            self.buttonBox = QtGui.QDialogButtonBox(self.dialog)
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
            self.buttonBox.setObjectName("buttonBox")

            la.addWidget(self.label)
            la.addWidget(self.radSel_1 )
            la.addWidget(self.radSel_2 )
            la.addWidget(self.radSel_3 )
            la.addWidget(self.radSel_4 )
            la.addWidget(self.radSel_5 )
            la.addWidget(self.radSel_6 )
            la.addWidget(self.radSel_7 )
            la.addWidget(self.radSel_8 )
            la.addWidget(self.radSel_9 )
            la.addWidget(self.radSel_10)
            la.addWidget( self.buttonBox)
            font = QtGui.QFont()
            font.setFamily("Caladea")
            font.setPointSize(10)
            font.setBold(True)

            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("self.dialog", "Select Desired subobjects by\n selecting below options"))
            self.radSel_1.setText(_translate("self.dialog", "All Faces"))
            self.radSel_2.setText(_translate("self.dialog", "Horizontal Faces"))
            self.radSel_3.setText(_translate("self.dialog", "Vertical Faces"))
            self.radSel_4.setText(_translate("self.dialog", "All Edges in the Object"))
            self.radSel_5.setText(_translate("self.dialog", "All Edges in the Face"))
            self.radSel_6.setText(_translate("self.dialog", "All Edges Horizontal Direction"))
            self.radSel_7.setText(_translate("self.dialog", "All Edges Vertical Direction"))
            self.radSel_8.setText(_translate("self.dialog", "All Vertexes in the Object"))
            self.radSel_9.setText(_translate("self.dialog", "All Vertexes in the Face"))
            self.radSel_10.setText(_translate("self.dialog", "All Vertexes in the Edge"))
            QtCore.QMetaObject.connectSlotsByName(self.dialog)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.getValue)
            QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.hideDialog)
            # connects the slot function and makes the argument of the band int type
            self.buttonGroup.buttonClicked.connect(self.selectObjects)

            return self.dialog
        except Exception as err:
            App.Console.PrintError("'Design456_SelectTool' getMainWindow-Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    def hideDialog(self):
        self.dialog.hide()
        dw = self.mw.findChildren(QtGui.QDockWidget)
        newsize = self.tab.count()  # Todo : Should we do that?
        self.tab.removeTab(newsize-1)  # it ==0,1,2,3 ..etc
        del self.dialog
        faced.showFirstTab()
        return
        

    def selectObjects(self,obj):
        print("Key was pressed, id is:", self.buttonGroup.id(obj))


    def getValue(self):
        result=0
        if self.radSel_1.isChecked():
            result= 1
        elif self.radSel_2.isChecked():
            result= 2
        elif self.radSel_3.isChecked():
            result= 3
        elif self.radSel_4.isChecked():
            result= 4
        elif self.radSel_5.isChecked():
            result= 5
        elif self.radSel_6.isChecked():
            result= 6
        elif self.radSel_7.isChecked():
            result= 7
        elif self.radSel_8.isChecked():
            result= 8
        elif self.radSel_9.isChecked():
            result= 9
        elif self.radSel_10.isChecked():
            result= 10
        elif self.radSel_11.isChecked():
            result= 11
        self.dialog.hide()
        return result

            
    def Activated(self):
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
            'Pixmap': Design456Init.ICON_PATH + 'SelectTool.svg',
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
