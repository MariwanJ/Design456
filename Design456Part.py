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
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore  # https://www.freecadweb.org/wiki/PySide
import Draft 
import Part 
import FACE_D as faced
from draftutils.translate import translate   #for translate

__updated__ = '2022-06-08 19:21:47'

import BasicShapes.CommandShapes
import CompoundTools._CommandExplodeCompound

import Design456Init

sys.path.append(Design456Init.PYRAMID_PATH)

# BOX
class Design456Part_Box:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Box"))
            newObj = App.ActiveDocument.addObject("Part::Box", "Box")
            newObj.Label = "Cube"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Box' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Box.svg',
            'MenuText': 'Part_Box',
                        'ToolTip':  'Part Box'
        }


Gui.addCommand('Design456Part_Box', Design456Part_Box())

# Cylinder


class Design456Part_Cylinder:

    def Activated(self):
        try: 
            App.ActiveDocument.openTransaction(translate("Design456","Part Cylinder"))
            newObj = App.ActiveDocument.addObject("Part::Cylinder", "Cylinder")
            newObj.Radius = 5
            App.ActiveDocument.ActiveObject.Label = "Cylinder"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Cylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Cylinder.svg',
            'MenuText': 'Part_Cylinder',
                        'ToolTip':  'Part Cylinder'
        }

Gui.addCommand('Design456Part_Cylinder', Design456Part_Cylinder())


# Tube
class Design456Part_Tube:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Tube"))
            Gui.runCommand('Part_Tube', 0)
            newObj =App.ActiveDocument.ActiveObject
            v = Gui.ActiveDocument.ActiveView
            App.ActiveDocument.recompute()
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Part::Tube' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Tube.svg',
            'MenuText': 'Part_Tube',
                        'ToolTip':  'Part Tube'
        }


Gui.addCommand('Design456Part_Tube', Design456Part_Tube())


# Sphere
class Design456Part_Sphere:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Sphere"))
            newObj = App.ActiveDocument.addObject("Part::Sphere", "Sphere")
            App.ActiveDocument.ActiveObject.Label = "Sphere"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
            
        except Exception as err:
            App.Console.PrintError("'Part::Sphere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Sphere.svg',
            'MenuText': 'Part_Sphere',
                        'ToolTip':  'Part Sphere'
        }


Gui.addCommand('Design456Part_Sphere', Design456Part_Sphere())
# Cone


class Design456Part_Cone:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Cone"))
            newObj = App.ActiveDocument.addObject("Part::Cone", "Cone")
            App.ActiveDocument.ActiveObject.Label = "Cone"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Cone' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Cone.svg',
            'MenuText': 'Part_Cone',
                        'ToolTip':  'Part Cone'
        }


Gui.addCommand('Design456Part_Cone', Design456Part_Cone())


# Cone
class Design456Part_Torus:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Torus"))
            newObj = App.ActiveDocument.addObject("Part::Torus", "Torus")
            App.ActiveDocument.ActiveObject.Label = "Torus"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Torus' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Torus.svg',
            'MenuText': 'Part_Torus',
                        'ToolTip':  'Part Torus'
        }

Gui.addCommand('Design456Part_Torus', Design456Part_Torus())

# Wedge


class Design456Part_Wedge:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Wedge"))
            newObj = App.ActiveDocument.addObject("Part::Wedge", "Wedge")
            App.ActiveDocument.ActiveObject.Label = "Wedge"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Wedge' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Wedge.svg',
            'MenuText': 'Part_Wedge',
                        'ToolTip':  'Part Wedge'
        }

Gui.addCommand('Design456Part_Wedge', Design456Part_Wedge())


# Prism
class Design456Part_Prism:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Prism"))
            newObj = App.ActiveDocument.addObject("Part::Prism", "Prism")
            App.ActiveDocument.ActiveObject.Label = "Prism"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Prism' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Prism.svg',
            'MenuText': 'Part_Prism',
                        'ToolTip':  'Part Prism'
        }

Gui.addCommand('Design456Part_Prism', Design456Part_Prism())

#TODO: FIXME: clean up the code and fix the code
# Pyramid
class Design456Part_Pyramid:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Pyramid"))
            plc = App.Placement()
            Faces = QtGui.QInputDialog.getInt(None, "Faces", "Faces:",5)[0]
            if(Faces ==0 ):
                return # Nothing to do here 
            plc.Rotation.Q = (0.0, 0.0, 0, 1.0)
            plc.Base = App.Vector(0.0, 0.0, 0.0)
            newObj = Draft.makePolygon(Faces, radius=10, inscribed=True, placement=plc, face=True, support=None)
            #Draft.autogroup(newObj)
            App.ActiveDocument.recompute()
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(
                App.ActiveDocument.Name, newObj.Name, 'Face1', 0, 0, 0)
            selectedEdge = Gui.Selection.getSelectionEx(
            )[0].SubObjects[0]    # select one element

            # loft
            plDirection = App.Placement()
            yL = selectedEdge.CenterOfMass
            uv = selectedEdge.Surface.parameter(yL)
            nv = selectedEdge.normalAt(uv[0], uv[1])
            direction = yL.sub(nv + yL)
            r = App.Rotation(App.Vector(0, 0, 1), direction)
            plDirection.Rotation.Q = r.Q
            plDirection.Base = yL

            firstFace = newObj
            point = Draft.makePoint(0, 0.0, 10.0)

            newObj1 = App.ActiveDocument.addObject('Part::Loft', 'tempPyramid')
            App.ActiveDocument.ActiveObject.Sections = [firstFace, point, ]
            App.ActiveDocument.ActiveObject.Solid = True
            newObj1 = App.ActiveDocument.ActiveObject
            App.ActiveDocument.recompute()

            # copy
            App.ActiveDocument.addObject('Part::Feature', 'Pyramid').Shape = Part.getShape(
                newObj1, '', needSubElement=False, refine=False)
            App.ActiveDocument.recompute()

            # Remove Old objects. I don't like to keep so many objects without any necessity.
            for obj in newObj1.Sections:
                App.ActiveDocument.removeObject(obj.Name)
            # Gui.SendMsgToActiveView("ViewFit")
            App.ActiveDocument.removeObject(newObj1.Name)
            # App.ActiveDocument.removeObject(point)
            App.ActiveDocument.commitTransaction() #undo reg.
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,App.ActiveDocument.ActiveObject,deleteOnEscape = True)

        except Exception as err:
            App.Console.PrintError("'Pyramid' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Pyramid.svg',
            'MenuText': 'Pyramid',
                        'ToolTip':  'Pyramid'
        }

Gui.addCommand('Design456Part_Pyramid', Design456Part_Pyramid())


# Hemisphere
class Design456Part_Hemisphere:

    def Activated(self):
        try:
            neRadius= QtGui.QInputDialog.getDouble(None, "Radius", "Radius:",0,1.0,10000.0,2)[0]
            if(neRadius ==0 ):
                return #Nothing to do here.
            App.ActiveDocument.openTransaction(translate("Design456","Part Hemisphere"))
            neObj = App.ActiveDocument.addObject("Part::Sphere", "tempHemisphere")
            neObj.Radius=neRadius 
            neObj.Placement = App.Placement(App.Vector(
                0.00, 0.00, 0.00), App.Rotation(App.Vector(1.00, 0.00, 0.00), 90.00))
            neObj.Angle1 = '-90.00 deg'
            neObj.Angle2 = '90.00 deg'
            neObj.Angle3 = '180.00 deg'
            App.ActiveDocument.recompute()

            sh = neObj.Shape
            nsh = sh.defeaturing([sh.Face2, ])
            
            if not sh.isPartner(nsh):
                defeat = App.ActiveDocument.addObject(
                    'Part::Feature', 'Hemisphere')
                defeat.Shape = nsh
                App.ActiveDocument.removeObject(neObj.Name)
            else:
                App.Console.PrintError('Defeaturing failed\n')
            App.ActiveDocument.recompute()
            App.ActiveDocument.commitTransaction() #undo reg.
            newObj= App.ActiveDocument.ActiveObject
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)

        except Exception as err:
            App.Console.PrintError("'Part::Hemisphere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Hemisphere.svg',
            'MenuText': 'Part_Hemisphere',
                        'ToolTip':  'Part Hemisphere'
        }

Gui.addCommand('Design456Part_Hemisphere', Design456Part_Hemisphere())

# Ellipsoid


class Design456Part_Ellipsoid:

    def Activated(self):
        try:
            App.ActiveDocument.openTransaction(translate("Design456","Part Ellipsoid"))

            newObj = App.ActiveDocument.addObject(
                "Part::Ellipsoid", "Ellipsoid")
            App.ActiveDocument.ActiveObject.Label = "Ellipsoid"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.commitTransaction() #undo reg.
        except Exception as err:
            App.Console.PrintError("'Part::Ellipsoid' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Part_Ellipsoid.svg',
            'MenuText': 'Part_Ellipsoid',
                        'ToolTip':  'Part Ellipsoid'
        }

Gui.addCommand('Design456Part_Ellipsoid', Design456Part_Ellipsoid())

#########################################################################
#Macro_D_Un_Jour_Random_Color_Faces                                     #
#Author : Mario52                                                       #
#23/03/2021                                                             #
#https://forum.freecadweb.org/viewtopic.php?f=22&t=56732                #
# Modified and added to Design456 by :                                  #
# Mariwan Jalal     mariwan.jalal@gmail.com                             #
#########################################################################
class Design_ColorizeObject:
     
    def Activated(self): 
        import random
        try:
            sel = Gui.Selection.getSelection()  # selection object
            if len(sel) == 0:
                errmsg="Please select an object to apply the tool"
                faced.errorDialog(errmsg)
                return
            
            for selectedObj in sel:
                App.ActiveDocument.openTransaction(translate("Design456","Colorize"))
                colors = []
                for ii in range(len(selectedObj.Shape.Faces)):
                    base =random.uniform(0.3, 0.7)  # Randomize even the lower limit 
                    colors.append((random.uniform(base, 1),
                                   random.uniform(base , 1), 
                                   random.uniform(base , 1), 0.0)) #red, green, blue, transparency
                selectedObj.ViewObject.DiffuseColor = colors 
                App.ActiveDocument.commitTransaction() #undo reg.
            
        except Exception as err:
            App.Console.PrintError("'Design_ColorizeObject' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + 'Design456_Colorize.svg',
            'MenuText': 'Colorize object',
                        'ToolTip':  'Colorize object randomly'
        }

Gui.addCommand('Design_ColorizeObject', Design_ColorizeObject())

############################################################################

class Design456Part:
    import polyhedrons
    list = ["Design456Part_Box",
            "Design456Part_Cylinder",
            "Design456Part_Tube",
            "Design456Part_Sphere",
            "Design456Part_Cone",
            "Design456Part_Torus",
            "Design456Part_Wedge",
            "Design456Part_Prism",
            "Design456Part_Pyramid",
            "Design456Part_Hemisphere",
            "Design456Part_Ellipsoid",
            "Pyramid",
            "Tetrahedron",
            #"Hexahedron",               #No need for this as box is in part.
            "Octahedron",
            "Dodecahedron",
            "Icosahedron",
            "Icosahedron_truncated",
            "Geodesic_sphere"
            ]

    """Design456 Part Toolbar"""

    def GetResources(self):
        return{
            'Pixmap':   Design456Init.ICON_PATH + 'Part_Box.svg',
            'MenuText': 'Box',
                        'ToolTip': 'Box'
        }

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True
        