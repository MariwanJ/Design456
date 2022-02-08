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
__updated__ = '2022-02-08 21:25:16'


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
#TODO: FIXME : Make this works in a better way.
    def Activated(self):
        print(Design456Init.DefaultDirectionOfExtrusion,
              " Design456Init.DefaultDirectionOfExtrusion")
        try:
            #Reset the object otherwise this tool fails.
            reset=Design456_ResetPlacements()
            reset.Activated()

            Selectedobjects = Gui.Selection.getSelectionEx()
            # TODO:This must be modified

            for obj in Selectedobjects:

                if Design456Init.DefaultDirectionOfExtrusion == 'z':
                    obj.Object.Placement.Base.z = 0.0
                elif Design456Init.DefaultDirectionOfExtrusion == 'y':
                    obj.Object.Placement.Base.y = 0.0
                elif Design456Init.DefaultDirectionOfExtrusion == 'x':
                    obj.Object.Placement.Base.x = 0.0
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
                    plOld = sObj.Object.Placement
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


class Design456_Alignment_Tools:
    list = ["Design456_MoveObject",
            "Design456_MoveObjectDetailed",
            "Separator",
            "Design456_ResetPlacements",
            "Separator",
            "Design456_AlignToPlane",
            "Design456_Magnet",
#            "Design456_SmartMove",
            "Design456_SmartAlignment"
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
