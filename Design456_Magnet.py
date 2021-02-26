# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *																		   *
# *	This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *																		   *
# *	Copyright (C) 2021													   *
# *																		   *
# *																		   *
# *	This library is free software; you can redistribute it and/or		   *
# *	modify it under the terms of the GNU Lesser General Public			   *
# *	License as published by the Free Software Foundation; either		   *
# *	version 2 of the License, or (at your option) any later version.	   *
# *																		   *
# *	This library is distributed in the hope that it will be useful,		   *
# *	but WITHOUT ANY WARRANTY; without even the implied warranty of		   *
# *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU	   *
# *	Lesser General Public License for more details.						   *
# *																		   *
# *	You should have received a copy of the GNU Lesser General Public	   *
# *	License along with this library; if not, If not, see				   *
# *	<http://www.gnu.org/licenses/>.										   *
# *																		   *
# *	Author : Mariwan Jalal	 mariwan.jalal@gmail.com					   *
# **************************************************************************
import os
import sys
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
import Design456Init
import FACE_D as faced


# This should calculate new position used by Magnet
# you should send Gui.Selection.getSelection()[0] , Gui.Selection.getSelection()[1]
class magnetNewLocation:
    def __init__(self, obj1, obj2):
        self.object1 = obj1
        self.object2 = obj2

    def Calculate(self):
        try:
            # face 1 is the base, face 2 muste be moved
            if(len(self.object1.SubElementNames) == 0 or
               len(self.object2.SubElementNames) == 0):
                # Two object must be selected
                errMessage = "Select two faces"
                faced.getInfo(self.object1).errorDialog(errMessage)
                return

            selectedEdge1 = self.object1.SubObjects[0]	  # select one element
            selectedEdge2 = self.object2.SubObjects[0]	  # select one element
            SubElementName1 = self.object1.SubElementNames[0]
            SubElementName1 = self.object2.SubElementNames[0]
            plr = plDirection = App.Placement()

            # section direction
            yL = selectedEdge1.CenterOfMass
            uv = selectedEdge1.Surface.parameter(yL)
            nv = selectedEdge1.normalAt(uv[0], uv[1])
            direction = yL.sub(nv + yL)
            r = App.Rotation(App.Vector(0, 0, 0), direction)
            plDirection.Rotation.Q = r.Q
            print(r.Q)
            plDirection.Base = yL
            plr = plDirection
            print("surface : ", self.object1.Object.Name, " ",
                  SubElementName1, "	 ", direction)
            # section direction

            # section placement face in length and direction
            newLocation = (App.Vector(direction)).scale(1,
                                                        1, 
                                                        1)
            print (newLocation)
            if (direction.x != 0 and abs(direction.x) == direction.x):
                newLocation.x = newLocation.x+selectedEdge1.Placement.Base.x*direction.x
            elif (direction.x != 0 and abs(direction.x) != direction.x):
                newLocation.x = newLocation.x-selectedEdge1.Placement.Base.x*direction.x
            else:
                newLocation.x = selectedEdge1.Placement.Base.x
            if (direction.y != 0 and abs(direction.y) == direction.y):  # posative >0
                newLocation.y = newLocation.y+selectedEdge1.Placement.Base.y*direction.y
            elif (direction.y != 0 and abs(direction.x) != direction.y):  # negative <0
                newLocation.y = newLocation.y-selectedEdge1.Placement.Base.y*direction.y
            else:
                newLocation.y = selectedEdge1.Placement.Base.y
            if (direction.z != 0 and abs(direction.z) == direction.z):
                newLocation.z = newLocation.z+selectedEdge1.Placement.Base.z*direction.z
            # negative <0:
            elif (direction.z != 0 and abs(direction.z) != direction.z):
                newLocation.z = newLocation.z-selectedEdge1.Placement.Base.z*direction.z
            else:
                newLocation.z = selectedEdge1.Placement.Base.z
            
            return newLocation
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


# Move an object to the location of the mouse click on another surface


class Design456_Magnet:

    def Activated(self):
        try:
            s = Gui.Selection.getSelectionEx()
            if (len(s) < 2):
                # Two object must be selected
                errMessage = "Select two or more objects to use Magnet Tool"
                faced.getInfo(s).errorDialog(errMessage)
                return
            sub1 = Gui.Selection.getSelectionEx()[0]
            sub2 = Gui.Selection.getSelectionEx()[1]
            newLoc = magnetNewLocation(sub1, sub2).Calculate()
            # Move OBJ1 to be on Top2
            #obj2info = faced.getInfo(sub2)
            #sub1.Object.Placement.Base = obj2info.objectRealPlacement3D()
            print (newLoc)
            sub2.Object.Placement.Base = newLoc
            
            """
            try:
                height=float (sub1.Object.Height)
            except:
                height=float(sub1.Object.Shape.BoundBox.ZLength)
                
            sub1.Object.Placement.Base.z=sub1.Object.Placement.Base.z+height
            """
            # sub1.Object.Placement.Base.x=sub1.Object.Placement.Base.x+float(sub1.Object.Shape.BoundBox.XLength)
            # sub1.Object.Placement.Base.y=sub1.Object.Placement.Base.y+float(sub1.Object.Shape.BoundBox.YLength)
            #sub1.Object.Placement.Base = obj2info.getObjectCenterOfMass()

            # sub1.Object.Placement.Base
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Magnet.svg',
            'MenuText': 'Part_Magnet',
                        'ToolTip':	'Part Magnet'
        }


Gui.addCommand('Design456_Magnet', Design456_Magnet())
