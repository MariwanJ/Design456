# ***************************************************************************
# *	  Copyright (c) 2019  Eddy Verlinden , Genk Belgium	  (eddyverl)		*
# *																			*
# *	  This file is a part of the FreeCAD CAx development system.			*
# *																			*
# *	  This program is free software; you can redistribute it and/or modify	*
# *	  it under the terms of the GNU Lesser General Public License (LGPL)	*
# *	  as published by the Free Software Foundation; either version 2 of		*
# *	  the License, or (at your option) any later version.					*
# *	  for detail see the LICENCE text file.									*
# *																			*
# *	  FreeCAD is distributed in the hope that it will be useful,			*
# *	  but WITHOUT ANY WARRANTY; without even the implied warranty of		*
# *	  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the			*
# *	  GNU Lesser General Public License for more details.					*
# *																			*
# *	  You should have received a copy of the GNU Library General Public		*
# *	  License along with FreeCAD; if not, write to the Free Software		*
# *	  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA	02111-1307	*
# *	  USA																	*
# *																			*
# ***************************************************************************

# Based on examples at : https://www.freecadweb.org/wiki/Workbench_creation

# Version 01.07


# Version 01.02	 (2020-01-15)
# added geodesic sphere

# version 01.03	  (2020-01-23)
# added hexahedron	(cube)

# version 01.04	 (2020-01-30)
# renamed Mod to Pyramids-and-Polyhedrons

# version 01.05	 (2020-02-24)
# Side of icosahedron_truncated was side of icosahedron -> corrected

# version 01.06	 (2020-12-21)
# Pyramids are rotatable around the z-axis and start parallel to the x-axis

# version 01.07	 (2020-12-26)
# Some namechanges

# version 01.07a (2020-12-30)
# flexibility for installation folder

# version 01.07b (2020-01-02)
# icosahedron_truncated : now radius of the result, not of the base icosahedron


import FreeCAD as App
import FreeCADGui as Gui
import Part as _part
import math
import sys
import os
from FreeCAD import Base
import Design456Init
import FACE_D as faced


def horizontal_regular_polygon_vertexes(sidescount, radius, z, startangle=0):
    try:
        vertexes = []
        if radius is not 0:
            for i in range(0, sidescount+1):
                angle = 2 * math.pi * i / sidescount + math.pi + startangle
                vertex = (radius * math.cos(angle),
                          radius * math.sin(angle), z)
                vertexes.append(vertex)
        else:
            vertex = (0, 0, z)
            vertexes.append(vertex)
        return vertexes
    except Exception as err:
        App.Console.PrintError("'horizontal_regular_polygon_vertexes' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return


# angle in degrees
def horizontal_regular_pyramid_vertexes(sidescount, radius, z, anglez=0):
    try:
        vertexes = []
        odd = 0
        if (sidescount % 2) is 0:
            odd = 1
        if radius is not 0:
            for i in range(0, sidescount+1):
                angle = 2 * math.pi * i / sidescount + \
                    (math.pi * (odd/sidescount + 1/2)) + anglez * math.pi / 180
                vertex = (radius * math.cos(angle),
                          radius * math.sin(angle), z)
                vertexes.append(vertex)
        else:
            vertex = (0, 0, z)
            vertexes.append(vertex)
        return vertexes
    except Exception as err:
        App.Console.PrintError("'horizontal_regular_pyramid_vertexes' Failed. "
                               "{err}\n".format(err=str(err)))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return


def getWorkbenchFolder():

    return (Design456Init.PYRAMID_PATH)

    import os.path
    from os import path

    import workbenchfolders

    basedir = str(App.getUserAppDataDir())
    folder = ""

    for tryfolder in workbenchfolders.recommended_folders:
        if path.exists(basedir + tryfolder):
            folder = basedir + tryfolder
            return folder

    for tryfolder in workbenchfolders.user_chosen_folders:
        if path.exists(basedir + tryfolder):
            folder = basedir + tryfolder
            return folder
        if path.exists(tryfolder):
            folder = tryfolder
            return folder

    return ""


# ===========================================================================

class ViewProviderBox:

    obj_name = "Dodecahedron"

    def __init__(self, obj, obj_name):
        self.obj_name = obj_name
        obj.Proxy = self

    def attach(self, obj):
        return

    def updateData(self, fp, prop):
        return

    def getDisplayModes(self, obj):
        return "As Is"

    def getDefaultDisplayMode(self):
        return "As Is"

    def setDisplayMode(self, mode):
        return "As Is"

    def onChanged(self, vobj, prop):
        pass

    def getIcon(self):
        # return str(App.getUserAppDataDir()) + 'Mod' + 'Pyramids-and-Polyhedrons/Resources/Icons/' + (self.obj_name).lower() + '.svg'
        return getWorkbenchFolder() + "/Resources/Icons/' + (self.obj_name).lower() + '.svg'"

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

# ===========================================================================


class Pyramid:

    radius1value = 0
    radius2value = 0
    sidescountvalue = 0
    side1value = 0
    side2value = 0
    anglez = 0

    def __init__(self, obj, sidescount=5, radius_bottom=2, radius_top=4, height=10, angz=0):
        obj.addProperty("App::PropertyLength", "Radius1", "Pyramid",
                        "Radius of the pyramid").Radius1 = radius_bottom
        obj.addProperty("App::PropertyLength", "Radius2", "Pyramid",
                        "Radius of the pyramid").Radius2 = radius_top
        obj.addProperty("App::PropertyLength", "Height",
                        "Pyramid", "Height of the pyramid").Height = height
        obj.addProperty("App::PropertyInteger", "Sidescount", "Pyramid",
                        "Sidescount of the pyramid").Sidescount = sidescount
        obj.addProperty("App::PropertyLength", "Sidelength1",
                        "Pyramid", "Sidelength1 of the pyramid")
        obj.addProperty("App::PropertyLength", "Sidelength2",
                        "Pyramid", "Sidelength2 of the pyramid")
        obj.addProperty("App::PropertyAngle", "Z_rotation",
                        "Pyramid", "alfa angle around Z").Z_rotation = angz

        obj.Proxy = self

    def execute(self, obj):
        try:
            sidescount = int(obj.Sidescount)
            angle = 2 * math.pi / sidescount
            radius_bottom = float(obj.Radius1)
            radius_top = float(obj.Radius2)
            sidelength_top = float(obj.Sidelength2)
            sidelength_bottom = float(obj.Sidelength1)
            height = float(obj.Height)
            anglez = float(obj.Z_rotation)

            if radius_bottom != self.radius1value or sidescount != self.sidescountvalue:
                obj.Sidelength1 = radius_bottom * math.sin(angle/2) * 2
                self.radius1value = radius_bottom
                self.side1value = float(obj.Sidelength1)
            elif sidelength_bottom != self.side1value:
                self.radius1value = float(
                    obj.Sidelength1 / 2) / math.sin(angle/2)
                obj.Radius1 = self.radius1value
                radius_bottom = self.radius1value
                self.side1value = float(obj.Sidelength1)

            if radius_top != self.radius2value or sidescount != self.sidescountvalue:
                obj.Sidelength2 = radius_top * math.sin(angle/2) * 2
                self.radius2value = float(radius_top)
                self.side2value = float(obj.Sidelength2)
            elif sidelength_top != self.side2value:
                self.radius2value = float(
                    obj.Sidelength2 / 2) / math.sin(angle/2)
                obj.Radius2 = self.radius2value
                radius_top = self.radius2value
                self.side2value = float(obj.Sidelength2)

            self.sidescountvalue = sidescount
            faces = []
            if radius_bottom is 0 and radius_top is 0:
                App.Console.PrintMessage("Both radiuses are zero" + "\n")
            else:
                vertexes_bottom = horizontal_regular_pyramid_vertexes(
                    sidescount, radius_bottom, 0, anglez)
                vertexes_top = horizontal_regular_pyramid_vertexes(
                    sidescount, radius_top, height, anglez)

                if radius_bottom is not 0:
                    polygon_bottom = _part.makePolygon(vertexes_bottom)
                    face_bottom = _part.Face(polygon_bottom)
                    faces.append(face_bottom)
                if radius_top is not 0:
                    polygon_top = _part.makePolygon(vertexes_top)
                    face_top = _part.Face(polygon_top)
                    faces.append(face_top)

                for i in range(sidescount):
                    if radius_top is 0:
                        vertexes_side = [
                            vertexes_bottom[i], vertexes_bottom[i+1], vertexes_top[0], vertexes_bottom[i]]
                    elif radius_bottom is 0:
                        vertexes_side = [
                            vertexes_bottom[0], vertexes_top[i+1], vertexes_top[i], vertexes_bottom[0]]
                    else:
                        vertexes_side = [vertexes_bottom[i], vertexes_bottom[i+1],
                                         vertexes_top[i+1], vertexes_top[i], vertexes_bottom[i]]
                    polygon_side = _part.makePolygon(vertexes_side)
                    faces.append(_part.Face(polygon_side))

                shell = _part.makeShell(faces)
                solid = _part.makeSolid(shell)
                obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'Class Pyramid' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class PyramidCommand:

    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/pyramid.svg',
                'Accel': "Shift+P",
                'MenuText': "Pyramid",
                'ToolTip': "Generate a Pyramid with any number of sides"}

    def Activated(self):
        try:
            # see https://www.freecadweb.org/wiki/Creating_a_FeaturePython_Box,_Part_II
            newObj = App.ActiveDocument.addObject(
                "Part::FeaturePython", "Pyramid")
            Pyramid(newObj)
            ViewProviderBox(newObj.ViewObject, "Pyramid")
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v, newObj, deleteOnEscape=True)
        except Exception as err:
            App.Console.PrintError("'PyramidCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


Gui.addCommand('Pyramid', PyramidCommand())


# ===========================================================================

class Tetrahedron:
    # == basics ==
    # R = z / 4 * sqrt(6)
    # ro = z / 12 * sqrt(6)	  -->	ro = R / 3
    # z = 4 * R / sqrt(6)
    # h = z / 3 * sqrt(6) = 4 * R / sqrt(6) /3 * sqrt(6) = 4 * R / 3	 = ro + R
    # radius at level = z / 2 / cos(30) = (4 * R / sqrt(6)) / 2 / sqrt(3) * 2 = 4 * R / (sqrt(6) * sqrt(3))= 4 * R / (3 * sqrt(2)

    radiusvalue = 0

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength", "Radius", "Tetrahedron",
                        "Radius of the tetrahedron").Radius = radius
        obj.addProperty("App::PropertyLength", "Side",
                        "Tetrahedron", "Sidelength of the tetrahedron")
        obj.Proxy = self

    def execute(self, obj):
        try:
            radius = float(obj.Radius)
            if (radius != self.radiusvalue):
                obj.Side = radius * 4 / math.sqrt(6)
                self.radiusvalue = radius
            else:
                self.radiusvalue = float(obj.Side * math.sqrt(6) / 4)
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue

            faces = []
            vertexes_bottom = horizontal_regular_polygon_vertexes(
                3, 4*radius/3/math.sqrt(2), - radius / 3)
            vertexes_top = horizontal_regular_polygon_vertexes(1, 0, radius)

            for i in range(3):
                vertexes_side = [
                    vertexes_bottom[i], vertexes_bottom[i+1], vertexes_top[0], vertexes_bottom[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            polygon_bottom = _part.makePolygon(vertexes_bottom)

            faces.append(_part.Face(polygon_bottom))
            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'PyramidCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class TetrahedronCommand:

    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/tetrahedron.svg',
                'Accel': "Shift+T",
                'MenuText': "Tetrahedron",
                'ToolTip': "Generate a Tetrahedron"}

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject(
                "Part::FeaturePython", "Tetrahedron")
            Tetrahedron(newObj)
            ViewProviderBox(newObj.ViewObject, "Tetrahedron")
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v, newObj, deleteOnEscape=True)
        except Exception as err:
            App.Console.PrintError("'TetrahedronCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


Gui.addCommand('Tetrahedron', TetrahedronCommand())

# ===========================================================================


class Hexahedron:

    radiusvalue = 0

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength", "Radius", "Hexahedron",
                        "Radius of the hexahedron").Radius = radius
        obj.addProperty("App::PropertyLength", "Side",
                        "Hexahedron", "Sidelength of the hexahedron")
        obj.Proxy = self

    def execute(self, obj):
        try:

            radius = float(obj.Radius)
            if (radius != self.radiusvalue):
                side = radius * 2 / math.sqrt(3)
                obj.Side = side
                self.radiusvalue = radius
            else:
                self.radiusvalue = obj.Side / 2 * math.sqrt(3)
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue
                side = obj.Side

            faces = []
            vertexes_bottom = horizontal_regular_polygon_vertexes(
                4, math.sqrt(side ** 2 / 2), - side/2, math.pi/4)
            vertexes_top = horizontal_regular_polygon_vertexes(
                4, math.sqrt(side ** 2 / 2), side/2, math.pi/4)

            for i in range(4):
                vertexes_side = [vertexes_bottom[i], vertexes_bottom[i+1],
                                 vertexes_top[i+1], vertexes_top[i], vertexes_bottom[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            polygon_bottom = _part.makePolygon(vertexes_bottom)
            faces.append(_part.Face(polygon_bottom))

            polygon_top = _part.makePolygon(vertexes_top)
            faces.append(_part.Face(polygon_top))

            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid
        except Exception as err:
            App.Console.PrintError("'Hexahedron' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class HexahedronCommand:

    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/hexahedron.svg',
                'Accel': "Shift+T",
                'MenuText': "Hexahedron",
                'ToolTip': "Generate a Hexahedron"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Hexahedron")
        Hexahedron(newObj)
        ViewProviderBox(newObj.ViewObject, "Hexahedron")
        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Hexahedron', HexahedronCommand())
# ===========================================================================


class Octahedron:
    # Z = R * sqrt(2)
    radiusvalue = 0

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength", "Radius", "Octahedron",
                        "Radius of the octahedron").Radius = radius
        obj.addProperty("App::PropertyLength", "Side",
                        "Octahedron", "Sidelength of the octahedron")
        obj.Proxy = self

    def execute(self, obj):
        try:
            radius = float(obj.Radius)
            if (radius != self.radiusvalue):
                obj.Side = radius * math.sqrt(2)
                self.radiusvalue = radius
            else:
                self.radiusvalue = float(obj.Side / math.sqrt(2))
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue

            faces = []
            vertexes_middle = horizontal_regular_polygon_vertexes(4, radius, 0)
            vertexes_bottom = horizontal_regular_polygon_vertexes(
                1, 0, -radius)
            vertexes_top = horizontal_regular_polygon_vertexes(1, 0, radius)

            for i in range(4):
                vertexes_side = [
                    vertexes_middle[i], vertexes_middle[i+1], vertexes_top[0], vertexes_middle[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            for i in range(4):
                vertexes_side = [vertexes_middle[i], vertexes_middle[i+1],
                                 vertexes_bottom[0], vertexes_middle[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'Octahedron' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class OctahedronCommand:

    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/octahedron.svg',
                'Accel': "Shift+O",
                'MenuText': "Octahedron",
                'ToolTip': "Generate a Octahedron"}

    def Activated(self):
        try:
            newObj = App.ActiveDocument.addObject(
                "Part::FeaturePython", "Octahedron")
            Octahedron(newObj)
            ViewProviderBox(newObj.ViewObject, "Octahedron")
            App.ActiveDocument.recompute()
            v = Gui.ActiveDocument.ActiveView
            faced.PartMover(v, newObj, deleteOnEscape=True)
        except Exception as err:
            App.Console.PrintError("'OctahedronCommand' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


Gui.addCommand('Octahedron', OctahedronCommand())

# ===========================================================================


class Dodecahedron:

    radiusvalue = 0

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength", "Radius", "Dodecahedron",
                        "Radius of the dodecahedron").Radius = radius
        obj.addProperty("App::PropertyLength", "Side",
                        "Dodecahedron", "Sidelength of the dodecahedron")
        obj.Proxy = self

    def execute(self, obj):
        try:
            angleribs = 121.717474411
            anglefaces = 116.565051177

            radius = float(obj.Radius)
            if (radius != self.radiusvalue):
                obj.Side = 4 * radius / (math.sqrt(3) * (1 + math.sqrt(5)))
                self.radiusvalue = radius
            else:
                self.radiusvalue = float(
                    obj.Side * (math.sqrt(3) * (1 + math.sqrt(5))) / 4)
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue

            faces = []
            z = 4 * radius / (math.sqrt(3) * (1 + math.sqrt(5)))
            r = z/2 * math.sqrt((25 + (11 * math.sqrt(5)))/10)
            # int sphere r is height / 2

            h2 = z * math.sin(angleribs/180 * math.pi)

            # height of the side-tips
            radius1 = z / 2 / math.sin(36 * math.pi / 180)
            h5h = (radius1 + radius1 * math.cos(36 * math.pi / 180)) * \
                math.sin(anglefaces * math.pi / 180)  # height of the tops

            radius2 = radius1 - z * math.cos(angleribs * math.pi / 180)

            r = (h2 + h5h)/2  # XXX to make it fit!

            vertexes_bottom = horizontal_regular_polygon_vertexes(
                5, radius1, -r)
            vertexes_low = horizontal_regular_polygon_vertexes(
                5, radius2, -r + h2)
            vertexes_high = horizontal_regular_polygon_vertexes(
                5, radius2, -r + h5h,  math.pi/5)
            vertexes_top = horizontal_regular_polygon_vertexes(
                5, radius1, r, math.pi/5)

            polygon_bottom = _part.makePolygon(vertexes_bottom)
            face_bottom = _part.Face(polygon_bottom)
            faces.append(face_bottom)

            polygon_top = _part.makePolygon(vertexes_top)
            face_top = _part.Face(polygon_top)
            faces.append(face_top)

            for i in range(5):
                vertexes_side = [vertexes_bottom[i], vertexes_bottom[i+1],
                                 vertexes_low[i+1], vertexes_high[i], vertexes_low[i], vertexes_bottom[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            for i in range(5):
                # vertexes_side=[vertexes_top[i],vertexes_top[i+1],vertexes_high[i+1],vertexes_high2[i], vertexes_high[i],vertexes_top[i] ]
                vertexes_side = [vertexes_top[i], vertexes_top[i+1], vertexes_high[i+1],
                                 vertexes_low[i+1], vertexes_high[i], vertexes_top[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'Dodecahedron' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class DodecahedronCommand:
    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/dodecahedron.svg',
                'Accel': "Shift+D",
                'MenuText': "Dodecahedron",
                'ToolTip': "Generate a Dodecahedron"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Dodecahedron")
        Dodecahedron(newObj)
        ViewProviderBox(newObj.ViewObject, "Dodecahedron")
        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Dodecahedron', DodecahedronCommand())

# ===========================================================================


class Icosahedron:

    radiusvalue = 0

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength", "Radius", "Icosahedron",
                        "Radius of the icosahedron").Radius = radius
        obj.addProperty("App::PropertyLength", "Side",
                        "Icosahedron", "Sidelength of the icosahedron")
        obj.Proxy = self

    def execute(self, obj):

        try:
            radius = float(obj.Radius)
            if (radius != self.radiusvalue):
                obj.Side = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
                self.radiusvalue = radius
            else:
                self.radiusvalue = float(
                    obj.Side * math.sqrt(10 + 2 * math.sqrt(5)) / 4)
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue

            z = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
            anglefaces = 138.189685104
            r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))

            # radius of a pentagram with the same side
            radius2 = z / math.sin(36 * math.pi/180)/2
            # height of radius2 in the sphere

            angle = math.acos(radius2/radius)
            height = radius * math.sin(angle)

            faces = []

            vertex_bottom = (0, 0, -radius)
            vertexes_low = horizontal_regular_polygon_vertexes(
                5, radius2, -height)
            vertexes_high = horizontal_regular_polygon_vertexes(
                5, radius2, height, math.pi/5)
            vertex_top = (0, 0, radius)

            for i in range(5):
                vertexes_side = [vertex_bottom, vertexes_low[i],
                                 vertexes_low[i+1], vertex_bottom]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            for i in range(5):
                vertexes_side = [vertexes_low[i], vertexes_low[i+1],
                                 vertexes_high[i], vertexes_low[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))
                vertexes_side = [vertexes_high[i], vertexes_high[i+1],
                                 vertexes_low[i+1], vertexes_high[i]]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            for i in range(5):
                vertexes_side = [vertex_top, vertexes_high[i],
                                 vertexes_high[i+1], vertex_top]
                polygon_side = _part.makePolygon(vertexes_side)
                faces.append(_part.Face(polygon_side))

            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'Icosahedron' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class IcosahedronCommand:
    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/icosahedron.svg',
                'Accel': "Shift+I",
                'MenuText': "Icosahedron",
                'ToolTip': "Generate a Icosahedron"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Icosahedron")
        Icosahedron(newObj)

        ViewProviderBox(newObj.ViewObject, "Icosahedron")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Icosahedron', IcosahedronCommand())

# ===========================================================================


class Icosahedron_truncated:

    radiusvalue = 0

    def __init__(self, obj, radius=5):
        obj.addProperty("App::PropertyLength", "Radius",
                        "Icosahedron_truncated", "Radius").Radius = radius
        obj.addProperty("App::PropertyLength", "Side",
                        "Icosahedron_truncated", "Sidelength")
        obj.Proxy = self

    def execute(self, obj):
        try:
            # correction for Icosohedron --> truncated
            radius = float(obj.Radius) * 1.144
            if (radius != self.radiusvalue):
                obj.Side = 4*radius / math.sqrt(10 + 2 * math.sqrt(5)) / 3
                self.radiusvalue = radius
            else:
                self.radiusvalue = float(
                    obj.Side * math.sqrt(10 + 2 * math.sqrt(5)) / 4) * 3
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue

            z = float(4*radius) / math.sqrt(10 + 2 *
                                            math.sqrt(5))  # z of base icosahedron
            anglefaces = 138.189685104
            r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))

            # radius of a pentagram with the same side
            radius2 = z / math.sin(36 * math.pi/180)/2

            # height of radius2 in the sphere
            angle = math.acos(radius2/radius)
            height = radius * math.sin(angle)

            faces = []

            vertex_bottom = (0, 0, -radius)
            vertexes_low = horizontal_regular_polygon_vertexes(
                5, radius2, -height)
            vertexes_high = horizontal_regular_polygon_vertexes(
                5, radius2, height,	 -math.pi/5)
            vertex_top = (0, 0, radius)

            vertexes_bottom = []
            vertexes_top = []

            for i in range(6):
                new_vertex = ((vertex_bottom[0]+vertexes_low[i][0])/3, (vertex_bottom[1] +
                                                                        vertexes_low[i][1])/3, vertex_bottom[2]-(vertex_bottom[2]-vertexes_low[i][2])/3)
                vertexes_bottom.append(new_vertex)
            polygon_side = _part.makePolygon(vertexes_bottom)
            faces.append(_part.Face(polygon_side))

            for i in range(6):
                new_vertex = ((vertex_top[0]+vertexes_high[i][0])/3, (vertex_top[1] +
                                                                      vertexes_high[i][1])/3, vertex_top[2]-(vertex_top[2]-vertexes_high[i][2])/3)
                vertexes_top.append(new_vertex)
            polygon_side = _part.makePolygon(vertexes_top)
            faces.append(_part.Face(polygon_side))

            pg6_bottom = []
            for i in range(5):
                vertex1 = vertexes_bottom[i]
                vertex2 = vertexes_bottom[i+1]
                vertex3 = (vertexes_bottom[i+1][0] + (vertexes_low[i+1][0] - vertexes_bottom[i+1][0])/2, vertexes_bottom[i+1][1] + (
                    vertexes_low[i+1][1] - vertexes_bottom[i+1][1])/2, (vertexes_low[i+1][2] + vertexes_bottom[i+1][2])/2)
                vertex4 = ((vertexes_low[i+1][0]*2 + vertexes_low[i][0])/3,
                           (vertexes_low[i+1][1]*2 + vertexes_low[i][1])/3, -height)
                vertex5 = ((vertexes_low[i+1][0]+vertexes_low[i][0]*2)/3,
                           (vertexes_low[i+1][1] + vertexes_low[i][1]*2)/3, -height)
                vertex6 = (vertexes_bottom[i][0] + (vertexes_low[i][0] - vertexes_bottom[i][0])/2, vertexes_bottom[i][1] + (
                    vertexes_low[i][1] - vertexes_bottom[i][1])/2, (vertexes_low[i][2] + vertexes_bottom[i][2])/2)
                vertexes = [vertex1, vertex2, vertex3,
                            vertex4, vertex5, vertex6, vertex1]
                pg6_bottom.append(vertexes)
                polygon_side = _part.makePolygon(vertexes)
                faces.append(_part.Face(polygon_side))

            pg6_top = []
            for i in range(5):
                vertex1 = vertexes_top[i]
                vertex2 = vertexes_top[i+1]
                vertex3 = (vertexes_top[i+1][0] + (vertexes_high[i+1][0] - vertexes_top[i+1][0])/2, vertexes_top[i+1][1] + (
                    vertexes_high[i+1][1] - vertexes_top[i+1][1])/2, (vertexes_high[i+1][2] + vertexes_top[i+1][2])/2)
                vertex4 = ((vertexes_high[i+1][0]*2 + vertexes_high[i][0])/3,
                           (vertexes_high[i+1][1]*2 + vertexes_high[i][1])/3, height)
                vertex5 = ((vertexes_high[i+1][0]+vertexes_high[i][0]*2)/3,
                           (vertexes_high[i+1][1] + vertexes_high[i][1]*2)/3, height)
                vertex6 = (vertexes_top[i][0] + (vertexes_high[i][0] - vertexes_top[i][0])/2, vertexes_top[i][1] + (
                    vertexes_high[i][1] - vertexes_top[i][1])/2, (vertexes_high[i][2] + vertexes_top[i][2])/2)
                vertexes = [vertex1, vertex2, vertex3,
                            vertex4, vertex5, vertex6, vertex1]
                pg6_top.append(vertexes)
                polygon_side = _part.makePolygon(vertexes)
                faces.append(_part.Face(polygon_side))

            pg6_low = []
            for i in range(5):
                vertex1 = pg6_bottom[i][3]
                vertex2 = pg6_bottom[i][4]
                vertex3 = ((vertexes_low[i][0]*2 + vertexes_high[i+1][0])/3, (vertexes_low[i][1]
                                                                              * 2 + vertexes_high[i+1][1])/3, (vertexes_low[i][2]*2 + vertexes_high[i+1][2])/3)
                vertex4 = ((vertexes_low[i][0] + vertexes_high[i+1][0]*2)/3, (vertexes_low[i][1] +
                                                                              vertexes_high[i+1][1]*2)/3, (vertexes_low[i][2] + vertexes_high[i+1][2]*2)/3)
                vertex5 = ((vertexes_low[i+1][0] + vertexes_high[i+1][0]*2)/3, (vertexes_low[i+1]
                                                                                [1] + vertexes_high[i+1][1]*2)/3, (vertexes_low[i+1][2] + vertexes_high[i+1][2]*2)/3)
                vertex6 = ((vertexes_low[i+1][0]*2 + vertexes_high[i+1][0])/3, (vertexes_low[i+1][1]
                                                                                * 2 + vertexes_high[i+1][1])/3, (vertexes_low[i+1][2]*2 + vertexes_high[i+1][2])/3)
                vertexes = [vertex1, vertex2, vertex3,
                            vertex4, vertex5, vertex6, vertex1]
                pg6_low.append(vertexes)
                polygon_side = _part.makePolygon(vertexes)
                faces.append(_part.Face(polygon_side))

            pg6_high = []
            for i in range(5):
                vertex1 = pg6_top[i][3]
                vertex2 = pg6_top[i][4]
                vertex3 = pg6_low[i-1][4]
                vertex4 = pg6_low[i-1][5]
                vertex5 = pg6_low[i][2]
                vertex6 = pg6_low[i][3]
                vertexes = [vertex1, vertex2, vertex3,
                            vertex4, vertex5, vertex6, vertex1]
                pg6_high.append(vertexes)
                polygon_side = _part.makePolygon(vertexes)
                faces.append(_part.Face(polygon_side))

            for i in range(5):
                vertex1 = pg6_top[i][4]
                vertex2 = pg6_top[i][5]
                vertex3 = pg6_high[i-1][6]
                vertex4 = pg6_high[i-1][5]
                vertex5 = pg6_low[i-1][4]
                vertexes = [vertex1, vertex2, vertex3,
                            vertex4, vertex5, vertex1]
                polygon_side = _part.makePolygon(vertexes)
                faces.append(_part.Face(polygon_side))

            for i in range(5):
                vertex1 = pg6_bottom[i][4]
                vertex2 = pg6_bottom[i][5]
                vertex3 = pg6_low[i-1][6]
                vertex4 = pg6_low[i-1][5]
                vertex5 = pg6_high[i][4]
                vertexes = [vertex1, vertex2, vertex3,
                            vertex4, vertex5, vertex1]
                polygon_side = _part.makePolygon(vertexes)
                faces.append(_part.Face(polygon_side))

            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'Icosahedron_truncated' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class IcosahedronTrCommand:
    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/icosahedron_trunc.svg',
                'Accel': "Shift+F",
                'MenuText': "Icosahedron truncated",
                'ToolTip': "Generate a Truncated Icosahedron (football)"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Icosahedron_truncated")
        Icosahedron_truncated(newObj)

        ViewProviderBox(newObj.ViewObject, "Icosahedron_trunc")

        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Icosahedron_truncated', IcosahedronTrCommand())

# ===========================================================================


def geodesic_radius2side(radius, div):
    # approximative experience values! Not all sides are equal!
    dictsides = {"2": 618.034, "3": 412.41, "4": 312.87, "5": 245.09,
                 "6": 205.91, "7": 173.53, "8": 152.96, "9": 135.96, "10": 121.55}
    div = int(round(div))
    if div < 0:
        return 0
    if div == 1:
        return radius * 4 / math.sqrt(10 + 2 * math.sqrt(5))
    elif div <= 10:
        factor = dictsides[str(div)]
        return radius * factor / 1000


def geodesic_side2radius(side, div):
    # approximatily experience values!	Not all sides are equal!
    dictsides = {"2": 618.034, "3": 412.41, "4": 312.87, "5": 245.09,
                 "6": 205.91, "7": 173.53, "8": 152.96, "9": 135.96, "10": 121.55}
    div = int(round(div))
    if div < 0:
        return 0
    if div == 1:
        return side / 4 * math.sqrt(10 + 2 * math.sqrt(5))
    elif div <= 10:
        factor = dictsides[str(div)]
        return side * 1000 / factor


# ===========================================================================

class Geodesic_sphere:

    radiusvalue = 0
    divided_by = 2

    def __init__(self, obj, radius=5, div=2):
        obj.addProperty("App::PropertyLength", "Radius",
                        "Geodesic", "Radius of the sphere").Radius = radius
        obj.addProperty("App::PropertyLength", "Side", "Geodesic",
                        "Sidelength of the triangles (approximative!)")
        obj.addProperty("App::PropertyInteger", "DividedBy", "Geodesic",
                        "The sides of the basic polyhedron are divided in ... (value 1 to 10)").DividedBy = div

        obj.Proxy = self

    def geodesic_divide_triangles(self, vertex1, vertex2, vertex3, faces):
        try:

            vector1 = (Base.Vector(vertex2) - Base.Vector(vertex1)) / \
                self.divided_by
            vector2 = (Base.Vector(vertex3) - Base.Vector(vertex2)) / \
                self.divided_by

            icosaPt = {}

            icosaPt[str(1)] = Base.Vector(vertex1)

            for level in range(self.divided_by):
                l1 = level + 1
                icosaPt[str(l1*10+1)] = icosaPt[str(1)] + vector1 * (l1)

                for pt in range(level+1):
                    icosaPt[str(l1*10+2+pt)] = icosaPt[str(l1*10+1)] + \
                        vector2 * (pt+1)

            for level in range(self.divided_by):

                for point in range(level+1):
                    vertex1x = icosaPt[str(level*10+1+point)
                                       ].normalize().multiply(self.radiusvalue)
                    vertex2x = icosaPt[str(level*10+11+point)
                                       ].normalize().multiply(self.radiusvalue)
                    vertex3x = icosaPt[str(level*10+12+point)
                                       ].normalize().multiply(self.radiusvalue)
                    polygon = _part.makePolygon(
                        [vertex1x, vertex2x, vertex3x, vertex1x])
                    faces.append(_part.Face(polygon))

                for point in range(level):
                    vertex1x = icosaPt[str(level*10+1+point)
                                       ].normalize().multiply(self.radiusvalue)
                    vertex2x = icosaPt[str(level*10+2+point)
                                       ].normalize().multiply(self.radiusvalue)
                    vertex3x = icosaPt[str(level*10+12+point)
                                       ].normalize().multiply(self.radiusvalue)
                    polygon = _part.makePolygon(
                        [vertex1x, vertex2x, vertex3x, vertex1x])
                    faces.append(_part.Face(polygon))

            return faces
        except Exception as err:
            App.Console.PrintError("'Icosahedron' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def execute(self, obj):
        try:

            obj.DividedBy = int(round(obj.DividedBy))
            if obj.DividedBy <= 0:
                obj.DividedBy = 1
            if obj.DividedBy > 10:
                obj.DividedBy = 10

            radius = float(obj.Radius)
            if radius != self.radiusvalue or obj.DividedBy != self.divided_by:
                self.divided_by = obj.DividedBy
                obj.Side = geodesic_radius2side(radius, self.divided_by)
                self.radiusvalue = radius
            else:
                self.radiusvalue = geodesic_side2radius(
                    obj.Side, self.divided_by)
                obj.Radius = self.radiusvalue
                radius = self.radiusvalue

            self.divided_by = obj.DividedBy

            z = 4*radius / math.sqrt(10 + 2 * math.sqrt(5))
            anglefaces = 138.189685104
            r = z/12 * math.sqrt(3) * (3 + math.sqrt(5))

            # radius of a pentagram with the same side
            radius2 = z / math.sin(36 * math.pi/180)/2

            # height of radius2 in the sphere
            angle = math.acos(radius2/radius)
            height = radius * math.sin(angle)

            faces = []

            vertex_bottom = (0, 0, -radius)
            vertexes_low = horizontal_regular_polygon_vertexes(
                5, radius2, -height)
            vertexes_high = horizontal_regular_polygon_vertexes(
                5, radius2, height, math.pi/5)
            vertex_top = (0, 0, radius)

            for i in range(5):
                faces = self.geodesic_divide_triangles(
                    vertex_bottom, vertexes_low[i+1], vertexes_low[i], faces)

            for i in range(5):
                faces = self.geodesic_divide_triangles(
                    vertexes_high[i], vertexes_low[i+1], vertexes_low[i], faces)
                faces = self.geodesic_divide_triangles(
                    vertexes_low[i+1], vertexes_high[i+1], vertexes_high[i], faces)

            for i in range(5):
                faces = self.geodesic_divide_triangles(
                    vertex_top, vertexes_high[i], vertexes_high[i+1], faces)

            shell = _part.makeShell(faces)
            solid = _part.makeSolid(shell)
            obj.Shape = solid

        except Exception as err:
            App.Console.PrintError("'geodesic_divide_triangles' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return


class GeodesicSphereCommand:
    def GetResources(self):
        return {'Pixmap': getWorkbenchFolder() + 'Resources/Icons/geodesic_sphere.svg',
                'Accel': "Shift+G",
                'MenuText': "Geodesic sphere",
                'ToolTip': "Generate Geodesic Spheres"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Geodesic sphere")
        Geodesic_sphere(newObj)

        ViewProviderBox(newObj.ViewObject, "Geodesic sphere")
        App.ActiveDocument.recompute()
        v = Gui.ActiveDocument.ActiveView
        faced.PartMover(v, newObj, deleteOnEscape=True)


Gui.addCommand('Geodesic_sphere', GeodesicSphereCommand())
