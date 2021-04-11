# ***************************************************************************
# *                                                                        *
# *   Copyright (c) 2016, 2018                                            *
# *   <microelly2@freecadbuch.de>                                        *
# *                                                                        *
# *  This program is free software; you can redistribute it and/or modify*
# *  it under the terms of the GNU Lesser General Public License (LGPL)    *
# *  as published by the Free Software Foundation; either version 2 of    *
# *  the License, or (at your option) any later version.                    *
# *  for detail see the LICENCE text file.                                *
# *                                                                        *
# *  This program is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# *  GNU Library General Public License for more details.                *
# *                                                                        *
# *  You should have received a copy of the GNU Library General Public    *
# *  License along with this program; if not, write to the Free Software    *
# *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
# *  USA                                                                    *
# *                                                                        *
# ************************************************************************


import os
import sys
sys.path.insert(0, './nurbs/nurbswb')
import configuration
import nurbswb

import re
__title__ = "FreeCAD Nurbs Library"

__vers__ = "V???"


import FreeCAD
import FreeCADGui
import Design456Init
# -

# from workfeature macro
global get_SelectedObjects


def get_SelectedObjects(info=0, printError=True):
    """ Return selected objects as
        Selection = (Number_of_Points, Number_of_Edges, Number_of_Planes,
                    Selected_Points, Selected_Edges, Selected_Planes)
    """
    def storeShapeType(Object, Selected_Points, Selected_Edges, Selected_Planes):
        if Object.ShapeType == "Vertex":
            Selected_Points.append(Object)
            return True
        if Object.ShapeType == "Edge":
            Selected_Edges.append(Object)
            return True
        if Object.ShapeType == "Face":
            Selected_Planes.append(Object)
            return True
        return False

    m_actDoc = App.ActiveDocument

    if m_actDoc.Name:
        # Return a list of SelectionObjects for a given document name.
        # "getSelectionEx" Used for selecting subobjects
        m_selEx = Gui.Selection.getSelectionEx(m_actDoc.Name)

        m_num = len(m_selEx)
        if info != 0:
            print_msg("m_selEx : " + str(m_selEx))
            print_msg("m_num   : " + str(m_num))

        if m_num >= 1:
            Selected_Points = []
            Selected_Edges = []
            Selected_Planes = []
            Selected_Objects = []
            for Sel_i_Object in m_selEx:
                if info != 0:
                    print_msg("Processing : " + str(Sel_i_Object.ObjectName))

                if Sel_i_Object.HasSubObjects:
                    for Object in Sel_i_Object.SubObjects:
                        if info != 0:
                            print_msg("SubObject : " + str(Object))
                        if hasattr(Object, 'ShapeType'):
                            storeShapeType(Object, Selected_Points,
                                           Selected_Edges, Selected_Planes)
                        if hasattr(Object, 'Shape'):
                            Selected_Objects.append(Object)
                else:
                    if info != 0:
                        print_msg("Object : " + str(Sel_i_Object))
                    if hasattr(Sel_i_Object, 'Object'):
                        if hasattr(Sel_i_Object.Object, 'ShapeType'):
                            storeShapeType(
                                Sel_i_Object.Object, Selected_Points, Selected_Edges, Selected_Planes)
                        if hasattr(Sel_i_Object.Object, 'Shape'):
                            if hasattr(Sel_i_Object.Object.Shape, 'ShapeType'):
                                if not storeShapeType(Sel_i_Object.Object.Shape, Selected_Points, Selected_Edges, Selected_Planes):
                                    Selected_Objects.append(
                                        Sel_i_Object.Object)

            Number_of_Points = len(Selected_Points)
            Number_of_Edges = len(Selected_Edges)
            Number_of_Planes = len(Selected_Planes)
            Selection = (Number_of_Points, Number_of_Edges, Number_of_Planes,
                         Selected_Points, Selected_Edges, Selected_Planes, Selected_Objects)
            if info != 0:
                print_msg("Number_of_Points, Number_of_Edges, Number_of_Planes," +
                          "Selected_Points, Selected_Edges, Selected_Planes , Selected_Objects = " + str(Selection))
            return Selection
        else:
            if info != 0:
                print_msg("No Object selected !")
            if printError:
                printError_msg("Select at least one object !")
            return None
    else:
        printError_msg("No active document !")
    return

# ------------------------------


# ---------------------------------------------------------------------------
# define the Commands of the Test Application module
# ---------------------------------------------------------------------------
class MyTestCmd2:
    """Opens a Qt dialog with all inserted unit tests"""

    def Activated(self):
        import QtUnitGui
        TestNurbsGui
        reload(nurbswb.TestNurbsGui)
        TestNurbs
        reload(nurbswb.TestNurbs)
        QtUnitGui.addTest("nurbswb.TestNurbsGui")
        QtUnitGui.addTest("nurbswb.TestNurbs")

    def GetResources(self):
        return {'MenuText': 'Test-test...', 'ToolTip': 'Runs the self-test for the workbench'}


Gui.addCommand('My_Test2', MyTestCmd2())
# FreeCADGui.runCommand('My_Test2')


# ------------------------------------------
# fast command adder template

global _Command2


class _Command2():

    def __init__(self, lib=None, name=None, icon=None, command=None, modul='nurbswb', tooltip='No Tooltip'):

        # print ("!! command 2:",icon,modul,lib,command,tooltip)

        if lib == None:
            lmod = modul
        else:
            lmod = modul + '.' + lib
        if command == None:
            command = lmod + ".run()"
        else:
            command = lmod + "." + command

        self.lmod = lmod
        self.command = command
        self.modul = modul
        if icon != None:
            self.icon = __dir__ + icon
        else:
            self.icon = None

        if name == None:
            name = command
        self.name = name
        self.tooltip = tooltip

    def GetResources(self):
        if self.icon != None:
            return {'Pixmap': self.icon,
                    'MenuText': self.name,
                    'ToolTip': self.tooltip,
                    'CmdType': "ForEdit"  # bleibt aktiv, wenn sketch editor oder andere tasktab an ist
                    }
        else:
            return {
                # 'Pixmap' : self.icon,
                'MenuText': self.name,
                'ToolTip': self.name,
                'CmdType': "ForEdit"  # bleibt aktiv, wenn sketch editor oder andere tasktab an ist
            }

    def IsActive(self):
        if Gui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):

        import re
        ta = True
        if ta:
            App.ActiveDocument.openTransaction(self.name)
        if self.command != '':
            if self.modul != '':
                modul = self.modul
            else:
                modul = self.name
            Gui.doCommand("import " + modul)
            Gui.doCommand("import " + self.lmod)
            Gui.doCommand("reload(" + self.lmod + ")")
            docstring = "print;print (" + \
                re.sub(r'\(.*\)', '.__doc__', self.command)

            Gui.doCommand(docstring)
            Gui.doCommand(self.command)
        if ta:
            App.ActiveDocument.commitTransaction()
        if App.ActiveDocument != None:
            App.ActiveDocument.recompute()


global _Command


class _Command():

    def __init__(self, lib=None, name=None, icon=Design456Init.NURBS_ICON_PATH+'nurbs.svg', command=None, modul='nurbswb'):

        # print ("!! command:",icon,modul,lib,command)
        if lib == None:
            lmod = modul
        else:
            lmod = modul+'.'+lib
        if command == None:
            command = lmod+".run()"
        else:
            command = lmod + "."+command

        self.lmod = lmod
        self.command = command
        self.modul = modul
        try:
            self.icon = __dir__ + icon
        except:
            pass
        if name == None:
            name = command
        self.name = name

    def GetResources(self):
        return {'Pixmap': self.icon,
                'MenuText': self.name,
                'ToolTip': self.name,
                'CmdType': "ForEdit"  # bleibt aktiv, wenn sketch editor oder andere tasktab an ist
                }

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        #App.ActiveDocument.openTransaction("create " + self.name)
        if self.command != '':
            if self.modul != '':
                modul = self.modul
            else:
                modul = self.name
            FreeCADGui.doCommand("import " + modul)
            FreeCADGui.doCommand("import "+self.lmod)
            FreeCADGui.doCommand("reload("+self.lmod+")")
            FreeCADGui.doCommand(self.command)
        # App.ActiveDocument.commitTransaction()
        if App.ActiveDocument is not None:
            App.ActiveDocument.recompute()


class _alwaysActive(_Command):

    def IsActive(self):
        return True

# conditions when a command should be active ..


def always():
    ''' always'''
    return True


def ondocument():
    '''if a document is active'''
    return FreeCADGui.ActiveDocument is not None


def onselection():
    '''if at least one object is selected'''
    return len(FreeCADGui.Selection.getSelection()) > 0


def onselection1():
    '''if exactly one object is selected'''
    return len(FreeCADGui.Selection.getSelection()) == 1


def onselection2():
    '''if exactly two objects are selected'''
    return len(FreeCADGui.Selection.getSelection()) == 2


def onselection3():
    '''if exactly three objects are selected'''
    return len(FreeCADGui.Selection.getSelection()) == 3


def onselex():
    '''if at least one subobject is selected'''
    return len(FreeCADGui.Selection.getSelectionEx()) != 0


def onselex1():
    '''if exactly one subobject is selected'''
    return len(FreeCADGui.Selection.getSelectionEx()) == 1


# the menu entry list
App.tcmds5 = []

# create menu entries
'''
def c1(menu,name,*info):
    global _Command
    name1="Nurbs_"+name
    t=_Command(name,*info)
    FreeCADGui.addCommand(name1,t)
    App.tcmds5.append([menu,name1,name,'always',info])
'''


def c1a(menu, isactive, name, *info):
    global _Command
    name1 = "Nurbs_"+name
    t = _Command(name, *info)
    t.IsActive = isactive
    FreeCADGui.addCommand(name1, t)
    App.tcmds5.append([menu, name1, name, isactive, info])


'''
def c2(menu,title,name,*info):
    #print info
    global _Command
    title1="Nurbs_"+title
    FreeCADGui.addCommand(title1,_Command(name,*info))
    App.tcmds5.append([menu,title1,name,'always',info])
'''


def c2a(menu, isactive, title, name, *info):
    global _Command
    t = _Command(name, *info)
    title1 = "Nurbs_"+title
    t.IsActive = isactive
    FreeCADGui.addCommand(title1, t)
    App.tcmds5.append([menu, title1, name, isactive, info])


def c2b(menu, isactive, title, name, text, icon, cmd=None, *info):

    import re
    global _Command
    if cmd == None:
        cmd = re.sub(r' ', '', text)+'()'
    if name == 0:
        name = re.sub(r' ', '', text)
    t = _Command(name, text, icon, cmd, *info)
    if title == 0:
        title = "TT"+re.sub(r' ', '', text)
    name1 = "Nurbs_"+title
    t.IsActive = isactive
    FreeCADGui.addCommand(name1, t)
    App.tcmds5.append([menu, name1])

# -----------------------------


# the menu entry list
App.tcmdsNurbs = []
# create menu entries


def c3b(menu, isactive, name, text, icon=None, cmd=None, *info):

    import re
    global _Command2
    if cmd == None:
        cmd = re.sub(r' ', '', text) + '()'
    if name == 0:
        name = re.sub(r' ', '', text)
#    if icon==None:
#        pic=re.sub(r' ', '', text)
#        icon=Design456Init.NURBS_ICON_PATH+''+pic+'.svg'

    t = _Command2(name, text, icon, cmd, *info)
    # if title ==0:
    title = re.sub(r' ', '', text)
#    print title
    name1 = "Nurbs_" + title
    t.IsActive = isactive
    Gui.addCommand(name1, t)

    App.tcmdsNurbs.append([menu, name1])
    return name1


def c3bI(menu, isactive, name, text, icon='None', cmd=None, tooltip='', *info):

    import re
    global _Command2
    if cmd == None:
        cmd = re.sub(r' ', '', text) + '()'
    if name == 0:
        name = re.sub(r' ', '', text)
    if icon == 'None':
        pic = re.sub(r' ', '', text)
        icon = Design456Init.NURBS_ICON_PATH+''+pic+'.svg'

    if tooltip == '':
        tooltip = name
    t = _Command2(name, text, icon, cmd, tooltip=tooltip, *info)
    title = re.sub(r' ', '', text)
    name1 = "Nurbs_" + title
    t.IsActive = isactive
    Gui.addCommand(name1, t)
    App.tcmdsNurbs.append([menu, name1])
    return name1


def c3bG(menu, isactive, name, text, icon='None', cmd=None, *info):

    import re
    global _Command2
    if cmd == None:
        cmd = "_" + re.sub(r' ', '', text + 'GUI') + '()'
    if name == 0:
        name = re.sub(r' ', '', text + 'GUI')

    t = _Command2(name, text, icon, cmd, *info)
    # if title ==0:
    title = re.sub(r' ', '', text)
    name1 = "Transportation_" + title
    t.IsActive = isactive
    Gui.addCommand(name1, t)
    App.tcmdsNurbs.append([menu, name1])
    return name1


# special conditions for actions
def onneedle():
    '''open the needle file'''
    dokname = App.ParamGet(
        'User parameter:Plugins/nurbs').GetString("Document", "Needle")
    try:
        App.getDocument(dokname)
        return True
    except:
        return False


def onspread():
    '''there should be a spreadsheet object'''
    try:
        App.ActiveDocument.Spreadsheet
        return True
    except:
        return False


if App.GuiUp:

    beztools = []
    _beztools = []

    current = []
    _current = []

    [c3bI(["Bezier"], always, 'upgradeobjects', 'upgrade Object')]
    [c3bI(["Bezier"], always, 'upgradeobjects', 'dump Object')]
    [c3bI(["Bezier"], always, 'approximator', 'activate Execution')]
    [c3bI(["Bezier"], always, 'approximator', 'deactivate Execution')]
#    [c3bI(["Bezier"], always, 'approximator', 'A')]
#    [c3bI(["Bezier"], always, 'approximator', 'B')]
    beztools += [c3bI(["Bezier", "Assembly"], always, 'morpher',
                      'create Morpher', tooltip='morph two Bezier faces')]
    beztools += [c3bI(["Bezier", "Assembly"], always, 'morpher', 'curve morphed Face',
                      tooltip='create a surface by 4 border curves')]
    [c3bI(["Bezier"], always, 'berings', 'flatten the wire')]

    [c3bI(["Bezier"], always, 'approximator', 'Ribs to Face')]
    [c3bI(["Bezier"], always, 'approximator', 'swap Curves')]
    [c3bI(["Bezier"], always, 'approximator', 'curves to Face')]

    [c3bG(["Bezier"], always, 'approximator', 'create MyMin A')]
    [c3bG(["Bezier"], always, 'approximator', 'create MyMin Soft')]
    [c3bG(["Bezier"], always, 'approximator',
          'create BezierPoles Frame from ribs')]

    beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Tripod',
                      tooltip='create a tripod onto the selected face')]
    beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Tripod Sketch',
                      tooltip='create a tripod with a sketch onto the selected face')]
    beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Sweep',
                      tooltip='create a Sweep of the selected ribs')]
    beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Loft',
                      tooltip='create a Loft of the selected ribs')]
    beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Compound',
                      tooltip='create a compound of the selection')]
    [c3bG(["Points"], always, 'approximator', 'load Pointcloud from Image')]
    [c3bG(["Points"], always, 'approximator', 'load Cylinderface from Image')]
    beztools += [c3bG(["Points"], always, 'approximator',
                      'Bump Face from Image', icon=None)]

    [c3bG(["Points"], always, 'approximator', 'smooth Pointcloud')]
    [c3bI(["Bezier"], always, 'berings', 'create Sketch Circle')]

    beztools += [c3bI(["Bezier", "Create"], always,
                      'berings', 'create BePlane')]
    beztools += [c3bI(["Bezier", "Create"], always,
                      'berings', 'create BeTube')]
    beztools += [c3bI(["Bezier", "Create"], always,
                      'berings', 'create Helmet')]

    c3b(["Bezier", "Create"], always, 'berings', 'create Datum Plane')
    c3b(["Bezier", "Create"], always, 'berings', 'create Datum Line')

    c3bI(["Bezier", "Assembly"], always, 'berings', 'create Triangle')
    c3bI(["Bezier", "Assembly"], always,
         'berings', 'create Plane Tube Connector')
    c3bI(["Bezier", "Assembly"], always,
         'berings', 'create Helmet Tube Connector')

    beztools += [c3bI(["Bezier", "Assembly"], always,
                      'berings', 'create Bering')]
    c3bG(["Bezier", "Assembly"], always, 'berings',
         'create Tangent Helpers', Design456Init.NURBS_ICON_PATH + "alpha.svg")
    beztools += [c3bI(["Bezier", "Assembly"], always,
                      'berings', 'create Beface')]
#    c3bG(["Bezier"], always, 'parameters', 'run')
    c3bI(["Bezier", "Assembly"], always, 'berings', 'create Product')
    c3bI(["Bezier", "Assembly"], always, 'berings', 'connect Faces')
    c3bI(["Bezier", "Assembly"], always, 'berings', 'create Seam')
    c3bG(["Bezier", "Assembly"], always, 'berings', 'create Gordon')

    c3b(["Bezier", "Convert"], always, 'berings', 'BSpline To Bezier Curve')
    c3b(["Bezier", "Convert"], always, 'berings', 'BSpline To Bezier Surface')
    c3b(["Bezier", "Convert"], always, 'berings', 'Face To Bezier Surface')
    c3bG(["Bezier", "Convert"], always, 'berings', 'create Approx',
         Design456Init.NURBS_ICON_PATH + "alpha.svg")

    current += [c3bI(["Bezier"], always, 'points_to_wires',
                     'AA', tooltip="Eine Testfunktion")]

    current += [c3bI(["Bezier"], always, 'points_to_face',
                     'Reconstruct Sphere', tooltip="Subselection to Sphere", icon=None)]
    current += [c3bI(["Bezier"], always, 'points_to_face',
                     'Reconstruct Cylinder', tooltip="Subselection to Cylinder", icon=None)]
    current += [c3bI(["Bezier"], always, 'points_to_face',
                     'optimize Cylinder', icon=None)]

    current += [c3bI(["Bezier"], always, 'points_to_face',
                     'Reconstruct Plane', tooltip="Subselection to Plane", icon=None)]
    current += [c3bI(["Bezier"], onselection1, 'points_to_face',
                     'noisy mesh', tooltip="add noise to a mesh", icon=None)]

    current += [c3bI(["Bezier"], onselection, 'merge_faces',
                     'merge 2 Faces', icon=None)]
    current += [c3bI(["Bezier"], onselection, 'merge_faces',
                     'merge 2 Faces B', icon=None)]

    current += [c3bI(["Bezier"], always, 'minimumsurface',
                     'test minimal surface', icon=None)]

#    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'create Array',icon=None)]
#    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'split Edges',icon=None)]
    current += [c3bI(["Pattern"], onselection, 'pattern_v2',
                     'remove Edges', icon=None)]
#    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'create Single Pattern',icon=None)]
#    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'create Pattern',icon=None)]
    current += [c3bI(["Pattern"], onselection,
                     'pattern_v2', 'pattern V3', icon=None)]
    current += [c3bI(["Pattern"], always, 'pattern_v2',
                     'pattern all tests', icon=None)]


#    beztools += [c3bI(["Points"], always, 'points_to_face', 'Points to Cone',tooltip="P1,N1,P2,P3,P4",icon=None)]
    beztools += [c3bI(["Bezier"], always, 'geodesic2', 'BB',
                      tooltip="Eine andere Testfunktion")]
#    beztools += [c3bI(["Points"], always, 'points_to_face', 'Points to Cone',tooltip="P1,N1,P2,P3,P4",icon=None)]
    _beztools += [c3bI(["Points"], always, 'points_to_face',
                       'Points to Cone PN P P P', tooltip="P1,N1,P2,P3,P4", icon=None)]
    _beztools += [c3bI(["Points"], always, 'points_to_face',
                       'Points to Cone PN PN ', tooltip="P1,N1,P2,N2", icon=None)]

    _beztools += [c3bI(["Points"], always, 'points_to_face',
                       'Points to Cylinder PN P P', tooltip="P1,N1,P2,P3", icon=None)]

    beztools += [c3bI(["Points"], always, 'points_to_face',
                      'Points to Cylinder 5P', tooltip="P1,P2,P3,p4,p%", icon=None)]
    _beztools += [c3bI(["Points"], always, 'points_to_face',
                       'Points to Sphere 4P', tooltip="P1,P2,P3,p4", icon=None)]
    _beztools += [c3bI(["Points"], always, 'points_to_face',
                       'Points to Sphere PN P', tooltip="P1,N1,P2", icon=None)]

    _beztools += [c3bI(["Points"], always, 'perspective_trafos', 'createPerspectiveTrafo',
                       tooltip="perspektiische Tranformation 3D einer Flaeche", icon=None)]

    _beztools += [c3bI(["Points"], always, 'concave_hull', 'create concave hull 2D',
                       tooltip="alpha shape fuer eine point cloud", icon=None)]

    beztools += [c3bI(["Curves", "Geodesic"], always, 'geodesic2', 'create a Path',
                      tooltip="create a connection between two points of a Face", icon=None)]
    beztools += [c3bI(["Curves", "Geodesic"], always, 'geodesic2', 'optimize Path',
                      tooltip="apporximate geodesic curve between two points starting form a given path", icon=None)]

    c3bI(["Bezier"], always, 'berings', 'add Knot')
    [c3bI(["Bezier"], always, 'multiedit', 'multiEdit')]

#    old version Surface Editor
#    c3b(["Bezier"], always, 'berings', 'Surface Editor')

    c3bI(["Bezier"], always, 'berings', 'create Be Grid')

    c3bI(["Bezier", "Segments"], always, 'berings', 'Split Into Cells')
    c3bI(["Bezier", "Segments"], always, 'berings', 'create Cell')
    c3bI(["Bezier", "Segments"], always, 'berings', 'create Hole')
    c3bG(["Bezier", "Segments"], always, 'berings', 'create Border',
         Design456Init.NURBS_ICON_PATH + "alpha.svg")

    c3bI(["Bezier", "Convert"], always, 'berings', 'create QuadPlacement',
         Design456Init.NURBS_ICON_PATH + "alpha.svg")
    c3bI(["Bezier", "Convert"], always, 'berings', 'stretch and bend')
    c3bG(["Bezier", "Convert"], always, 'berings', 'polish G1',
         Design456Init.NURBS_ICON_PATH + "alpha.svg")

    c3bI(["Bezier", "Diagnostics"], ondocument, 'monitor', 'create a force monitor',
         Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runforce()")

    c3bI(["Bezier", "Specials"], always, 'berings', 'fix Corner')
    c3bI(["Bezier", "Specials"], always, 'berings', 'create Tangent Stripes')

    [c3bG(["Bezier", "Specials"], always, 'approximator', 'minimum Length Bezier')]
    [c3bG(["Bezier", "Specials"], always, 'approximator',
          'near constant Curvature Bezier')]

    [c3bI(["Bezier", "Specials"], always, 'leastsq', 'leastsq Bezier')]
    [c3bI(["Bezier", "Specials"], always, 'leastsq', 'leastsq Bezier Two Segments')]

    c3bI(["Bezier", "Specials"], always, 'berings', 'glaetten')
    c3bI(["Bezier", "Specials"], always, 'berings', 'solid')
    c3bI(["Bezier", "Specials"], always,
         'approximation', 'create Approximation')
    c3bI(["Bezier", "Specials"], always,
         'approximation', 'create Poles for Test')


# -------------------------------------------
    mt = "Transportation V0"
    c2a([mt], ondocument, 'LoadSketch', 'sketchmanager', 'load sketch from a sketchlib',
        Design456Init.NURBS_ICON_PATH+'sketchlibload.svg', "runLoadSketch()")
    c2a([mt], onselection2, 'Status155', 'feedbacksketch', 'connect road to line ',
        Design456Init.NURBS_ICON_PATH + "alpha.svg", "connectLine()", "sketcher")
    c2b([mt], ondocument, 0, 'sketch_to_bezier', 'create Arc Sketch',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b([mt], onselection1, 0, 'sketch_to_bezier',
        'create Labels', Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b([mt], onselection1, 0, 'sketch_to_bezier',
        'create Stations', Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b([mt], ondocument, 0, 'sketch_to_bezier', 'create LatLonMarker',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b([mt], onselection, 0, 'sketch_to_bezier',
        'update Labels', Design456Init.NURBS_ICON_PATH+'draw.svg')

# -------------------------------------------

    c2b(["SMOOTH"], onselection1, 0, 'smooth', 'smooth Wire',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["SMOOTH"], onselection1, 0, 'smooth', 'smooth Mesh',
        Design456Init.NURBS_ICON_PATH+'draw.svg')

    c2b(["SMOOTH"], onselection1, 0, 'smooth', 'split Mesh',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["SMOOTH"], onselection2, 0, 'smooth', 'slice Mesh by Sketch',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["SMOOTH"], onselection2, 0, 'smooth', 'distance Curves',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["SMOOTH"], onselection2, 0, 'smooth', 'draw Path',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["Sketchertools"], ondocument, 0, 'sketch_to_bezier',
        'create Bezier Sketch', Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["Sketchertools"], ondocument, 0, 'sketch_to_bezier',
        'create Arc Sketch', Design456Init.NURBS_ICON_PATH+'draw.svg')

    c2b(["Sketchertools"], onselection1, 0, 'sketch_to_bezier',
        'create Labels', Design456Init.NURBS_ICON_PATH+'draw.svg')

    c2b(["Sketchertools"], onselection, 0, 'sketch_to_bezier',
        'update Labels', Design456Init.NURBS_ICON_PATH+'draw.svg')

    # geodesics
    c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',
        'create Curvature Star', Design456Init.NURBS_ICON_PATH+'draw.svg')
    c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',
        'create Geodesic', Design456Init.NURBS_ICON_PATH+'geodesic.svg')
    c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',
        'geodesic Distance', Design456Init.NURBS_ICON_PATH+'geodesiccircle.svg')
    c2b(["Curves", "Geodesic"], onselection2, 0, 'geodesic_lines',
        'geodesic Map Patch To Face', Design456Init.NURBS_ICON_PATH+'patch.svg')
    c2b(["Curves", "Geodesic"], ondocument, 0, 'geodesic_lines',
        'create Marker', Design456Init.NURBS_ICON_PATH+'geodesic_ref.svg')
    c2b(["Curves", "Geodesic"], onselection2, 0, 'geodesic_lines',
        'find Geodesic To Target', Design456Init.NURBS_ICON_PATH+'geodesic_target.svg')
    c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',
        'append Geodesic', Design456Init.NURBS_ICON_PATH+'geodesic_append.svg')
    c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',
        'create geodesic bunch', Design456Init.NURBS_ICON_PATH+'geodesic_bunch.svg')

    # shoe
    c2b(["Shoe", "Markers"], always, 0, 'geodesic_lines',
        'create Shoe Markers', Design456Init.NURBS_ICON_PATH+'geodesic_ref.svg')
    c2b(["Shoe", "Markers"], always, 0, 'geodesic_lines', 'connect Markers',
        Design456Init.NURBS_ICON_PATH+'geodesic_target.svg')

    c1a(["Curves"], always, "scancut", "cut Scanned Mesh ",
        Design456Init.NURBS_ICON_PATH+'mesh_cut.svg')
    c1a(["Curves"], ondocument, "weighteditor", "Weight Editor")

    c1a(["Curves"], ondocument, "simplecurve", "simplify curve")
    c1a(["Curves"], onselection1, "removeknot", "remove a knot in a bspline")
    c1a(["Curves"], onselection2, "curvedistance",
        "calculate the distance between two curves")
    c1a(["Curves"], always, "createsketchspline", "create Sketcher BSpline from a curve",
        Design456Init.NURBS_ICON_PATH+'createsketchspline.svg')
    c1a(["Curves"], ondocument, "weighteditor", "Weight Editor")
    #c2a(["Curves"],onselection1,'DraftBSpline Editor',"DraftBSplineEditor","Edit Draft Bspline",Design456Init.NURBS_ICON_PATH+'32px-draftbspline_edit.png',"run()")
    c2a(["Curves"], always, 'DraftBSpline Editor', "DraftBSplineEditor", "Edit Draft Bspline",
        Design456Init.NURBS_ICON_PATH+'32px-draftbspline_edit.png', "run()")

    c2a(["Curves"], always, 'facedraw', 'facedraw', 'draw on a face',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "run()")
#    c2a(["Curves"],always,'facedraws','facedraw_segments','draw over segments',Design456Init.NURBS_ICON_PATH+'draw.svg',"run()")
    c2a(["Curves"], always, 'facedrawa', 'facedraw', 'create Map of a face',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "createMap()")
    c2a(["Curves"], always, 'facedrawa2', 'facedraw', 'create Curvature Map of a face',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "createMap(mode='curvature')")
    c2a(["Curves"], always, 'curvaturea', 'curvatureplot',
        'draw the curvature net', Design456Init.NURBS_ICON_PATH+'draw.svg', "run()")

    c2a(["Curves"], always, 'facedrawb', 'facedraw', 'create Grids for a face',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "createGrid()")

    c2a(["Curves"], always, 'isodraw32', 'isodraw', '3D to 2D',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "map3Dto2D()")
    c2a(["Curves"], always, 'isodraw23', 'isodraw', '2D to 3D',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "map2Dto3D()")
    c2a(["Curves"], always, 'isodraw24', 'isodraw', '3D Grid to 2D Grid',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "map3Dgridto2Dgrid()")

    c2b(["Curves"], always, 0, 'isodraw', 'create Brezel',
        Design456Init.NURBS_ICON_PATH+'draw.svg')
#    c2a(["Curves"],always,'importColorSVG','shoe_importSVG','import SVG for shoes',Design456Init.NURBS_ICON_PATH+'draw.svg',"import_test()")

    c2a(["Curves"], always, 'holes', 'holes', 'Play with holes on a surface',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "run()")
    c2a(["Curves"], always, 'holeswires', 'holes', 'extract the wires of the selected part',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "extractWires()")

    c2a(["Curves"], always, 'linkSVG', 'shoe_importSVG', 'create link to SVG file',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "create_svglink()")

    c2a(["Curves"], always, 'impSVG', 'shoe_importSVG', 'import svg file',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "import_svg()")
    c2a(["Curves"], always, 'expSVG', 'shoe_importSVG', 'export svg file',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "export_svg()")

    c2a(["Curves"], always, 'cnotrol', 'controlpanel', 'create a controlpanel',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "run()")

    c2a(["Curves"], always, 'beziera', 'bezier', 'selected face to sketch',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "faceToSketch()")
    c2a(["Curves"], always, 'bezierb', 'bezier', 'selected edges to sketches',
        Design456Init.NURBS_ICON_PATH+'draw.svg', "subsToSketch()")

    c2a(["Curves"], always, 'transform_spline', 'transform_spline',
        'perspective transformation of a Bbspline', Design456Init.NURBS_ICON_PATH+'upgrade.svg', "run()")
    c2a(["Curves"], ondocument, 'createcloverleaf', 'createcloverleaf',
        'create a cloverleaf', Design456Init.NURBS_ICON_PATH+'cloverleaf.svg', "run()")
    c2a(["Curves"], ondocument, 'createshoerib', 'createshoerib',
        'create a shoe last rib', Design456Init.NURBS_ICON_PATH+'cloverleaf.svg', "run()")

    c2a(["Curves"], ondocument, 'project_edge2face1', 'project_edge2face',
        'parallel projection of edge to face', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Curves"], ondocument, 'project_edge2face2', 'project_edge2face',
        'parallel projection of selection to face', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runAll()")
    c2a(["Curves"], ondocument, 'project_edge2face3', 'project_edge2face',
        'concatenate Draft.BSplines', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "concatenateBSplines()")

    c2a(["Curves"], onselection1, 'project_edge2face4', 'project_edge2face',
        'split curve in xy, sz', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "splitCurve()")
    c2a(["Curves"], onselection2, 'project_edge2face5', 'project_edge2face',
        'combine sz,xy, to 3dCurve', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "combineCurve()")

    c2a(["Curves"], ondocument, 'loft_selection', 'loft_selection',
        'loft between two selections', Design456Init.NURBS_ICON_PATH+'Loft.svg', "run()")
    c2a(["Curves"], ondocument, 'loft_selectionEdges', 'loft_selection',
        'loft between two selected edges', Design456Init.NURBS_ICON_PATH+'Loft.svg', "runOnEdges()")

    c2a(["Curves"], ondocument, 'knotsandpoles', 'knotsandpoles',
        'display knots and poles for selected curves', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Curves"], ondocument, 'monitor', 'monitor', 'create a monitor for a curve length',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Curves"], ondocument, 'param_bspline', 'param_bspline',
        'create a parametric bspline with tangents', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Curves"], ondocument, 'OffsetSpline', 'curves', 'create a Sketch for a OffsetSpline',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runOffsetSpline()")
    c2a(["Curves"], ondocument, 'Stare', 'curves', 'create a Sketch for a Star',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runStar()")
    c2a(["Curves"], ondocument, 'DynamicOffset', 'dynamicoffset',
        'create a dynamic Offset', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Curves"], ondocument, 'FloatList', 'datatools', 'create a floatlist',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runFloatlist()")
    c2a(["Curves"], ondocument, 'Sole', 'create_sole_sketch',
        'create a sole as offsetspline', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runSole()")
    c2a(["Curves"], onselection2, 'MoveAlongCurve', 'move_along_curve',
        'move an object #2 along a bspline curve #1', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Curves"], ondocument, 'SketchClone', 'sketchclone', 'create a semi clone of a sketch',
        Design456Init.NURBS_ICON_PATH+'sketchdriver.svg', "runSketchClone()")

    c2a(["Faces", "create"], always, 'Random Plane', "nurbs", "Create plane with randoms",
        Design456Init.NURBS_ICON_PATH+'plane.svg', "testRandomB()")
    c2a(["Faces", "create"], always, 'Random Torus', "nurbs", "Create torus with randoms",
        Design456Init.NURBS_ICON_PATH+'torus.svg', "testRandomTorus()")
    c2a(["Faces", "create"], always, 'Random Cylinder', "nurbs", "Create cylinder with randomness",
        Design456Init.NURBS_ICON_PATH+'cylinder.svg', "testRandomCylinder()")
    c2a(["Faces", "create"], always, 'Random Sphere', "nurbs", "Create sphere with randomness",
        Design456Init.NURBS_ICON_PATH+'sphere.svg', "testRandomSphere()")
    c2a(["Faces", "create"], ondocument, 'simple Hood', 'simplehood',
        'create a simple hood', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Faces", "create"], ondocument, 'grid test data', 'mesh_generator',
        'create a grid testset', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "gentest()")

    c2a(["Faces", "create"], ondocument, 'helm', 'helmlet', 'create a helmlet',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "createHelmlet()")

    c2a(["AAA"], onselection1, 'corridor2a', 'corridor', 'wire to bspline',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "WireToBSpline()")

    c2a(["Faces", "create"], onselection2, 'corridor', 'corridor',
        'create a corridor for a path on s face testset', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")

    c2a(["Faces"], ondocument, 'sculpt', 'sculpter', 'sculpt a face (MyGrid)',
        Design456Init.NURBS_ICON_PATH+'beta.svg', "run()")

    c2a(["Faces"], ondocument, 'patcha', 'patch', 'connect 2 curve segments to a face',
        Design456Init.NURBS_ICON_PATH+'beta.svg', "run()")
    c2a(["Faces"], ondocument, 'patchb', 'patch', 'patch b',
        Design456Init.NURBS_ICON_PATH+'alpha.svg', "runb()")
    c2a(["Faces"], ondocument, 'folda', 'folding', 'create a folding of a face',
        Design456Init.NURBS_ICON_PATH+'testit.svg', "run()")

    c2a(["Faces"], ondocument, 'unrolla', 'unroll_curve', 'unroll curve Yaw from a face',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "unroll_yaw()")
    c2a(["Faces"], ondocument, 'unrollb', 'unroll_curve', 'unroll curve Pitch from a face',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "unroll_pitch()")

    c2a(["Faces"], ondocument, 'unrollc', 'unroll_curve', 'combine Yaw and Pitch curces',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "combineCT()")

    c2a(["Shoe"], ondocument, 'Sole Change Model', 'sole_change_model',
        'Shoe Sole Change Model', Design456Init.NURBS_ICON_PATH+'solechange.svg', "run()")
    c2a(["Faces"], ondocument, 'load Sole Height', 'load_sole_profile_height',
        'Load Height Profile', Design456Init.NURBS_ICON_PATH+'sole.svg', "run()")
    c2a(["Faces"], ondocument, 'load Sole Widht', 'load_sole_profile_width',
        'Load Width Profile', Design456Init.NURBS_ICON_PATH+'sole.svg', "run()")

    c2a(["Faces"], ondocument, 'Iso Map', 'isomap', 'draw isomap of Face',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")

    c2a(["Faces", "create"], always, 'Nurbs Editor', 'nurbs',
        'creates a test nurbs', Design456Init.NURBS_ICON_PATH+'zebra.svg', "runtest()")
    c2a(["Faces", "create"], onselection, 'UV Grid Generator', 'uvgrid_generator',
        'create UV grid of the partr', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runSel()")
    c2a(["Faces", "create"], onselection, 'Nurbs Helper', 'helper',
        'create helper objects of the part', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "makeHelperSel()")
    c2a(["Faces", "create"], ondocument, 'Create QR Code', 'createbitmap',
        'create a qr code surface', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")

    c2a(["Faces"], always, 'filledface', 'filledface', 'createFilledFace',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "createFilledFace()")

    c2a(["Faces"], always, 'ZebraTool', 'zebratool', 'ZebraTool',
        Design456Init.NURBS_ICON_PATH+'zebra.svg', "run()")
    c2a(["Faces"], always, 'Curves to Face', 'curves2face',
        'Curves to Face', Design456Init.NURBS_ICON_PATH+'upgrade.svg', "run()")
    c2a(["Faces"], always, 'Segment', 'segment', 'Cut a segment of a Face',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runsegment()")
    c2a(["Faces"], always, 'FineSegment', 'segment', 'Cut a fine segment of a Face',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runfinesegment()")
    c2a(["Faces"], always, 'NurbsTrafo', 'segment', 'Transform a Face',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runnurbstrafo()")
    c2a(["Faces"], always, 'Tangent', 'tangentsurface', 'create a tangent Face',
        Design456Init.NURBS_ICON_PATH+'tangentsurface.svg', "runtangentsurface()")
    c2a(["Faces"], always, 'Seam', 'tangentsurface', 'create a Seam',
        Design456Init.NURBS_ICON_PATH+'createSeam.svg', "runseam()")
    c2a(["Faces"], always, 'Grid generator', 'uvgrid_generator',
        'create a uv-grid for a Face', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")

    c2a(["Topology"], always, 'Topological Analyse', 'analyse_topology_v2',
        'topological analysis', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Topology"], always, 'Topological Compare', 'analyse_topology_v2',
        'topological compare', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "runCompare()")
    c2a(["Topology"], always, 'Topo8', 'analyse_topology_v2', 'display Quality Points',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "displayQualityPoints()")
    c2a(["Topology"], always, 'Topo5', 'analyse_topology_v2', 'print Graph Data',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "printData()")

    c2a(["Topology"], always, 'Topo4', 'analyse_topology_v2', 'add to Vertex Store',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "addToVertexStore()")
    c2a(["Topology"], always, 'Topo2', 'analyse_topology_v2', 'print Vertex Store Dump',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "printVertexStore()")
    c2a(["Topology"], always, 'Topo2a', 'analyse_topology_v2', 'display Vertex Store Common Points',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "displayVertexStore()")

    c2a(["Topology"], always, 'Topo3', 'analyse_topology_v2', 'reset Vertex Store',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "resetVertexStore()")

    c2a(["Topology"], always, 'Topo6', 'analyse_topology_v2', 'load Test 1',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "loadTest1()")
    c2a(["Topology"], always, 'Topo7', 'analyse_topology_v2', 'load Test 2',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "loadTest2()")
    c2a(["Topology"], always, 'Topo10', 'fem_edgelength_mesh',
        'Grid Tension Simulation', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run()")
    c2a(["Topology"], always, 'Topo9', 'analyse_topology_v2',
        'Identify Vertexes in a Shape', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "Test4()")

    c2a(["Topology"], always, 'Topo11', 'fem_edgelength_mesh',
        'Grid Tension Animation', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "run(False)")
    c2a(["Topology"], always, 'Topo12', 'analyse_topology_v2',
        'Test 4', Design456Init.NURBS_ICON_PATH+'nurbs.svg', "Test4()")

    c2a(["Workspace"], ondocument, 'CreateWorkspace', None, "Create workspace",
        Design456Init.NURBS_ICON_PATH+'workspace.svg', "createws()", "workspace")
    c2a(["Workspace"], ondocument, 'CreateWSLink', None, "Create workspace link",
        Design456Init.NURBS_ICON_PATH+'workspacelink.svg', "createlink()", "workspace")

    c2a(["Workspace"], ondocument, 'ViewsQV', 'views', "Create QuadView",
        Design456Init.NURBS_ICON_PATH+'workspacequad.svg', "createquadview()", "workspace")
    c2a(["Workspace"], ondocument, 'Views2H', 'views', "Create 2 horizontal views",
        Design456Init.NURBS_ICON_PATH+'workspace2h.svg', "createh2()", "workspace")

    c2a(["Workspace"], ondocument, 'DarkRoom', 'views', "Create Dark Room",
        Design456Init.NURBS_ICON_PATH+'darkroom.svg', "createdarkroom()", "workspace")
    c2a(["Workspace"], ondocument, 'Light', 'views', "Create Light",
        Design456Init.NURBS_ICON_PATH+'light.svg', "createlight()", "workspace")
    c2a(["Workspace"], ondocument, 'LightOn', 'views', "Light on",
        Design456Init.NURBS_ICON_PATH+'light_on.svg', "lightOn()", "workspace")
    c2a(["Workspace"], ondocument, 'LightOff', 'views', "Light off",
        Design456Init.NURBS_ICON_PATH+'light_off.svg', "lightOff()", "workspace")

    c2a(["Needle"], ondocument, 'Needle', 'needle', 'create a needle',
        Design456Init.NURBS_ICON_PATH+'shoe.svg', "run()")
    c2a(["Needle"], onneedle, 'needle Change Model', 'needle_change_model',
        'needle Change Model', Design456Init.NURBS_ICON_PATH+'shoe.svg', "run()")
    c2a(["Needle"], onselex1, 'addULine', 'needle_cmds', 'add Meridian/Rib',
        Design456Init.NURBS_ICON_PATH+'add_edge.svg', "cmdAdd()")
    c2a(["Needle"], onselex1, 'deleteULine', 'needle_cmds', 'delete Meridian/Rib',
        Design456Init.NURBS_ICON_PATH+'delete_edge.svg', "cmdDel()")
    c2a(["Needle"], onspread, 'Open Spreadsheet', 'wheel_event', 'Open Spreadsheet',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "undock('Spreadsheet')")
    c2a(["Needle"], onneedle, 'Edit Rib', 'wheel_event', 'Edit Rib',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "start('Rib_template')")
    c2a(["Needle"], onneedle, 'Edit Backbone', 'wheel_event', 'Edit Backbone',
        Design456Init.NURBS_ICON_PATH+'nurbs.svg', "start('Backbone')")

    c2a(["Shoe"], always, 'Create Shoe', 'shoe', 'Create Shoe',
        Design456Init.NURBS_ICON_PATH+'shoe.svg', "run()")
    c2a(["Shoe"], always, 'scanbackbonecut', 'scanbackbonecut',
        'Cut the Scan along backbone ', Design456Init.NURBS_ICON_PATH+'backbonecut.svg', "run()")
    c2a(["Shoe"], always, 'Create Sole', 'sole', 'Create Shoe Sole',
        Design456Init.NURBS_ICON_PATH+'sole.svg', "run()")

    c2a(["Shoe"], ondocument, 'toggleSketch', 'shoe_tools', 'toggle constraints of a rib',
        Design456Init.NURBS_ICON_PATH+'toggleshoesketch.svg', "toggleShoeSketch()")
    c2a(["Shoe"], always, 'Generate Docu', "gendok", "generate menu structure docu for web",
        Design456Init.NURBS_ICON_PATH+'plane.svg', "run()")

    c2a(["Shoe"], always, 'DriverSketch', 'skdriver', 'driver test for shoe rib',
        Design456Init.NURBS_ICON_PATH+'toggleshoesketch.svg', "runribtest()")
    c2a(["Shoe"], always, 'DriverSketchAll', 'skdriver', 'driver for all ribs',
        Design456Init.NURBS_ICON_PATH+'toggleshoesketch.svg', "runribtest2()")

    c2a(["Shoe"], always, 'RecomputeAll', 'skdriver', 'recompute shoe',
        Design456Init.NURBS_ICON_PATH+'toggleshoesketch.svg', "recomputeAll()")

    c2a(["Shoe"], always, 'LoadSketch', 'sketchmanager', 'load sketch from a sketchlib',
        Design456Init.NURBS_ICON_PATH+'sketchlibload.svg', "runLoadSketch()")
    c2a(["Shoe"], always, 'SaveSketch', 'sketchmanager', 'save sketch into the sketchlib',
        Design456Init.NURBS_ICON_PATH+'sketchlibsave.svg', "runSaveSketch()")
    c2a(["Shoe"], always, 'DisplaySketchlib', 'sketchmanager', 'list all sketches of the sketchlib',
        Design456Init.NURBS_ICON_PATH+'sketchlib.svg', "runSketchLib()")

    c2a(["Nurbs"], always, 'Grid', 'blender_grid', 'Create Grid',
        Design456Init.NURBS_ICON_PATH + "Draft_Grid.svg", "run()")

    c2a(["Points"], always, 'pta', 'points', 'points to volums',
        Design456Init.NURBS_ICON_PATH + "points.svg", "runA()",)
    c2a(["Points"], always, 'ptb', 'points', 'test B',
        Design456Init.NURBS_ICON_PATH + "points.svg", "runB()",)
    c2a(["Points"], always, 'ptc', 'points', 'create point cloud y = 0.5*x with noise',
        Design456Init.NURBS_ICON_PATH + "points.svg", "runC()",)
    c2a(["Points"], always, 'ptd', 'points', 'approx points with outliner detection',
        Design456Init.NURBS_ICON_PATH + "points.svg", "runD()",)
    c2a(["Points"], always, 'pte', 'points', 'approx point simple',
        Design456Init.NURBS_ICON_PATH + "points.svg", "runE()",)

    c2a(["Neo4j"], always, 'Start', 'neodb', 'start db',
        Design456Init.NURBS_ICON_PATH + "neo4j.png", "start()", "graphdb")
    c2a(["Neo4j"], always, 'Stop', 'neodb', 'stop db',
        Design456Init.NURBS_ICON_PATH + "neo4j_stop.png", "stop()", "graphdb")
    c2a(["Neo4j"], always, 'Status', 'neodb', 'status db',
        Design456Init.NURBS_ICON_PATH + "neo4j_status.png", "status()", "graphdb")

    c2a(["Neo4j"], always, 'Start_OF', 'openflights', 'import_Open Flights',
        Design456Init.NURBS_ICON_PATH + "openflights-import.png", "load()", "graphdb")
    c2a(["Neo4j"], always, 'Reset_OG', 'openflights', 'reset_Open Flights',
        Design456Init.NURBS_ICON_PATH + "openflights.png", "reset()", "graphdb")

    c2a(["Sketchertools"], always, 'Status1', 'feedbacksketch', 'fb sketch',
        Design456Init.NURBS_ICON_PATH + "alpha.svg", "run_test_two_clients()", "sketcher")
    c2a(["Sketchertools"], always, 'Status2', 'feedbacksketch', 'revers order of constraints A',
        Design456Init.NURBS_ICON_PATH + "alpha.svg", "run_test_reverse_Constraints()", "sketcher")
    c2a(["Sketchertools"], always, 'Status3', 'feedbacksketch', 'create Example B',
        Design456Init.NURBS_ICON_PATH + "alpha.svg", "runB()", "sketcher")
    c2a(["Sketchertools"], always, 'Status4', 'feedbacksketch', 'Copy 1.Sketch into 2nd Sketch',
        Design456Init.NURBS_ICON_PATH + "sketchcopy.svg", "run_copySketch()", "sketcher")
    c2a(["Sketchertools"], always, 'Status51', 'feedbacksketch', 'Create FeedBack with 1 client',
        Design456Init.NURBS_ICON_PATH + "feedback-1.svg", "run_createFBS_with_one_Client()", "sketcher")
    c2a(["Sketchertools"], always, 'Status52', 'feedbacksketch', 'Create FeedBack with 2 clients',
        Design456Init.NURBS_ICON_PATH + "feedback-2.svg", "run_createFBS_with_two_Clients()", "sketcher")
    c2a(["Sketchertools"], always, 'Status53', 'feedbacksketch', 'Create FeedBack with 3 clients',
        Design456Init.NURBS_ICON_PATH + "feedback-3.svg", "run_createFBS_with_three_Clients()", "sketcher")

    c2a(["Sketchertools"], always, 'Status56', 'sketcher_grids', 'Create Sketcher Grid',
        Design456Init.NURBS_ICON_PATH + "sketchgrid.svg", "createGridSketch()", "sketcher")


# hier ist ein fehler
#    c2a(["Sketchertools"],always,'Status155','feedbacksketch','connect road to line ',Design456Init.NURBS_ICON_PATH + "alpha.svg","connectLine()","sketcher")


#    for cmd in FreeCADGui.listCommands():
#        if cmd.startswith("Nurbs_"):
#            print cmd

    toolbars = [
        ['Bezier Tools', beztools],
        ['My current Work', current]
    ]


'''

nd=App.newDocument("Unnamed")
App.setActiveDocument(nd.Name)
App.ActiveDocument=App.getDocument(nd.Name)
Gui.ActiveDocument=Gui.getDocument(nd.Name)
'''


class NurbsWorkbench(Workbench):
    '''Nurbs'''

    MenuText = "Nurbs"
    ToolTip = "Nurbs Editor"

    Icon = '''
/* XPM */
static char * nurbs_xpm[] = {
"16 16 2 1",
".    c #E12DEC",
"+    c #FFFFFF",
"................",
"................",
"................",
"................",
".........+++++..",
".........+++++..",
".........+++++..",
".........+++++..",
".........+++++..",
".........+++++..",
"................",
"................",
"................",
"................",
"................",
"................"};'''


"""
    def GetClassName(self):
        return "Gui::PythonWorkbench"


    def __init__(self, toolbars, version):

        self.toolbars = toolbars
        self.version = version

"""
"""
    def Initialize(self):

        Gui.activateWorkbench("DraftWorkbench")
        Gui.activateWorkbench("SketcherWorkbench")

        try: # some methods from curve wb
            import ZebraTool
            import ParametricComb
            import GeomInfo
        except: pass

        cmds= ['ZebraTool','ParametricComb','GeomInfo','Nurbs_DraftBSpline Editor',
        'Nurbs_Create Shoe','Nurbs_Create Sole','Nurbs_Sole Change Model',
        'Nurbs_scanbackbonecut','Nurbs_createsketchspline','Nurbs_Curves to Face', 'Nurbs_facedraw',

        'Part_Cone', 'Part_Cylinder','Draft_Move','Draft_Rotate','Draft_Point','Draft_ToggleGrid',
        'My_Test2','Sketcher_NewSketch',
        #'Nurbs_facedraws','Nurbs_patcha','Nurbs_patchb','Nurbs_folda'
        ]

        cmds2=['Nurbs_facedraw','Nurbs_patcha','Nurbs_patchb','Nurbs_folda']
        
        cmds3=['Nurbs_CreateWorkspace','Nurbs_CreateWSLink','Nurbs_ViewsQV','Nurbs_Views2H','Nurbs_DarkRoom','Nurbs_LightOn','Nurbs_LightOff']
        cmds4=['Nurbs_pta','Nurbs_ptb','Nurbs_ptc','Nurbs_ptd','Nurbs_pte']
        cmds5=['Nurbs_geodesic'+str(a+1) for a in range(6)]
        cmds5 += ['Nurbs_multiEdit', 'Nurbs_AA','Nurbs_BB']



        if 1:
            self.appendMenu("Nurbs", cmds)
#            self.appendToolbar("TTT", cmds2 )
            self.appendToolbar("Nurbs", cmds )
            self.appendToolbar("Workspaces and Views", cmds3 )
            self.appendToolbar("Points Workspaces and Views", cmds4 )
            self.appendToolbar("Geodesic Patch Tests", cmds5 )

#            print ("create toolbars-------------------------")
            for t in self.toolbars:
#                print (t)
                self.appendToolbar(t[0], t[1])


        menues={}
        ml=[]
        for _t in App.tcmds5:
            c=_t[0]
            a=_t[1]
            try:menues[tuple(c)].append(a)

            except: 
                menues[tuple(c)]=[a]
                ml.append(tuple(c))

        for m in ml:
            self.appendMenu(list(m),menues[m])

        # create menues
        menues = {}
        ml = []
        for _t in App.tcmdsNurbs:
            c = _t[0]
            a = _t[1]
            try:
                menues[tuple(c)].append(a)

            except:
                menues[tuple(c)] = [a]
                ml.append(tuple(c))

        for m in ml:
            self.appendMenu(list(m), menues[m])





#Gui.addWorkbench(NurbsWorkbench(toolbars, __vers__))

"""
