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
import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit


sys.path.insert(0, './nurbs')
import configuration
import nurbs
import views
import re
__title__ = "FreeCAD Nurbs Library"

__vers__ = "V???"


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
        #reload(TestNurbsGui)
        TestNurbs
        #reload(TestNurbs)
        QtUnitGui.addTest("TestNurbsGui")
        QtUnitGui.addTest("TestNurbs")

    def GetResources(self):
        return {'MenuText': 'Test-test...', 'ToolTip': 'Runs the self-test for the workbench'}


Gui.addCommand('My_Test2', MyTestCmd2())
# Gui.runCommand('My_Test2')


# ------------------------------------------
# fast command adder template

global _Command2


class _Command2():

    def __init__(self, lib=None, name=None, icon=NURBSinit.ICONS_PATH+'nurbs.svg', command=None, modul='', tooltip='No Tooltip'):

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
            self.icon =icon
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
            Gui.doCommand("#reload(" + self.lmod + ")")
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

    def __init__(self, lib=None, name=None, icon=NURBSinit.ICONS_PATH+'nurbs.svg', command=None, modul='nurbs'):

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
            self.icon = icon
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
        if Gui.ActiveDocument:
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
            #Gui.doCommand("import " + modul)
            #Gui.doCommand("import "+self.lmod)
            #Gui.doCommand("#reload("+self.lmod+")")
            print(self.command)
            Gui.doCommand(self.command)
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
    return Gui.ActiveDocument is not None


def onselection():
    '''if at least one object is selected'''
    return len(Gui.Selection.getSelectionEx()) > 0


def onselection1():
    '''if exactly one object is selected'''
    return len(Gui.Selection.getSelectionEx()) == 1


def onselection2():
    '''if exactly two objects are selected'''
    return len(Gui.Selection.getSelectionEx()) == 2


def onselection3():
    '''if exactly three objects are selected'''
    return len(Gui.Selection.getSelectionEx()) == 3


def onselex():
    '''if at least one subobject is selected'''
    return len(Gui.Selection.getSelectionEx()) != 0


def onselex1():
    '''if exactly one subobject is selected'''
    return len(Gui.Selection.getSelectionEx()) == 1


# the menu entry list
App.tcmds5 = []

# create menu entries
'''
def c1(menu,name,*info):
    global _Command
    name1="Nurbs_"+name
    t=_Command(name,*info)
    Gui.addCommand(name1,t)
    App.tcmds5.append([menu,name1,name,'always',info])
'''


def c1a(menu, isactive, name, *info):
    global _Command
    name1 = "Nurbs_"+name
    t = _Command(name, *info)
    t.IsActive = isactive
    Gui.addCommand(name1, t)
    App.tcmds5.append([menu, name1, name, isactive, info])


'''
def c2(menu,title,name,*info):
    #print info
    global _Command
    title1="Nurbs_"+title
    Gui.addCommand(title1,_Command(name,*info))
    App.tcmds5.append([menu,title1,name,'always',info])
'''


def c2a(menu, isactive, title, name, *info):
    global _Command
    t = _Command(name, *info)
    title1 = "Nurbs_"+title
    t.IsActive = isactive
    Gui.addCommand(title1, t)
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
    Gui.addCommand(name1, t)
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
#        icon=NURBSinit.ICONS_PATH+''+pic+'.svg'

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
        icon = NURBSinit.ICONS_PATH+''+pic+'.svg'

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
    docname = App.ParamGet(
        'User parameter:Plugins/nurbs').GetString("Document", "Needle")
    try:
        App.getDocument(docname)
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


#if App.GuiUp:

# by mariwan                            global beztools 
# by mariwan                            global _beztools
# by mariwan                            global current 
# by mariwan                            global _current
# by mariwan                            beztools = []
# by mariwan                            _beztools = []
# by mariwan                            current = []
# by mariwan                            _current = []
# by mariwan                            [c3bI(["Bezier"], always, 'upgradeobjects', 'upgrade Object')]
# by mariwan                            [c3bI(["Bezier"], always, 'upgradeobjects', 'dump Object')]
# by mariwan                            [c3bI(["Bezier"], always, 'approximator', 'activate Execution')]
# by mariwan                            [c3bI(["Bezier"], always, 'approximator', 'deactivate Execution')]
# by mariwan                            #    [c3bI(["Bezier"], always, 'approximator', 'A')]
# by mariwan                            #    [c3bI(["Bezier"], always, 'approximator', 'B')]
# by mariwan                            beztools += [c3bI(["Bezier", "Assembly"], always, 'morpher',                  'create Morpher', tooltip='morph two Bezier faces')]
# by mariwan                            beztools += [c3bI(["Bezier", "Assembly"], always, 'morpher', 'curve morphed Face',                  tooltip='create a surface by 4 border curves')]
# by mariwan                            [c3bI(["Bezier"], always, 'berings', 'flatten the wire')]
# by mariwan                            [c3bI(["Bezier"], always, 'approximator', 'Ribs to Face')]
# by mariwan                            [c3bI(["Bezier"], always, 'approximator', 'swap Curves')]
# by mariwan                            [c3bI(["Bezier"], always, 'approximator', 'curves to Face')]
# by mariwan                            [c3bG(["Bezier"], always, 'approximator', 'create MyMin A')]
# by mariwan                            [c3bG(["Bezier"], always, 'approximator', 'create MyMin Soft')]
# by mariwan                            [c3bG(["Bezier"], always, 'approximator',      'create BezierPoles Frame from ribs')]
# by mariwan                            beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Tripod',             tooltip='create a tripod onto the selected face')]
# by mariwan                            beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Tripod Sketch',                  tooltip='create a tripod with a sketch onto the selected face')]
# by mariwan                            beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Sweep',                  tooltip='create a Sweep of the selected ribs')]
# by mariwan                            beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Loft',                  tooltip='create a Loft of the selected ribs')]
# by mariwan                            beztools += [c3bI(["Faces"], always, 'tripod_2', 'create Compound',                  tooltip='create a compound of the selection')]
# by mariwan                            [c3bG(["Points"], always, 'approximator', 'load Pointcloud from Image')]
# by mariwan                            [c3bG(["Points"], always, 'approximator', 'load Cylinderface from Image')]
# by mariwan                            beztools += [c3bG(["Points"], always, 'approximator',                  'Bump Face from Image', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            [c3bG(["Points"], always, 'approximator', 'smooth Pointcloud')]
# by mariwan                            [c3bI(["Bezier"], always, 'berings', 'create Sketch Circle')]
# by mariwan                            beztools += [c3bI(["Bezier", "Create"], always,                  'berings', 'create BePlane')]
# by mariwan                            beztools += [c3bI(["Bezier", "Create"], always,                  'berings', 'create BeTube')]
# by mariwan                            beztools += [c3bI(["Bezier", "Create"], always,                  'berings', 'create Helmet')]
# by mariwan                            c3b(["Bezier", "Create"], always, 'berings', 'create Datum Plane')
# by mariwan                            c3b(["Bezier", "Create"], always, 'berings', 'create Datum Line')
# by mariwan                            c3bI(["Bezier", "Assembly"], always, 'berings', 'create Triangle')
# by mariwan                            c3bI(["Bezier", "Assembly"], always,     'berings', 'create Plane Tube Connector')
# by mariwan                            c3bI(["Bezier", "Assembly"], always,     'berings', 'create Helmet Tube Connector')
# by mariwan                            beztools += [c3bI(["Bezier", "Assembly"], always,                  'berings', 'create Bering')]
# by mariwan                            c3bG(["Bezier", "Assembly"], always, 'berings',     'create Tangent Helpers', NURBSinit.ICONS_PATH + "alpha.svg")
# by mariwan                            beztools += [c3bI(["Bezier", "Assembly"], always,                  'berings', 'create Beface')]
# by mariwan                            #    c3bG(["Bezier"], always, 'parameters', 'run')
# by mariwan                            c3bI(["Bezier", "Assembly"], always, 'berings', 'create Product')
# by mariwan                            c3bI(["Bezier", "Assembly"], always, 'berings', 'connect Faces')
# by mariwan                            c3bI(["Bezier", "Assembly"], always, 'berings', 'create Seam')
# by mariwan                            c3bG(["Bezier", "Assembly"], always, 'berings', 'create Gordon')
# by mariwan                            c3b(["Bezier", "Convert"], always, 'berings', 'BSpline To Bezier Curve')
# by mariwan                            c3b(["Bezier", "Convert"], always, 'berings', 'BSpline To Bezier Surface')
# by mariwan                            c3b(["Bezier", "Convert"], always, 'berings', 'Face To Bezier Surface')
# by mariwan                            c3bG(["Bezier", "Convert"], always, 'berings', 'create Approx',     NURBSinit.ICONS_PATH + "alpha.svg")
# by mariwan                            #current += [c3bI(["Bezier"], always, 'points_to_wires','AA', tooltip="Eine Testfunktion")]
# by mariwan                            #current += [c3bI(["Bezier"], always, 'points_to_face','Reconstruct Sphere', tooltip="Subselection to Sphere", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], always, 'points_to_face','Reconstruct Cylinder', tooltip="Subselection to Cylinder", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], always, 'points_to_face','optimize Cylinder', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], always, 'points_to_face','Reconstruct Plane', tooltip="Subselection to Plane", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], onselection1, 'points_to_face','noisy mesh', tooltip="add noise to a mesh", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], onselection, 'merge_faces','merge 2 Faces', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], onselection, 'merge_faces','merge 2 Faces B', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Bezier"], always, 'minimumsurface','test minimal surface', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            
# by mariwan                            #    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'create Array',icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'split Edges',icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Pattern"], onselection, 'pattern_v2','remove Edges', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'create Single Pattern',icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #    current += [c3bI(["Pattern"], onselection, 'pattern_v2', 'create Pattern',icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Pattern"], onselection,                 'pattern_v2', 'pattern V3', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            #current += [c3bI(["Pattern"], always, 'pattern_v2',                 'pattern all tests', icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            
# by mariwan                            
# by mariwan                            #    beztools += [c3bI(["Points"], always, 'points_to_face', 'Points to Cone',tooltip="P1,N1,P2,P3,P4",icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            beztools += [c3bI(["Bezier"], always, 'geodesic2', 'BB',tooltip="Eine andere Testfunktion")]
# by mariwan                            #    beztools += [c3bI(["Points"], always, 'points_to_face', 'Points to Cone',tooltip="P1,N1,P2,P3,P4",icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'points_to_face',   'Points to Cone PN P P P', tooltip="P1,N1,P2,P3,P4", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'points_to_face',   'Points to Cone PN PN ', tooltip="P1,N1,P2,N2", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'points_to_face',   'Points to Cylinder PN P P', tooltip="P1,N1,P2,P3", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            beztools += [c3bI(["Points"], always, 'points_to_face',  'Points to Cylinder 5P', tooltip="P1,P2,P3,p4,p%", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'points_to_face',   'Points to Sphere 4P', tooltip="P1,P2,P3,p4", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'points_to_face',   'Points to Sphere PN P', tooltip="P1,N1,P2", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'perspective_trafos', 'createPerspectiveTrafo',                   tooltip="perspektiische Tranformation 3D einer Flaeche", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            _beztools += [c3bI(["Points"], always, 'concave_hull', 'create concave hull 2D',                   tooltip="alpha shape fuer eine point cloud", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            beztools += [c3bI(["Curves", "Geodesic"], always, 'geodesic2', 'create a Path',                  tooltip="create a connection between two points of a Face", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            beztools += [c3bI(["Curves", "Geodesic"], always, 'geodesic2', 'optimize Path',                  tooltip="apporximate geodesic curve between two points starting form a given path", icon=NURBSinit.ICONS_PATH + "noIcon.svg")]
# by mariwan                            
# by mariwan                            c3bI(["Bezier"], always, 'berings', 'add Knot')
# by mariwan                            [c3bI(["Bezier"], always, 'multiedit', 'multiEdit')]
# by mariwan                            
# by mariwan                            #    old version Surface Editor
# by mariwan                            #    c3b(["Bezier"], always, 'berings', 'Surface Editor')
# by mariwan                            
# by mariwan                            c3bI(["Bezier"], always, 'berings', 'create Be Grid')
# by mariwan                            c3bI(["Bezier", "Segments"], always, 'berings', 'Split Into Cells')
# by mariwan                            c3bI(["Bezier", "Segments"], always, 'berings', 'create Cell')
# by mariwan                            c3bI(["Bezier", "Segments"], always, 'berings', 'create Hole')
# by mariwan                            c3bG(["Bezier", "Segments"], always, 'berings', 'create Border',     NURBSinit.ICONS_PATH + "alpha.svg")
# by mariwan                            c3bI(["Bezier", "Convert"], always, 'berings', 'create QuadPlacement',     NURBSinit.ICONS_PATH + "alpha.svg")
# by mariwan                            c3bI(["Bezier", "Convert"], always, 'berings', 'stretch and bend')
# by mariwan                            c3bG(["Bezier", "Convert"], always, 'berings', 'polish G1',     NURBSinit.ICONS_PATH + "alpha.svg")
# by mariwan                            c3bI(["Bezier", "Diagnostics"], ondocument, 'monitor', 'create a force monitor',     NURBSinit.ICONS_PATH+'nurbs.svg', "runforce()")
# by mariwan                            c3bI(["Bezier", "Specials"], always, 'berings', 'fix Corner')
# by mariwan                            c3bI(["Bezier", "Specials"], always, 'berings', 'create Tangent Stripes')
# by mariwan                            [c3bG(["Bezier", "Specials"], always, 'approximator', 'minimum Length Bezier')]
# by mariwan                            [c3bG(["Bezier", "Specials"], always, 'approximator',      'near constant Curvature Bezier')]
# by mariwan                            [c3bI(["Bezier", "Specials"], always, 'leastsq', 'leastsq Bezier')]
# by mariwan                            [c3bI(["Bezier", "Specials"], always, 'leastsq', 'leastsq Bezier Two Segments')]
# by mariwan                            c3bI(["Bezier", "Specials"], always, 'berings', 'glaetten')
# by mariwan                            c3bI(["Bezier", "Specials"], always, 'berings', 'solid')
# by mariwan                            c3bI(["Bezier", "Specials"], always,     'approximation', 'create Approximation')
# by mariwan                            c3bI(["Bezier", "Specials"], always,     'approximation', 'create Poles for Test')
# by mariwan                            
# by mariwan                            # -------------------------------------------
# by mariwan                            mt = "Transportation V0"
# by mariwan                            c2a([mt], ondocument, 'LoadSketch', 'sketchmanager', 'load sketch from a sketchlib',    NURBSinit.ICONS_PATH+'sketchlibload.svg', "runLoadSketch()")
# by mariwan                            c2a([mt], onselection2, 'Status155', 'feedbacksketch', 'connect road to line ',    NURBSinit.ICONS_PATH + "alpha.svg", "connectLine()", "sketcher")
# by mariwan                            c2b([mt], ondocument, 0, 'sketch_to_bezier', 'create Arc Sketch',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b([mt], onselection1, 0, 'sketch_to_bezier',    'create Labels', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b([mt], onselection1, 0, 'sketch_to_bezier',    'create Stations', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b([mt], ondocument, 0, 'sketch_to_bezier', 'create LatLonMarker',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b([mt], onselection, 0, 'sketch_to_bezier',    'update Labels', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            
# by mariwan                            # -------------------------------------------
# by mariwan                            
# by mariwan                            c2b(["SMOOTH"], onselection1, 0, 'smooth', 'smooth Wire',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["SMOOTH"], onselection1, 0, 'smooth', 'smooth Mesh',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["SMOOTH"], onselection1, 0, 'smooth', 'split Mesh',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["SMOOTH"], onselection2, 0, 'smooth', 'slice Mesh by Sketch',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["SMOOTH"], onselection2, 0, 'smooth', 'distance Curves',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["SMOOTH"], onselection2, 0, 'smooth', 'draw Path',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["Sketchertools"], ondocument, 0, 'sketch_to_bezier',    'create Bezier Sketch', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["Sketchertools"], ondocument, 0, 'sketch_to_bezier',    'create Arc Sketch', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["Sketchertools"], onselection1, 0, 'sketch_to_bezier',    'create Labels', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["Sketchertools"], onselection, 0, 'sketch_to_bezier',    'update Labels', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            # geodesics
# by mariwan                            c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',    'create Curvature Star', NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',    'create Geodesic', NURBSinit.ICONS_PATH+'geodesic.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',    'geodesic Distance', NURBSinit.ICONS_PATH+'geodesiccircle.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], onselection2, 0, 'geodesic_lines',    'geodesic Map Patch To Face', NURBSinit.ICONS_PATH+'patch.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], ondocument, 0, 'geodesic_lines',    'create Marker', NURBSinit.ICONS_PATH+'geodesic_ref.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], onselection2, 0, 'geodesic_lines',    'find Geodesic To Target', NURBSinit.ICONS_PATH+'geodesic_target.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',    'append Geodesic', NURBSinit.ICONS_PATH+'geodesic_append.svg')
# by mariwan                            c2b(["Curves", "Geodesic"], onselection1, 0, 'geodesic_lines',    'create geodesic bunch', NURBSinit.ICONS_PATH+'geodesic_bunch.svg')
# by mariwan                            # shoe
# by mariwan                            c2b(["Shoe", "Markers"], always, 0, 'geodesic_lines',    'create Shoe Markers', NURBSinit.ICONS_PATH+'geodesic_ref.svg')
# by mariwan                            c2b(["Shoe", "Markers"], always, 0, 'geodesic_lines', 'connect Markers',    NURBSinit.ICONS_PATH+'geodesic_target.svg')
# by mariwan                            c1a(["Curves"], always, "scancut", "cut Scanned Mesh ",    NURBSinit.ICONS_PATH+'mesh_cut.svg')
# by mariwan                            c1a(["Curves"], ondocument, "weighteditor", "Weight Editor")
# by mariwan                            c1a(["Curves"], ondocument, "simplecurve", "simplify curve")
# by mariwan                            c1a(["Curves"], onselection1, "removeknot", "remove a knot in a bspline")
# by mariwan                            c1a(["Curves"], onselection2, "curvedistance",    "calculate the distance between two curves")
# by mariwan                            c1a(["Curves"], always, "createsketchspline", "create Sketcher BSpline from a curve",    NURBSinit.ICONS_PATH+'createsketchspline.svg')
# by mariwan                            c1a(["Curves"], ondocument, "weighteditor", "Weight Editor")
# by mariwan                            #c2a(["Curves"],onselection1,'DraftBSpline Editor',"DraftBSplineEditor","Edit Draft Bspline",NURBSinit.ICONS_PATH+'32px-draftbspline_edit.png',"run()")
# by mariwan                            c2a(["Curves"], always, 'DraftBSpline Editor', "DraftBSplineEditor", "Edit Draft Bspline",    NURBSinit.ICONS_PATH+'32px-draftbspline_edit.png', "run()")
# by mariwan                            c2a(["Curves"], always, 'facedraw', 'facedraw', 'draw on a face',    NURBSinit.ICONS_PATH+'draw.svg', "run()")
# by mariwan                            #    c2a(["Curves"],always,'facedraws','facedraw_segments','draw over segments',NURBSinit.ICONS_PATH+'draw.svg',"run()")
# by mariwan                            c2a(["Curves"], always, 'facedrawa', 'facedraw', 'create Map of a face',    NURBSinit.ICONS_PATH+'draw.svg', "createMap()")
# by mariwan                            c2a(["Curves"], always, 'facedrawa2', 'facedraw', 'create Curvature Map of a face',    NURBSinit.ICONS_PATH+'draw.svg', "createMap(mode='curvature')")
# by mariwan                            c2a(["Curves"], always, 'curvaturea', 'curvatureplot',    'draw the curvature net', NURBSinit.ICONS_PATH+'draw.svg', "run()")
# by mariwan                            c2a(["Curves"], always, 'facedrawb', 'facedraw', 'create Grids for a face',    NURBSinit.ICONS_PATH+'draw.svg', "createGrid()")
# by mariwan                            c2a(["Curves"], always, 'isodraw32', 'isodraw', '3D to 2D',    NURBSinit.ICONS_PATH+'draw.svg', "map3Dto2D()")
# by mariwan                            c2a(["Curves"], always, 'isodraw23', 'isodraw', '2D to 3D',    NURBSinit.ICONS_PATH+'draw.svg', "map2Dto3D()")
# by mariwan                            c2a(["Curves"], always, 'isodraw24', 'isodraw', '3D Grid to 2D Grid',    NURBSinit.ICONS_PATH+'draw.svg', "map3Dgridto2Dgrid()")
# by mariwan                            c2b(["Curves"], always, 0, 'isodraw', 'create Brezel',    NURBSinit.ICONS_PATH+'draw.svg')
# by mariwan                            #    c2a(["Curves"],always,'importColorSVG','shoe_importSVG','import SVG for shoes',NURBSinit.ICONS_PATH+'draw.svg',"import_test()")
# by mariwan                            
# by mariwan                            c2a(["Curves"], always, 'holes', 'holes', 'Play with holes on a surface',    NURBSinit.ICONS_PATH+'draw.svg', "run()")
# by mariwan                            c2a(["Curves"], always, 'holeswires', 'holes', 'extract the wires of the selected part',    NURBSinit.ICONS_PATH+'draw.svg', "extractWires()")
# by mariwan                            c2a(["Curves"], always, 'linkSVG', 'shoe_importSVG', 'create link to SVG file',    NURBSinit.ICONS_PATH+'draw.svg', "create_svglink()")
# by mariwan                            c2a(["Curves"], always, 'impSVG', 'shoe_importSVG', 'import svg file',    NURBSinit.ICONS_PATH+'draw.svg', "import_svg()")
# by mariwan                            c2a(["Curves"], always, 'expSVG', 'shoe_importSVG', 'export svg file',    NURBSinit.ICONS_PATH+'draw.svg', "export_svg()")
# by mariwan                            c2a(["Curves"], always, 'cnotrol', 'controlpanel', 'create a controlpanel',    NURBSinit.ICONS_PATH+'draw.svg', "run()")
# by mariwan                            c2a(["Curves"], always, 'beziera', 'bezier', 'selected face to sketch',    NURBSinit.ICONS_PATH+'draw.svg', "faceToSketch()")
# by mariwan                            c2a(["Curves"], always, 'bezierb', 'bezier', 'selected edges to sketches',    NURBSinit.ICONS_PATH+'draw.svg', "subsToSketch()")
# by mariwan                            c2a(["Curves"], always, 'transform_spline', 'transform_spline',    'perspective transformation of a Bbspline', NURBSinit.ICONS_PATH+'upgrade.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'createcloverleaf', 'createcloverleaf',    'create a cloverleaf', NURBSinit.ICONS_PATH+'cloverleaf.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'createshoerib', 'createshoerib',    'create a shoe last rib', NURBSinit.ICONS_PATH+'cloverleaf.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'project_edge2face1', 'project_edge2face',    'parallel projection of edge to face', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'project_edge2face2', 'project_edge2face',    'parallel projection of selection to face', NURBSinit.ICONS_PATH+'nurbs.svg', "runAll()")
# by mariwan                            c2a(["Curves"], ondocument, 'project_edge2face3', 'project_edge2face',    'concatenate Draft.BSplines', NURBSinit.ICONS_PATH+'nurbs.svg', "concatenateBSplines()")
# by mariwan                            c2a(["Curves"], onselection1, 'project_edge2face4', 'project_edge2face',    'split curve in xy, sz', NURBSinit.ICONS_PATH+'nurbs.svg', "splitCurve()")
# by mariwan                            c2a(["Curves"], onselection2, 'project_edge2face5', 'project_edge2face',    'combine sz,xy, to 3dCurve', NURBSinit.ICONS_PATH+'nurbs.svg', "combineCurve()")
# by mariwan                            c2a(["Curves"], ondocument, 'loft_selection', 'loft_selection',    'loft between two selections', NURBSinit.ICONS_PATH+'Loft.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'loft_selectionEdges', 'loft_selection',    'loft between two selected edges', NURBSinit.ICONS_PATH+'Loft.svg', "runOnEdges()")
# by mariwan                            c2a(["Curves"], ondocument, 'knotsandpoles', 'knotsandpoles',    'display knots and poles for selected curves', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'monitor', 'monitor', 'create a monitor for a curve length',    NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'param_bspline', 'param_bspline',    'create a parametric bspline with tangents', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'OffsetSpline', 'curves', 'create a Sketch for a OffsetSpline',    NURBSinit.ICONS_PATH+'nurbs.svg', "runOffsetSpline()")
# by mariwan                            c2a(["Curves"], ondocument, 'Stare', 'curves', 'create a Sketch for a Star',    NURBSinit.ICONS_PATH+'nurbs.svg', "runStar()")
# by mariwan                            c2a(["Curves"], ondocument, 'DynamicOffset', 'dynamicoffset',    'create a dynamic Offset', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'FloatList', 'datatools', 'create a floatlist',    NURBSinit.ICONS_PATH+'nurbs.svg', "runFloatlist()")
# by mariwan                            c2a(["Curves"], ondocument, 'Sole', 'create_sole_sketch',    'create a sole as offsetspline', NURBSinit.ICONS_PATH+'nurbs.svg', "runSole()")
# by mariwan                            c2a(["Curves"], onselection2, 'MoveAlongCurve', 'move_along_curve',    'move an object #2 along a bspline curve #1', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Curves"], ondocument, 'SketchClone', 'sketchclone', 'create a semi clone of a sketch',    NURBSinit.ICONS_PATH+'sketchdriver.svg', "runSketchClone()")
# by mariwan                            c2a(["Faces", "create"], always, 'Random Plane', "nurbs", "Create plane with randoms",    NURBSinit.ICONS_PATH+'plane.svg', "testRandomB()")
# by mariwan                            c2a(["Faces", "create"], always, 'Random Torus', "nurbs", "Create torus with randoms",    NURBSinit.ICONS_PATH+'torus.svg', "testRandomTorus()")
# by mariwan                            c2a(["Faces", "create"], always, 'Random Cylinder', "nurbs", "Create cylinder with randomness",    NURBSinit.ICONS_PATH+'cylinder.svg', "testRandomCylinder()")
# by mariwan                            c2a(["Faces", "create"], always, 'Random Sphere', "nurbs", "Create sphere with randomness",    NURBSinit.ICONS_PATH+'sphere.svg', "testRandomSphere()")
# by mariwan                            c2a(["Faces", "create"], ondocument, 'simple Hood', 'simplehood',    'create a simple hood', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Faces", "create"], ondocument, 'grid test data', 'mesh_generator',    'create a grid testset', NURBSinit.ICONS_PATH+'nurbs.svg', "gentest()")
# by mariwan                            c2a(["Faces", "create"], ondocument, 'helm', 'helmlet', 'create a helmlet',    NURBSinit.ICONS_PATH+'nurbs.svg', "createHelmlet()")
# by mariwan                            c2a(["AAA"], onselection1, 'corridor2a', 'corridor', 'wire to bspline',    NURBSinit.ICONS_PATH+'nurbs.svg', "WireToBSpline()")
# by mariwan                            c2a(["Faces", "create"], onselection2, 'corridor', 'corridor',    'create a corridor for a path on s face testset', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'sculpt', 'sculpter', 'sculpt a face (MyGrid)',    NURBSinit.ICONS_PATH+'beta.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'patcha', 'patch', 'connect 2 curve segments to a face',    NURBSinit.ICONS_PATH+'beta.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'patchb', 'patch', 'patch b',    NURBSinit.ICONS_PATH+'alpha.svg', "runb()")
# by mariwan                            c2a(["Faces"], ondocument, 'folda', 'folding', 'create a folding of a face',    NURBSinit.ICONS_PATH+'testit.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'unrolla', 'unroll_curve', 'unroll curve Yaw from a face',    NURBSinit.ICONS_PATH+'nurbs.svg', "unroll_yaw()")
# by mariwan                            c2a(["Faces"], ondocument, 'unrollb', 'unroll_curve', 'unroll curve Pitch from a face',    NURBSinit.ICONS_PATH+'nurbs.svg', "unroll_pitch()")
# by mariwan                            c2a(["Faces"], ondocument, 'unrollc', 'unroll_curve', 'combine Yaw and Pitch curces',    NURBSinit.ICONS_PATH+'nurbs.svg', "combineCT()")
# by mariwan                            c2a(["Shoe"], ondocument, 'Sole Change Model', 'sole_change_model',    'Shoe Sole Change Model', NURBSinit.ICONS_PATH+'solechange.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'load Sole Height', 'load_sole_profile_height',    'Load Height Profile', NURBSinit.ICONS_PATH+'sole.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'load Sole Widht', 'load_sole_profile_width',    'Load Width Profile', NURBSinit.ICONS_PATH+'sole.svg', "run()")
# by mariwan                            c2a(["Faces"], ondocument, 'Iso Map', 'isomap', 'draw isomap of Face',    NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Faces", "create"], always, 'Nurbs Editor', 'nurbs',    'creates a test nurbs', NURBSinit.ICONS_PATH+'zebra.svg', "runtest()")
# by mariwan                            c2a(["Faces", "create"], onselection, 'UV Grid Generator', 'uvgrid_generator',    'create UV grid of the partr', NURBSinit.ICONS_PATH+'nurbs.svg', "runSel()")
# by mariwan                            c2a(["Faces", "create"], onselection, 'Nurbs Helper', 'helper',    'create helper objects of the part', NURBSinit.ICONS_PATH+'nurbs.svg', "makeHelperSel()")
# by mariwan                            c2a(["Faces", "create"], ondocument, 'Create QR Code', 'createbitmap',    'create a qr code surface', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Faces"], always, 'filledface', 'filledface', 'createFilledFace',    NURBSinit.ICONS_PATH+'nurbs.svg', "createFilledFace()")
# by mariwan                            c2a(["Faces"], always, 'ZebraTool', 'zebratool', 'ZebraTool',    NURBSinit.ICONS_PATH+'zebra.svg', "run()")
# by mariwan                            c2a(["Faces"], always, 'Curves to Face', 'curves2face',    'Curves to Face', NURBSinit.ICONS_PATH+'upgrade.svg', "run()")
# by mariwan                            c2a(["Faces"], always, 'Segment', 'segment', 'Cut a segment of a Face',    NURBSinit.ICONS_PATH+'nurbs.svg', "runsegment()")
# by mariwan                            c2a(["Faces"], always, 'FineSegment', 'segment', 'Cut a fine segment of a Face',    NURBSinit.ICONS_PATH+'nurbs.svg', "runfinesegment()")
# by mariwan                            c2a(["Faces"], always, 'NurbsTrafo', 'segment', 'Transform a Face',    NURBSinit.ICONS_PATH+'nurbs.svg', "runnurbstrafo()")
# by mariwan                            c2a(["Faces"], always, 'Tangent', 'tangentsurface', 'create a tangent Face',    NURBSinit.ICONS_PATH+'tangentsurface.svg', "runtangentsurface()")
# by mariwan                            c2a(["Faces"], always, 'Seam', 'tangentsurface', 'create a Seam',    NURBSinit.ICONS_PATH+'createSeam.svg', "runseam()")
# by mariwan                            c2a(["Faces"], always, 'Grid generator', 'uvgrid_generator',    'create a uv-grid for a Face', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Topology"], always, 'Topological Analyse', 'analyse_topology_v2',    'topological analysis', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Topology"], always, 'Topological Compare', 'analyse_topology_v2',    'topological compare', NURBSinit.ICONS_PATH+'nurbs.svg', "runCompare()")
# by mariwan                            c2a(["Topology"], always, 'Topo8', 'analyse_topology_v2', 'display Quality Points',    NURBSinit.ICONS_PATH+'nurbs.svg', "displayQualityPoints()")
# by mariwan                            c2a(["Topology"], always, 'Topo5', 'analyse_topology_v2', 'print Graph Data',    NURBSinit.ICONS_PATH+'nurbs.svg', "printData()")
# by mariwan                            c2a(["Topology"], always, 'Topo4', 'analyse_topology_v2', 'add to Vertex Store',    NURBSinit.ICONS_PATH+'nurbs.svg', "addToVertexStore()")
# by mariwan                            c2a(["Topology"], always, 'Topo2', 'analyse_topology_v2', 'print Vertex Store Dump',    NURBSinit.ICONS_PATH+'nurbs.svg', "printVertexStore()")
# by mariwan                            c2a(["Topology"], always, 'Topo2a', 'analyse_topology_v2', 'display Vertex Store Common Points',    NURBSinit.ICONS_PATH+'nurbs.svg', "displayVertexStore()")
# by mariwan                            c2a(["Topology"], always, 'Topo3', 'analyse_topology_v2', 'reset Vertex Store',    NURBSinit.ICONS_PATH+'nurbs.svg', "resetVertexStore()")
# by mariwan                            c2a(["Topology"], always, 'Topo6', 'analyse_topology_v2', 'load Test 1',    NURBSinit.ICONS_PATH+'nurbs.svg', "loadTest1()")
# by mariwan                            c2a(["Topology"], always, 'Topo7', 'analyse_topology_v2', 'load Test 2',    NURBSinit.ICONS_PATH+'nurbs.svg', "loadTest2()")
# by mariwan                            c2a(["Topology"], always, 'Topo10', 'fem_edgelength_mesh',    'Grid Tension Simulation', NURBSinit.ICONS_PATH+'nurbs.svg', "run()")
# by mariwan                            c2a(["Topology"], always, 'Topo9', 'analyse_topology_v2',    'Identify Vertexes in a Shape', NURBSinit.ICONS_PATH+'nurbs.svg', "Test4()")
# by mariwan                            c2a(["Topology"], always, 'Topo11', 'fem_edgelength_mesh',    'Grid Tension Animation', NURBSinit.ICONS_PATH+'nurbs.svg', "run(False)")
# by mariwan                            c2a(["Topology"], always, 'Topo12', 'analyse_topology_v2',    'Test 4', NURBSinit.ICONS_PATH+'nurbs.svg', "Test4()")
# by mariwan                            c2a(["Workspace"], ondocument, 'CreateWorkspace', None, "Create workspace",    NURBSinit.ICONS_PATH+'workspace.svg', "createws()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'CreateWSLink', None, "Create workspace link",    NURBSinit.ICONS_PATH+'workspacelink.svg', "createlink()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'ViewsQV', 'views', "Create QuadView",    NURBSinit.ICONS_PATH+'workspacequad.svg', "createquadview()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'Views2H', 'views', "Create 2 horizontal views",    NURBSinit.ICONS_PATH+'workspace2h.svg', "createh2()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'DarkRoom', 'views', "Create Dark Room",    NURBSinit.ICONS_PATH+'darkroom.svg', "createdarkroom()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'Light', 'views', "Create Light",    NURBSinit.ICONS_PATH+'light.svg', "createlight()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'LightOn', 'views', "Light on",    NURBSinit.ICONS_PATH+'light_on.svg', "lightOn()", "initGUI")
# by mariwan                            c2a(["Workspace"], ondocument, 'LightOff', 'views', "Light off",    NURBSinit.ICONS_PATH+'light_off.svg', "lightOff()", "initGUI")
# by mariwan                            c2a(["Needle"], ondocument, 'Needle', 'needle', 'create a needle',    NURBSinit.ICONS_PATH+'shoe.svg', "run()")
# by mariwan                            c2a(["Needle"], onneedle, 'needle Change Model', 'needle_change_model',    'needle Change Model', NURBSinit.ICONS_PATH+'shoe.svg', "run()")
# by mariwan                            c2a(["Needle"], onselex1, 'addULine', 'needle_cmds', 'add Meridian/Rib',    NURBSinit.ICONS_PATH+'add_edge.svg', "cmdAdd()")
# by mariwan                            c2a(["Needle"], onselex1, 'deleteULine', 'needle_cmds', 'delete Meridian/Rib',    NURBSinit.ICONS_PATH+'delete_edge.svg', "cmdDel()")
# by mariwan                            c2a(["Needle"], onspread, 'Open Spreadsheet', 'wheel_event', 'Open Spreadsheet',    NURBSinit.ICONS_PATH+'nurbs.svg', "undock('Spreadsheet')")
# by mariwan                            c2a(["Needle"], onneedle, 'Edit Rib', 'wheel_event', 'Edit Rib',    NURBSinit.ICONS_PATH+'nurbs.svg', "start('Rib_template')")
# by mariwan                            c2a(["Needle"], onneedle, 'Edit Backbone', 'wheel_event', 'Edit Backbone',    NURBSinit.ICONS_PATH+'nurbs.svg', "start('Backbone')")
# by mariwan                            c2a(["Shoe"], always, 'Create Shoe', 'shoe', 'Create Shoe',    NURBSinit.ICONS_PATH+'shoe.svg', "run()")
# by mariwan                            c2a(["Shoe"], always, 'scanbackbonecut', 'scanbackbonecut',    'Cut the Scan along backbone ', NURBSinit.ICONS_PATH+'backbonecut.svg', "run()")
# by mariwan                            c2a(["Shoe"], always, 'Create Sole', 'sole', 'Create Shoe Sole',    NURBSinit.ICONS_PATH+'sole.svg', "run()")
# by mariwan                            c2a(["Shoe"], ondocument, 'toggleSketch', 'shoe_tools', 'toggle constraints of a rib',    NURBSinit.ICONS_PATH+'toggleshoesketch.svg', "toggleShoeSketch()")
# by mariwan                            c2a(["Shoe"], always, 'Generate Docu', "gendok", "generate menu structure docu for web",    NURBSinit.ICONS_PATH+'plane.svg', "run()")
# by mariwan                            c2a(["Shoe"], always, 'DriverSketch', 'skdriver', 'driver test for shoe rib',    NURBSinit.ICONS_PATH+'toggleshoesketch.svg', "runribtest()")
# by mariwan                            c2a(["Shoe"], always, 'DriverSketchAll', 'skdriver', 'driver for all ribs',    NURBSinit.ICONS_PATH+'toggleshoesketch.svg', "runribtest2()")
# by mariwan                            c2a(["Shoe"], always, 'RecomputeAll', 'skdriver', 'recompute shoe',    NURBSinit.ICONS_PATH+'toggleshoesketch.svg', "recomputeAll()")
# by mariwan                            c2a(["Shoe"], always, 'LoadSketch', 'sketchmanager', 'load sketch from a sketchlib',    NURBSinit.ICONS_PATH+'sketchlibload.svg', "runLoadSketch()")
# by mariwan                            c2a(["Shoe"], always, 'SaveSketch', 'sketchmanager', 'save sketch into the sketchlib',    NURBSinit.ICONS_PATH+'sketchlibsave.svg', "runSaveSketch()")
# by mariwan                            c2a(["Shoe"], always, 'DisplaySketchlib', 'sketchmanager', 'list all sketches of the sketchlib',    NURBSinit.ICONS_PATH+'sketchlib.svg', "runSketchLib()")
# by mariwan                            c2a(["Nurbs"], always, 'Grid', 'blender_grid', 'Create Grid',    NURBSinit.ICONS_PATH + "Draft_Grid.svg", "run()")
# by mariwan                            c2a(["Points"], always, 'pta', 'points', 'points to volums',    NURBSinit.ICONS_PATH + "points.svg", "runA()",)
# by mariwan                            c2a(["Points"], always, 'ptb', 'points', 'test B',    NURBSinit.ICONS_PATH + "points.svg", "runB()",)
# by mariwan                            c2a(["Points"], always, 'ptc', 'points', 'create point cloud y = 0.5*x with noise',    NURBSinit.ICONS_PATH + "points.svg", "runC()",)
# by mariwan                            c2a(["Points"], always, 'ptd', 'points', 'approx points with outliner detection',    NURBSinit.ICONS_PATH + "points.svg", "runD()",)
# by mariwan                            c2a(["Points"], always, 'pte', 'points', 'approx point simple',    NURBSinit.ICONS_PATH + "points.svg", "runE()",)
# by mariwan                            c2a(["Neo4j"], always, 'Start', 'neodb', 'start db',    NURBSinit.ICONS_PATH + "neo4j.png", "start()", "graphdb")
# by mariwan                            c2a(["Neo4j"], always, 'Stop', 'neodb', 'stop db',    NURBSinit.ICONS_PATH + "neo4j_stop.png", "stop()", "graphdb")
# by mariwan                            c2a(["Neo4j"], always, 'Status', 'neodb', 'status db',    NURBSinit.ICONS_PATH + "neo4j_status.png", "status()", "graphdb")
# by mariwan                            c2a(["Neo4j"], always, 'Start_OF', 'openflights', 'import_Open Flights',    NURBSinit.ICONS_PATH + "openflights-import.png", "load()", "graphdb")
# by mariwan                            c2a(["Neo4j"], always, 'Reset_OG', 'openflights', 'reset_Open Flights',    NURBSinit.ICONS_PATH + "openflights.png", "reset()", "graphdb")
# by mariwan                            c2a(["Sketchertools"], always, 'Status1', 'feedbacksketch', 'fb sketch',    NURBSinit.ICONS_PATH + "alpha.svg", "run_test_two_clients()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status2', 'feedbacksketch', 'revers order of constraints A',    NURBSinit.ICONS_PATH + "alpha.svg", "run_test_reverse_Constraints()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status3', 'feedbacksketch', 'create Example B',    NURBSinit.ICONS_PATH + "alpha.svg", "runB()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status4', 'feedbacksketch', 'Copy 1.Sketch into 2nd Sketch',    NURBSinit.ICONS_PATH + "sketchcopy.svg", "run_copySketch()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status51', 'feedbacksketch', 'Create FeedBack with 1 client',    NURBSinit.ICONS_PATH + "feedback-1.svg", "run_createFBS_with_one_Client()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status52', 'feedbacksketch', 'Create FeedBack with 2 clients',    NURBSinit.ICONS_PATH + "feedback-2.svg", "run_createFBS_with_two_Clients()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status53', 'feedbacksketch', 'Create FeedBack with 3 clients',    NURBSinit.ICONS_PATH + "feedback-3.svg", "run_createFBS_with_three_Clients()", "sketcher")
# by mariwan                            c2a(["Sketchertools"], always, 'Status56', 'sketcher_grids', 'Create Sketcher Grid',    NURBSinit.ICONS_PATH + "sketchgrid.svg", "createGridSketch()", "sketcher")
# by mariwan                            
# by mariwan                            
# by mariwan                            # hier ist ein fehler
# by mariwan                            #    c2a(["Sketchertools"],always,'Status155','feedbacksketch','connect road to line ',NURBSinit.ICONS_PATH + "alpha.svg","connectLine()","sketcher")
# by mariwan                            
# by mariwan                            
# by mariwan                            #    for cmd in Gui.listCommands():
# by mariwan                            #        if cmd.startswith("Nurbs_"):
# by mariwan                            #            print cmd
# by mariwan                            toolbars=[]
# by mariwan                            toolbars = [
# by mariwan                                    ['Bezier Tools', beztools],
# by mariwan                                    ['My current Work', current]
# by mariwan                                ]
