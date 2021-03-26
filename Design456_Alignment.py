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
# Toolbar class
"""Design456_Alignment"""

# Object Alignment
class Design456_AlignFlatToPlane:
    def Activated(self):
        try:
            Selectedobjects = Gui.Selection.getSelectionEx()
            #This must be modified          
            
            for eachObj in Selectedobjects:
                if Design456Init.DefaultDirectionOfExtrusion=='z':
                    eachObj.Object.Placement.Base.z = 0.0
                elif Design456Init.DefaultDirectionOfExtrusion=='y':
                    eachObj.Object.Placement.Base.y = 0.0
                elif Design456Init.DefaultDirectionOfExtrusion=='x':
                    eachObj.Object.Placement.Base.x = 0.0

                
        except Exception as err:
            App.Console.PrintError("'Align to Plain' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/AlignToPlane.svg',
            'MenuText': 'Align To Plane',
            'ToolTip':  'Align to Plane'
        }
        
Gui.addCommand('Design456_AlignToPlane',Design456_AlignFlatToPlane())

# Plane Alignments

#Top
class Design456_TopSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 1.0), 0.0)
        Gui.activeDocument().activeView().viewTop()
        Design456Init.DefaultDirectionOfExtrusion='z'
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/TopSideView.svg',
            'MenuText': 'Top Side View',
            'ToolTip':  'Top Side View'
            }

Gui.addCommand('Design456_TopSideView',Design456_TopSideView())

#Bottom View
class Design456_BottomView:
    import Design456Init
    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, -1.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion='z'
        Gui.activeDocument().activeView().viewBottom()
        Gui.Snapper.grid.on()
        
    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/BottomSideView.svg',
            'MenuText': 'Bottom Side View',
            'ToolTip':  'Bottom Side View'
            }

Gui.addCommand('Design456_BottomView',Design456_BottomView())

#Left
class Design456_LeftSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(1.0,0.0 , 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion='x'
        Gui.activeDocument().activeView().viewLeft()
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/LeftSideView.svg',
            'MenuText': 'Left Side View',
            'ToolTip':  'Left Side View'
            }

Gui.addCommand('Design456_LeftSideView',Design456_LeftSideView())

#Right
class Design456_RightSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(-1.0, 0.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion='x'
        Gui.activeDocument().activeView().viewRight()
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/RightSideView.svg',
            'MenuText': 'Right Side View',
            'ToolTip':  'Right Side View'
            }

Gui.addCommand('Design456_RightSideView',Design456_RightSideView())

#Front
class Design456_FrontSideView:
    def Activated(self):
        import Design456Init
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0,1.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion='y'
        Gui.activeDocument().activeView().viewFront()
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/FrontSideView.svg',
            'MenuText': 'Front Side View',
            'ToolTip':  'Front Side View'
            }

Gui.addCommand('Design456_FrontSideView',Design456_FrontSideView())

#Back
class Design456_BackSideView:
    import Design456Init
    def Activated(self):
        Gui.Snapper.grid.off()
        App.DraftWorkingPlane.alignToPointAndAxis(
            App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, -1.0, 0.0), 0.0)
        Design456Init.DefaultDirectionOfExtrusion='y'
        Gui.activeDocument().activeView().viewRear()
        Gui.Snapper.grid.on()

    def GetResources(self):
        import Design456Init
        return{
            'Pixmap':    Design456Init.ICON_PATH + '/BackSideView.svg',
            'MenuText': 'Backside View',
            'ToolTip':  'BackSide View'
            }

Gui.addCommand('Design456_BackSideView',Design456_BackSideView())


#Design456 Move 
class Design456_MoveObject:
    
    def Activated(self): 
        try:
            #Gui.runCommand('Std_Transform')
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
            'Pixmap':    Design456Init.ICON_PATH + '/Design456_Move.svg',
            'MenuText': 'Design456 Move',
            'ToolTip':  'Design456 Move'
            }
Gui.addCommand('Design456_MoveObject', Design456_MoveObject())

#Design456 Move Detailed
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
            'Pixmap':    Design456Init.ICON_PATH + '/Design456_MoveD.svg',
            'MenuText': 'Design456 Move-Detailed',
            'ToolTip':  'Design456 Move Detailed'
            }
Gui.addCommand('Design456_MoveObjectDetailed', Design456_MoveObjectDetailed())


class Design456_AlignmentGroup:

    """Design456 Part Alignment Tools"""
    #Separator = QtGui.QSpacerItem(5, 237, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

    def GetCommands(self):
        """3D Alignments Tools."""
        return ("Design456_MoveObject",
                "Design456_MoveObjectDetailed",
                #"Separator",
                "Design456_AlignToPlane",

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools for Aligning 3D/2D Shapes")
        return {'Pixmap':  Design456Init.ICON_PATH +'/Design456_Alignment.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Alignment"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}


Gui.addCommand("Design456_AlignmentGroup", Design456_AlignmentGroup())
