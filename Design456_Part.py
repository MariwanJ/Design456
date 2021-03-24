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
import Draft as _draft
import Part as _part
import FACE_D as faced

#import PartGui
import BasicShapes.CommandShapes
#import CompoundTools._CommandCompoundFilter
import CompoundTools._CommandExplodeCompound

import Design456Init
# from Part import CommandShapes     #Tube   not working



sys.path.append(Design456Init.PYRAMID_PATH)
class Design456_Part:
    import polyhedrons
    list = ["Design456_Part_Box",
            "Design456_Part_Cylinder",
            "Design456_Part_Tube",
            "Design456_Part_Sphere",
            "Design456_Part_Cone",
            "Design456_Part_Torus",
            "Design456_Part_Wedge",
            "Design456_Part_Prism",
            "Design456_Part_Pyramid",
            "Design456_Part_Hemisphere",
            "Design456_Part_Ellipsoid",
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
            'Pixmap':   Design456Init.ICON_PATH + '/Part_Box.svg',
            'MenuText': 'Box',
                        'ToolTip': 'Box'
        }

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True

    def Activated(self):
        self.appendToolbar("Design456_Part", self.list)

# BOX


class Design456_Part_Box:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Box", "Box")
            newObj.Label = "Cube"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Box' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Box.svg',
            'MenuText': 'Part_Box',
                        'ToolTip':  'Part Box'
        }


Gui.addCommand('Design456_Part_Box', Design456_Part_Box())

# Cylinder


class Design456_Part_Cylinder:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Cylinder", "Cylinder")
            App.ActiveDocument.ActiveObject.Label = "Cylinder"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Cylinder' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Cylinder.svg',
            'MenuText': 'Part_Cylinder',
                        'ToolTip':  'Part Cylinder'
        }


Gui.addCommand('Design456_Part_Cylinder', Design456_Part_Cylinder())


# Tube
class Design456_Part_Tube:

    def Activated(self):
        try:
            Gui.runCommand('Part_Tube', 0)
            newObj =App.ActiveDocument.ActiveObject
            v = Gui.ActiveDocument.ActiveView
            App.ActiveDocument.recompute()
            faced.PartMover(v,newObj,deleteOnEscape = True)
            App.ActiveDocument.recompute()
        except Exception as err:
            App.Console.PrintError("'Part::Tube' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Tube.svg',
            'MenuText': 'Part_Tube',
                        'ToolTip':  'Part Tube'
        }


Gui.addCommand('Design456_Part_Tube', Design456_Part_Tube())


# Shpere
class Design456_Part_Sphere:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Sphere", "Sphere")
            App.ActiveDocument.ActiveObject.Label = "Sphere"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Sphere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Sphere.svg',
            'MenuText': 'Part_Sphere',
                        'ToolTip':  'Part Sphere'
        }


Gui.addCommand('Design456_Part_Sphere', Design456_Part_Sphere())
# Cone


class Design456_Part_Cone:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Cone", "Cone")
            App.ActiveDocument.ActiveObject.Label = "Cone"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Cone' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Cone.svg',
            'MenuText': 'Part_Cone',
                        'ToolTip':  'Part Cone'
        }


Gui.addCommand('Design456_Part_Cone', Design456_Part_Cone())


# Cone
class Design456_Part_Torus:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Torus", "Torus")
            App.ActiveDocument.ActiveObject.Label = "Torus"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Torus' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Torus.svg',
            'MenuText': 'Part_Torus',
                        'ToolTip':  'Part Torus'
        }


Gui.addCommand('Design456_Part_Torus', Design456_Part_Torus())

# Wedge


class Design456_Part_Wedge:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Wedge", "Wedge")
            App.ActiveDocument.ActiveObject.Label = "Wedge"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Wedge' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Wedge.svg',
            'MenuText': 'Part_Wedge',
                        'ToolTip':  'Part Wedge'
        }


Gui.addCommand('Design456_Part_Wedge', Design456_Part_Wedge())


# Prism
class Design456_Part_Prism:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject("Part::Prism", "Prism")
            App.ActiveDocument.ActiveObject.Label = "Prism"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Prism' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Prism.svg',
            'MenuText': 'Part_Prism',
                        'ToolTip':  'Part Prism'
        }


Gui.addCommand('Design456_Part_Prism', Design456_Part_Prism())


# Pyramid
class Design456_Part_Pyramid:

    def Activated(self):
        try:

            obj = App.Placement()
            Faces = QtGui.QInputDialog.getInt(None, "Faces", "Faces:")[0]
            if(Faces==0):
                return # Nothing to do here 
            obj.Rotation.Q = (0.0, 0.0, 0, 1.0)
            obj.Base = App.Vector(0.0, 0.0, 0.0)
            newObj = _draft.makePolygon(
                Faces, radius=10, inscribed=True, placement=obj, face=True, support=None)
            _draft.autogroup(newObj)
            App.ActiveDocument.recompute()
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(
                App.ActiveDocument.Name, newObj.Name, 'Face1', 0, 0, 0)
            selectedEdge = Gui.Selection.getSelectionEx(
            )[0].SubObjects[0]    # select one element

            # loft
            plr = plDirection = App.Placement()
            yL = selectedEdge.CenterOfMass
            uv = selectedEdge.Surface.parameter(yL)
            nv = selectedEdge.normalAt(uv[0], uv[1])
            direction = yL.sub(nv + yL)
            r = App.Rotation(App.Vector(0, 0, 1), direction)
            plDirection.Rotation.Q = r.Q
            plDirection.Base = yL
            plr = plDirection

            firstFace = newObj
            point = _draft.makePoint(0, 0.0, 10.0)

            newObj1 = App.activeDocument().addObject('Part::Loft', 'tempPyramid')
            App.ActiveDocument.ActiveObject.Sections = [firstFace, point, ]
            App.ActiveDocument.ActiveObject.Solid = True
            newObj1 = App.ActiveDocument.ActiveObject
            App.ActiveDocument.recompute()

            # copy
            newOBJ = App.ActiveDocument.addObject('Part::Feature', 'Pyramid').Shape = _part.getShape(
                newObj1, '', needSubElement=False, refine=False)
            App.ActiveDocument.recompute()

            # Remove Old objects. I don't like to keep so many objects without any necessity.
            for obj in newObj1.Sections:
                App.ActiveDocument.removeObject(obj.Name)
            # Gui.SendMsgToActiveView("ViewFit")
            App.ActiveDocument.removeObject(newObj1.Name)
            # App.ActiveDocument.removeObject(point)
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,App.ActiveDocument.ActiveObject,deleteOnEscape = True)

        except Exception as err:
            App.Console.PrintError("'Part::Pyramid' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Pyramid.svg',
            'MenuText': 'Part_Pyramid',
                        'ToolTip':  'Part Pyramid'
        }


Gui.addCommand('Design456_Part_Pyramid', Design456_Part_Pyramid())


# Hemisphere
class Design456_Part_Hemisphere:

    def Activated(self):
        try:

            neRaduis= QtGui.QInputDialog.getDouble(None, "Radius", "Radius:",0,1.0,10000.0,2)[0]
            if(neRaduis==0):
                return #Nothing to do here.
            neObj = App.ActiveDocument.addObject("Part::Sphere", "tempHemisphere")
            neObj.Radius=neRaduis 
            neObj.Placement = App.Placement(App.Vector(
                0.00, 0.00, 0.00), App.Rotation(App.Vector(1.00, 0.00, 0.00), 90.00))
            neObj.Angle1 = '-90.00 deg'
            neObj.Angle2 = '90.00 deg'
            neObj.Angle3 = '180.00 deg'
            App.ActiveDocument.recompute()
            # Gui.SendMsgToActiveView("ViewFit")
            sh = neObj.Shape
            nsh = sh.defeaturing([sh.Face2, ])
            defat=None
            if not sh.isPartner(nsh):
                defeat = App.ActiveDocument.addObject(
                    'Part::Feature', 'Hemisphere').Shape = nsh
                App.ActiveDocument.removeObject(neObj.Name)
            else:
                App.Console.PrintError('Defeaturing failed\n')
            App.ActiveDocument.recompute()
            newObj= App.ActiveDocument.ActiveObject
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,App.ActiveDocument.ActiveObject,deleteOnEscape = True)

        except Exception as err:
            App.Console.PrintError("'Part::Hemisphere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Hemisphere.svg',
            'MenuText': 'Part_Hemisphere',
                        'ToolTip':  'Part Hemisphere'
        }


Gui.addCommand('Design456_Part_Hemisphere', Design456_Part_Hemisphere())

# Ellipsoid


class Design456_Part_Ellipsoid:

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject(
                "Part::Ellipsoid", "Ellipsoid")
            App.ActiveDocument.ActiveObject.Label = "Ellipsoid"
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v,newObj,deleteOnEscape = True)
            # Gui.SendMsgToActiveView("ViewFit")
        except Exception as err:
            App.Console.PrintError("'Part::Ellipsoid' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Part_Ellipsoid.svg',
            'MenuText': 'Part_Ellipsoid',
                        'ToolTip':  'Part Ellipsoid'
        }


Gui.addCommand('Design456_Part_Ellipsoid', Design456_Part_Ellipsoid())

#Macro_D_Un_Jour_Random_Color_Faces
#Mario52
#23/03/2021
#https://forum.freecadweb.org/viewtopic.php?f=22&t=56732
#
class Design_ColorizeObject:
     
    def Activated(self): 
        import random
        try:
            aa = Gui.Selection.getSelection()[0]  # selection objet
            colors = []
            for ii in range(len(aa.Shape.Faces)):
                colors.append((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 0.0)) #red, green, blue, transparence
       
            aa.ViewObject.DiffuseColor = colors 
        
        except Exception as err:
            App.Console.PrintError("'Part::Hemisphere' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def GetResources(self):
        return {
            'Pixmap': Design456Init.ICON_PATH + '/Design456_Colorize.svg',
            'MenuText': 'Colorize object',
                        'ToolTip':  'Colorize object randomly'
        }
Gui.addCommand('Design_ColorizeObject', Design_ColorizeObject())