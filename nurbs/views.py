# -*- coding: utf-8 -*-
# -------------------------------------------------
# -- special view support
# --
# -- microelly 2017 v 0.1
# --
# -- GNU Lesser General Public License (LGPL)
# -------------------------------------------------

import FreeCAD as App
import FreeCADGui as Gui 

import NURBSinit
import controlpanel

from PySide import QtCore, QtGui
from pivy import coin
import Part
import os
import FACE_D as faced
try:
    import numpy as np
except ImportError:
    print("Please install the required module : numpy")

import random


'''
v=Gui.createViewer(2,"title")

view=v.getViewer(1)
rm=view.getSoRenderManager()
c=rm.getCamera()

c.orientation
c.orientation=App.Rotation(App.Vector(1,1,1),15).Q

c.pointAt(coin.SbVec3f(10,10,10))
c.scaleHeight(3)

'''

import Part



class PartFeature:
    ''' base class Nurbs_for part feature '''

    def __init__(self, obj):
        obj.Proxy = self

# grundmethoden zum sichern

    def attach(self, vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


class ViewProvider:
    ''' view provider class Nurbs_for Tripod'''

    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def onDelete(self, obj, subelements):
        print("on Delete Quadview")
        print(self.obj)
        print(subelements)
        self.obj.Object.Proxy.v.close()
        return True

    def onChanged(self, obj, prop):
        print("onchange", prop)
        if prop == "Visibility" and not self.obj.Visibility:
            obj.Object.Proxy.v.close()
        if prop == "Visibility" and self.obj.Visibility:
            fp = self.obj.Object
            title = fp.Label
            v = Gui.createViewer(4, title)
            for i in range(4):
                v.getViewer(i).setEnabledNaviCube(False)
            updatencontent(v, fp.objs, fp)
            fp.Proxy.v = v


class Nurbs_ViewProviderH2:
    ''' view provider class Nurbs_for Tripod'''

    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def onDelete(self, obj, subelements):
        print("on Delete Quadview")
        print(obj)
        print(subelements)
        obj.Object.Proxy.v.close()
        return True

    def onChanged(self, obj, prop):
        if obj == None:
            return
        print("onchange H2", prop)
        if prop == "Visibility" and not obj.Visibility:
            print("close it")
            try:
                _ = obj.Object.Proxy.v
                obj.Object.Proxy.v.close()
            except:
                pass
        if prop == "Visibility" and obj.Visibility:
            fp = obj.Object
            title = fp.Label
            v = Gui.createViewer(4, title)
            for i in range(4):
                v.getViewer(i).setEnabledNaviCube(False)
            resizeWindows(v, fp)
            # updatencontenth2(v,fp.obja,fp.objb,fp.objs,fp)
            fp.Proxy.v = v


class Nurbs_QuadView(PartFeature):
    def __init__(self, obj, label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyVector", "A Axis", "V00")
        obj.addProperty("App::PropertyFloat", "A Angle", "V00")
        obj.addProperty("App::PropertyInteger", "A DisplayMode", "V00")
        obj.addProperty("App::PropertyInteger", "A OrientationMode", "V00")

        obj.A_Axis = App.Vector(1, 0, 0)
        obj.A_Angle = 90

        obj.addProperty("App::PropertyVector", "B Axis", "V01")
        obj.addProperty("App::PropertyFloat", "B Angle", "V01")
        obj.addProperty("App::PropertyInteger", "B DisplayMode", "V01")
        obj.addProperty("App::PropertyInteger", "B OrientationMode", "V01")

        obj.B_Axis = App.Vector(1, 1, 1)
        obj.B_Angle = 120

        obj.addProperty("App::PropertyVector", "C Axis", "V10")
        obj.addProperty("App::PropertyFloat", "C Angle", "V10")
        obj.addProperty("App::PropertyInteger", "C DisplayMode", "V10")
        obj.addProperty("App::PropertyInteger", "C OrientationMode", "V10")

        obj.addProperty("App::PropertyVector", "D Axis", "V11")
        obj.addProperty("App::PropertyFloat", "D Angle", "V11")
        obj.addProperty("App::PropertyInteger", "D DisplayMode", "V11")
        obj.addProperty("App::PropertyInteger", "D OrientationMode", "V11")

        obj.D_Axis = App.Vector(1, 0, 1)
        obj.D_Angle = 45

        obj.addProperty("App::PropertyBool", "DisplayMode", "Render")
        obj.addProperty("App::PropertyBool", "fitAll", "Render")
        obj.addProperty("App::PropertyLinkList", "objs", "Render")

        if label != None:
            obj.Label = label

    def onChanged(self, fp, prop):

        print("on changed .....", fp.Label, prop)
        if not fp.ViewObject.Visibility:
            return

        try:
            self.v
        except:
            return

        AxisAngle = [
            (App.Vector(1, 1, 1), 120),
            (App.Vector(1, 1, 1), -120),

            (App.Vector(1, 0, 1), 45),
            (App.Vector(1, 0, 1), 60),
            (App.Vector(1, 0, 1), 30),

            (App.Vector(1, 0, 0), 90),
            (App.Vector(1, 0, 0), -90),

            (App.Vector(-1, 0, 0), 90),
            (App.Vector(-1, 0, 0), -90),

        ]

        if prop == "Shape":
            # updatencontent(self.v,fp.objs,fp,False,False)
            dpms = [fp.A_DisplayMode, fp.B_DisplayMode,
                    fp.C_DisplayMode, fp.D_DisplayMode]
            vals = [fp.A_OrientationMode, fp.B_OrientationMode,
                    fp.C_OrientationMode, fp.D_OrientationMode]
            for ix in range(4):
                objs = fp.objs
                view = self.v.getViewer(ix)
                val = vals[ix]
                marker = coin.SoSeparator()
                for objx in objs:
                    print("run ", objx.Label)
                    node = objx.ViewObject.RootNode

                    if fp.DisplayMode:
                        nodeA = node.copy()
                        clds = nodeA.getChildren()
                        s2 = clds[2]
                        s2.whichChild.setValue(0)
                    else:
                        nodeA = node

                    if fp.A_DisplayMode == 0:
                        nodeA = node
                    else:
                        nodeA = node.copy()
                        clds = nodeA.getChildren()
                        s2 = clds[2]
                        s2.whichChild.setValue(dpms[ix])

                    marker.addChild(nodeA)

                c = view.getSoRenderManager().getCamera()
                if val != 0:
                    c.orientation = App.Rotation(
                        AxisAngle[val-1][0], AxisAngle[val-1][1]).Q

                # replace the objects
                sg = view.getSceneGraph()
                sg.removeChild(0)
                sg.addChild(marker)

            return

        if prop.endswith("DisplayMode"):
            w = getattr(fp, prop)
            if w < 0:
                setattr(fp, prop, 0)
            if w > 3:
                setattr(fp, prop, 3)
            updatencontent(self.v, fp.objs, fp, False)
            return

        if prop.endswith("OrientationMode"):
            val = getattr(fp, prop)
            if val >= len(AxisAngle) or val < 0:
                setattr(fp, prop, val % len(AxisAngle))
            val = getattr(fp, prop)
            if val != 0:
                if prop == "A_OrientationMode":
                    fp.A_Axis = AxisAngle[val-1][0]
                    fp.A_Angle = AxisAngle[val-1][1]
                if prop == "B_OrientationMode":
                    fp.B_Axis = AxisAngle[val-1][0]
                    fp.B_Angle = AxisAngle[val-1][1]
                if prop == "C_OrientationMode":
                    fp.C_Axis = AxisAngle[val-1][0]
                    fp.C_Angle = AxisAngle[val-1][1]
                if prop == "D_OrientationMode":
                    fp.D_Axis = AxisAngle[val-1][0]
                    fp.D_Angle = AxisAngle[val-1][1]
            return

        if prop.startswith("A_"):
            c = self.v.getViewer(0).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.A_Axis, fp.A_Angle).Q

            view = self.v.getViewer(0)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("B_"):
            c = self.v.getViewer(1).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.B_Axis, fp.B_Angle).Q

            view = self.v.getViewer(1)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("C_"):
            c = self.v.getViewer(2).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.C_Axis, fp.C_Angle).Q

            view = self.v.getViewer(2)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("D_"):
            c = self.v.getViewer(3).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.D_Axis, fp.D_Angle).Q

            view = self.v.getViewer(3)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if fp.fitAll:
            self.v.fitAll()

    def onDocumentRestored(self, fp):
        print(["onDocumentRestored", str(fp.Label) +
              ": "+str(fp.Proxy.__class__.__name__)])
        fp.ViewObject.Visibility = False
        return
        # +# todo: the view restore does not woprk as expected
        # title=fp.Label
        # v=Gui.createViewer(4,title)
        # updatencontent(v,fp.objs,fp)
        # fp.Proxy.v=v


# ---------------------------

class Nurbs_CreateQuadview:
    """
    Todo : What is the usage of this class?
    """

    def Activated(self):

        objs = Gui.Selection.getSelection()

        labels = [obj.Label for obj in objs]
        title = ', '.join(labels)

        v = Gui.createViewer(4, title)
        for i in range(4):
            v.getViewer(i).setEnabledNaviCube(False)

        a = App.ActiveDocument.addObject("Part::FeaturePython", "MyQuadView")
        Nurbs_QuadView(a, "QuadView for " + title)
        ViewProvider(a.ViewObject)

        updatencontent(v, objs, a)

        a.Proxy.v = v
        a.objs = objs

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap': NURBSinit.ICONS_PATH+'workspacequad.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_CreateQuadview"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs_CreateQuadview", _tooltip)}

Gui.addCommand("Nurbs_CreateQuadview", Nurbs_CreateQuadview())


def updatencontent(viewer, objs, fp, clearSel=True, fit=True):

    print("update content", fp, fp.Label)

    try:
        view = viewer.getViewer(0)
    except:
        title = fp.Label
        viewer = Gui.createViewer(4, title)
        for i in range(4):
            viewer.getViewer(i).setEnabledNaviCube(False)

        fp.Proxy.v = viewer

    v = viewer
    view = v.getViewer(0)
    rm = view.getSoRenderManager()
    print("######################")
    rm.setCamera(coin.SoOrthographicCamera())

    marker = coin.SoSeparator()

    for objx in objs:
        try:
            objgx = objx.Group
        except:
            objgx = [objx]
        for objx in objgx:
            print("run ", objx.Label)
            node = objx.ViewObject.RootNode

            if fp.A_DisplayMode == 0:
                nodeA = node
            else:
                nodeA = node.copy()
                clds = nodeA.getChildren()
                s2 = clds[2]
                s2.whichChild.setValue(fp.A_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.A_Axis, fp.A_Angle).Q

    reg = view.getSoRenderManager().getViewportRegion()
    marker = view.getSoRenderManager().getSceneGraph()
    c.viewAll(marker, reg)

    # ------------------------------------

    view = v.getViewer(1)
    marker = coin.SoSeparator()
    for objx in objs:
        try:
            objgx = objx.Group
        except:
            objgx = [objx]
        for objx in objgx:
            node = objx.ViewObject.RootNode

            if fp.B_DisplayMode == 0:
                nodeA = node
            else:
                nodeA = node.copy()
                clds = nodeA.getChildren()
                s2 = clds[2]
                s2.whichChild.setValue(fp.B_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.B_Axis, fp.B_Angle).Q

    # ------------------------------------

    view = v.getViewer(2)
    marker = coin.SoSeparator()
    for objx in objs:
        try:
            objgx = objx.Group
        except:
            objgx = [objx]
        for objx in objgx:
            node = objx.ViewObject.RootNode

            if fp.C_DisplayMode == 0:
                nodeA = node
            else:
                nodeA = node.copy()
                clds = nodeA.getChildren()
                s2 = clds[2]
                s2.whichChild.setValue(fp.C_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.C_Axis, fp.C_Angle).Q

    # ------------------------------------

    view = v.getViewer(3)
    marker = coin.SoSeparator()
    for objx in objs:
        try:
            objgx = objx.Group
        except:
            objgx = [objx]
        for objx in objgx:

            node = objx.ViewObject.RootNode

            if fp.D_DisplayMode == 0:
                nodeA = node
            else:
                nodeA = node.copy()
                clds = nodeA.getChildren()
                s2 = clds[2]
                s2.whichChild.setValue(fp.D_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.D_Axis, fp.D_Angle).Q

    # ------------------------------------

    if fit:
        v.fitAll()

    if clearSel:
        Gui.Selection.clearSelection()


#
# two horizontal windows ...
#

def XXupdatencontenth2(viewer, obja, objb):
    # +# todo: update like quadview

    v = viewer

    node = obja.ViewObject.RootNode

    view = v.getViewer(0)
    view.setSceneGraph(node)

    view = v.getViewer(1)
    marker = coin.SoSeparator()
    t = coin.SoTransform()
    t.rotation.setValue(coin.SbVec3f((1, 0, 0)), -np.pi/2)
    marker.addChild(t)
    marker.addChild(node)
    view.setSceneGraph(marker)

    node = objb.ViewObject.RootNode

    view = v.getViewer(2)
    marker = coin.SoSeparator()
    t = coin.SoTransform()
    t.rotation.setValue(coin.SbVec3f((1, 0, 0)), -np.pi/2)
    marker.addChild(t)
    marker.addChild(node)
    view.setSceneGraph(marker)

    view = v.getViewer(3)
    marker = coin.SoSeparator()
    marker.addChild(node)
    view.setSceneGraph(marker)

    v.fitAll()
    v.viewTop()


def updatencontenth2(viewer, obja, objb, objs, fp, clearSel=True, fit=True):

    print("update content", fp, fp.Label)

    try:
        view = viewer.getViewer(0)
    except:
        title = fp.Label
        viewer = Gui.createViewer(4, title)
        for i in range(4):
            viewer.getViewer(i).setEnabledNaviCube(False)

        fp.Proxy.v = viewer

    v = viewer
    view = v.getViewer(0)
    rm = view.getSoRenderManager()
    print("######################")
    rm.setCamera(coin.SoOrthographicCamera())

    marker = coin.SoSeparator()

    for objx in objs+[obja]:
        print("run 0", objx.Label)
        node = objx.ViewObject.RootNode

        if fp.A_DisplayMode == 0:
            nodeA = node
        else:
            nodeA = node.copy()
            clds = nodeA.getChildren()
            s2 = clds[2]
            s2.whichChild.setValue(fp.A_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.A_Axis, fp.A_Angle).Q

    reg = view.getSoRenderManager().getViewportRegion()
    marker = view.getSoRenderManager().getSceneGraph()
    c.viewAll(marker, reg)

    # ------------------------------------

    view = v.getViewer(1)
    marker = coin.SoSeparator()
    for objx in objs + [objb]:
        print("run 1", objx.Label)
        node = objx.ViewObject.RootNode

        if fp.B_DisplayMode == 0:
            nodeA = node
        else:
            nodeA = node.copy()
            clds = nodeA.getChildren()
            s2 = clds[2]
            s2.whichChild.setValue(fp.B_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.B_Axis, fp.B_Angle).Q

    # ------------------------------------

    view = v.getViewer(2)
    marker = coin.SoSeparator()
    for objx in objs + [objb]:
        print("run 2", objx.Label)
        node = objx.ViewObject.RootNode

        if fp.C_DisplayMode == 0:
            nodeA = node
        else:
            nodeA = node.copy()
            clds = nodeA.getChildren()
            s2 = clds[2]
            s2.whichChild.setValue(fp.C_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.C_Axis, fp.C_Angle).Q

    # ------------------------------------

    view = v.getViewer(3)
    marker = coin.SoSeparator()
    for objx in objs + [obja]:
        print("run 3", objx.Label)
        node = objx.ViewObject.RootNode

        if fp.D_DisplayMode == 0:
            nodeA = node
        else:
            nodeA = node.copy()
            clds = nodeA.getChildren()
            s2 = clds[2]
            s2.whichChild.setValue(fp.D_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c = view.getSoRenderManager().getCamera()
    c.orientation = App.Rotation(fp.D_Axis, fp.D_Angle).Q

    # ------------------------------------

    if fit:
        v.fitAll()

    if clearSel:
        Gui.Selection.clearSelection()


class Nurbs_ViewH2(PartFeature):
    def __init__(self, obj, label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyVector", "A Axis", "V00")
        obj.addProperty("App::PropertyFloat", "A Angle", "V00")
        obj.addProperty("App::PropertyInteger", "A DisplayMode", "V00")
        obj.addProperty("App::PropertyInteger", "A OrientationMode", "V00")

        obj.A_Axis = App.Vector(1, 0, 0)
        obj.A_Angle = 90

        obj.addProperty("App::PropertyVector", "B Axis", "V01")
        obj.addProperty("App::PropertyFloat", "B Angle", "V01")
        obj.addProperty("App::PropertyInteger", "B DisplayMode", "V01")
        obj.addProperty("App::PropertyInteger", "B OrientationMode", "V01")

        obj.B_Axis = App.Vector(1, 1, 1)
        obj.B_Angle = 120

        obj.addProperty("App::PropertyVector", "C Axis", "V10")
        obj.addProperty("App::PropertyFloat", "C Angle", "V10")
        obj.addProperty("App::PropertyInteger", "C DisplayMode", "V10")
        obj.addProperty("App::PropertyInteger", "C OrientationMode", "V10")

        obj.addProperty("App::PropertyVector", "D Axis", "V11")
        obj.addProperty("App::PropertyFloat", "D Angle", "V11")
        obj.addProperty("App::PropertyInteger", "D DisplayMode", "V11")
        obj.addProperty("App::PropertyInteger", "D OrientationMode", "V11")

        obj.D_Axis = App.Vector(1, 0, 1)
        obj.D_Angle = 45

        obj.addProperty("App::PropertyBool", "DisplayMode", "Render")
        obj.addProperty("App::PropertyBool", "fitAll", "Render")
        obj.addProperty("App::PropertyLinkList", "objs", "Render")

        obj.addProperty("App::PropertyLink", "obja", "Render")
        obj.addProperty("App::PropertyLink", "objb", "Render")

        if label != None:
            obj.Label = label

    def onChanged(self, fp, prop):

        print("on changed .....", fp.Label, prop)
#        print ("deanctivated"
#        return

        if not fp.ViewObject.Visibility:
            return

        try:
            self.v
        except:
            return

        AxisAngle = [
            (App.Vector(1, 1, 1), 120),
            (App.Vector(1, 1, 1), -120),

            (App.Vector(1, 0, 1), 45),
            (App.Vector(1, 0, 1), 60),
            (App.Vector(1, 0, 1), 30),

            (App.Vector(1, 0, 0), 90),
            (App.Vector(1, 0, 0), -90),

            (App.Vector(-1, 0, 0), 90),
            (App.Vector(-1, 0, 0), -90),

        ]

        if prop == "Shape":
            # updatencontent(self.v,fp.objs,fp,False,False)
            dpms = [fp.A_DisplayMode, fp.B_DisplayMode,
                    fp.C_DisplayMode, fp.D_DisplayMode]
            vals = [fp.A_OrientationMode, fp.B_OrientationMode,
                    fp.C_OrientationMode, fp.D_OrientationMode]
            for ix in range(4):
                objs = fp.objs
                view = self.v.getViewer(ix)
                val = vals[ix]
                marker = coin.SoSeparator()
                for objx in objs:
                    print("run ", objx.Label)
                    node = objx.ViewObject.RootNode

                    if fp.DisplayMode:
                        nodeA = node.copy()
                        clds = nodeA.getChildren()
                        s2 = clds[2]
                        s2.whichChild.setValue(0)
                    else:
                        nodeA = node

                    if fp.A_DisplayMode == 0:
                        nodeA = node
                    else:
                        nodeA = node.copy()
                        clds = nodeA.getChildren()
                        s2 = clds[2]
                        s2.whichChild.setValue(dpms[ix])

                    marker.addChild(nodeA)

                c = view.getSoRenderManager().getCamera()
                if val != 0:
                    c.orientation = App.Rotation(
                        AxisAngle[val-1][0], AxisAngle[val-1][1]).Q

                # replace the objects
                sg = view.getSceneGraph()
                sg.removeChild(0)
                sg.addChild(marker)

            return

        if prop.endswith("DisplayMode"):
            w = getattr(fp, prop)
            if w < 0:
                setattr(fp, prop, 0)
            if w > 3:
                setattr(fp, prop, 3)
            updatencontenth2(self.v, fp.obja, fp.objb, fp.objs, fp, False)
            return

        if prop.endswith("OrientationMode"):
            val = getattr(fp, prop)
            if val >= len(AxisAngle) or val < 0:
                setattr(fp, prop, val % len(AxisAngle))
            val = getattr(fp, prop)
            if val != 0:
                if prop == "A_OrientationMode":
                    fp.A_Axis = AxisAngle[val-1][0]
                    fp.A_Angle = AxisAngle[val-1][1]
                if prop == "B_OrientationMode":
                    fp.B_Axis = AxisAngle[val-1][0]
                    fp.B_Angle = AxisAngle[val-1][1]
                if prop == "C_OrientationMode":
                    fp.C_Axis = AxisAngle[val-1][0]
                    fp.C_Angle = AxisAngle[val-1][1]
                if prop == "D_OrientationMode":
                    fp.D_Axis = AxisAngle[val-1][0]
                    fp.D_Angle = AxisAngle[val-1][1]
            return

        if prop.startswith("A_"):
            c = self.v.getViewer(0).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.A_Axis, fp.A_Angle).Q

            view = self.v.getViewer(0)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("B_"):
            c = self.v.getViewer(1).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.B_Axis, fp.B_Angle).Q

            view = self.v.getViewer(1)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("C_"):
            c = self.v.getViewer(2).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.C_Axis, fp.C_Angle).Q

            view = self.v.getViewer(2)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("D_"):
            c = self.v.getViewer(3).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.D_Axis, fp.D_Angle).Q

            view = self.v.getViewer(3)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if fp.fitAll:
            self.v.fitAll()

    def onDocumentRestored(self, fp):
        print(["onDocumentRestored", str(fp.Label) +
              ": "+str(fp.Proxy.__class__.__name__)])
        fp.ViewObject.Visibility = False
        return
        # +# todo: the view restore does not woprk as expected


def resizeWindows(v, a):

    title = "Horizontal views for "+a.obja.Label+" and "+a.objb.Label

    mw = Gui.getMainWindow()
    mdiarea = mw.findChild(QtGui.QMdiArea)

    sws = mdiarea.subWindowList()

    print(title)
    print("windows ...")
    for i, w2 in enumerate(sws):
        print("XX--!"+str(w2.windowTitle()))

    for i, w2 in enumerate(sws):
        print("!!"+str(w2.windowTitle()))
        if w2.windowTitle() == title:

            #            print w2.children()
            va = w2.children()[3]

#            print va.children()
            sp = va.children()[2]

            spa = sp.children()[0]
            spa.setSizes([10, 0])

            spa = sp.children()[1]
            spa.setSizes([10, 0])

            print("update content h2 -- start ")
            updatencontenth2(v, a.obja, a.objb, a.objs, a, False)
            print("update content h2 -- done")
            # return


class Nurbs_CreateH2():

    def Activated(self):
        s=Gui.Selection.getSelection()
        if (len(s) <3):
            # An object must be sele()
            errMessage = "Select 3 objects to use Extrude Face"
            faced.getInfo(s).errorDialog(errMessage)
            return
        obja = Gui.Selection.getSelection()[0]
        objb = Gui.Selection.getSelection()[1]
        objs = Gui.Selection.getSelection()[2:]

        title = "Horizontal views for "+obja.Label+" and "+objb.Label

#        v=Gui.createViewer(4,title)

        a = App.ActiveDocument.addObject("Part::FeaturePython", "MyViewH2")
        Nurbs_ViewH2(a, title)
        Nurbs_ViewProviderH2(a.ViewObject)

#        a.Proxy.v=v
        a.obja = obja
        a.objb = objb
        a.objs = objs

        a.ViewObject.Visibility = False

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_CreateH2")
        return {'Pixmap': NURBSinit.ICONS_PATH+'workspace.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_CreateH2"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs createH2", _tooltip)}
Gui.addCommand("Nurbs_CreateH2", Nurbs_CreateH2())

# ------------------------------------------------------


def mkshadow(sgg, lis):

    rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr = "HeadlightIntensity"
    v = rGrp.GetInt(atr)

    # set headlight on
    rGrp.SetInt(atr, 100)

    # or off
    rGrp.SetInt(atr, 0)

    # myCustomNode=Gui.ActiveDocument.ActiveView.getSceneGraph()

    sggs = sgg.getChildren()
    cs = [c.copy() for c in sggs]
    for i in range(len(cs)):
        sgg.removeChild(0)

    sotype = coin.SoType.fromName("ShadowGroup")
    sg = sotype.createInstance()
    sg.getTypeId().getName()
    sg.quality = 1

    sgg.insertChild(sg, 0)
    ss = sg

    ff = 0.5

    if 0:
        l = coin.SoSpotLight()
        l.direction.setValue(coin.SbVec3f(-20, 10, -300))
        l.color.setValue(coin.SbColor(ff*random.random(), ff *
                         random.random(), ff*random.random()))
        l.location.setValue(coin.SbVec3f(0, 0, 300))
        l.cutOffAngle.setValue(0.4)
        l.dropOffRate.setValue(0.)
        ss.insertChild(l, 0)

        l = coin.SoSpotLight()
        l.direction.setValue(coin.SbVec3f(0, 0, -300))
        l.color.setValue(coin.SbColor(ff*random.random(), ff *
                         random.random(), ff*random.random()))
        l.location.setValue(coin.SbVec3f(0, 0, 300))
        l.cutOffAngle.setValue(0.4)
        l.dropOffRate.setValue(0.)
        ss.insertChild(l, 0)

        l = coin.SoSpotLight()
        l.direction.setValue(coin.SbVec3f(10, 20, -300))
        l.color.setValue(coin.SbColor(1, 0, 0))
        l.color.setValue(coin.SbColor(ff*random.random(), ff *
                         random.random(), ff*random.random()))
        l.location.setValue(coin.SbVec3f(50, 10, 300))
        l.cutOffAngle.setValue(.35)
        l.dropOffRate.setValue(0.)
        ss.insertChild(l, 0)

    else:
        for lig in lis:
            ss.insertChild(lig, 0)

    ll = len(cs)
    for i in range(len(cs)):
        sotype = coin.SoType.fromName("SoShadowStyle")
        inst = sotype.createInstance()
        print(inst.getTypeId().getName())  # => ShadowStyle)
        inst.style = 3
        ss.insertChild(inst, 0)
        ss.addChild(cs[ll-1-i])

    Gui.SendMsgToActiveView("ViewFit")

    print("children von sg")
    ssc = sg.getChildren()
    for c in ssc:
        print(c)

# \cond


# -------------------------------------

class Nurbs_DarkRoom(PartFeature):
    obj=label=None
    def __init__(self, obj, label=None):
        self.obj=obj
        self.label=label
        self.fp=None
        PartFeature.__init__(self, obj)

        self.obj.addProperty("App::PropertyBool", "On", "Render")

        self.obj.addProperty("App::PropertyVector", "A Axis", "V00")
        self.obj.addProperty("App::PropertyFloat", "A Angle", "V00")
        self.obj.addProperty("App::PropertyInteger", "A DisplayMode", "V00")
        self.obj.addProperty("App::PropertyInteger", "A OrientationMode", "V00")

        self.obj.A_Axis = App.Vector(1, 0, 1)
        self.obj.A_Angle = 60

        self.obj.addProperty("App::PropertyVector", "B Axis", "V01")
        self.obj.addProperty("App::PropertyFloat", "B Angle", "V01")
        self.obj.addProperty("App::PropertyInteger", "B DisplayMode", "V01")
        self.obj.addProperty("App::PropertyInteger", "B OrientationMode", "V01")
        
        self.obj.B_Axis = App.Vector(1, 1, 1)
        self.obj.B_Angle = 120

        self.obj.addProperty("App::PropertyVector", "C Axis", "V10")
        self.obj.addProperty("App::PropertyFloat", "C Angle", "V10")
        self.obj.addProperty("App::PropertyInteger", "C DisplayMode", "V10")
        self.obj.addProperty("App::PropertyInteger", "C OrientationMode", "V10")

        self.obj.addProperty("App::PropertyVector", "D Axis", "V11")
        self.obj.addProperty("App::PropertyFloat", "D Angle", "V11")
        self.obj.addProperty("App::PropertyInteger", "D DisplayMode", "V11")
        self.obj.addProperty("App::PropertyInteger", "D OrientationMode", "V11")

        self.obj.D_Axis = App.Vector(1, 0, 1)
        self.obj.D_Angle = 45

        self.obj.addProperty("App::PropertyBool", "DisplayMode", "Render")
        self.obj.addProperty("App::PropertyBool", "fitAll", "Render")
        self.obj.addProperty("App::PropertyLinkList", "objs", "Render")

        self.obj.addProperty("App::PropertyLink", "obja", "Render")
        self.obj.addProperty("App::PropertyLink", "objb", "Render")

        if label != None:
            self.obj.Label = label

    def onChanged(self, fp, prop):
        self.fp=fp
        if not self.fp.On:
            return

        print("on changed .....", fp.Label, prop)

        if self.fp == None:
            return
        if not self.fp.ViewObject.Visibility:
            return

        try:
            self.v
        except:
            return

        AxisAngle = [
            (App.Vector(1, 1, 1), 120),
            (App.Vector(1, 1, 1), -120),

            (App.Vector(1, 0, 1), 45),
            (App.Vector(1, 0, 1), 60),
            (App.Vector(1, 0, 1), 30),

            (App.Vector(1, 0, 0), 90),
            (App.Vector(1, 0, 0), -90),

            (App.Vector(-1, 0, 0), 90),
            (App.Vector(-1, 0, 0), -90),

        ]

        if prop == "Shape" or prop == "Group":
            dpms = [self.fp.A_DisplayMode,     self.fp.B_DisplayMode,
                    self.fp.C_DisplayMode,     self.fp.D_DisplayMode]
            vals = [self.fp.A_OrientationMode, self.fp.B_OrientationMode,
                    self.fp.C_OrientationMode, self.fp.D_OrientationMode]
            for ix in [0]:
                objs = self.fp.objs
                view = self.v.getViewer(ix)
                val = vals[ix]
                marker = coin.SoSeparator()
                for objx in objs+[self.fp.obja]:
                    print("run ", objx.Label)
                    node = objx.ViewObject.RootNode

                    if self.fp.DisplayMode:
                        nodeA = node.copy()
                        clds = nodeA.getChildren()
                        s2 = clds[2]
                        s2.whichChild.setValue(0)
                    else:
                        nodeA = node

                    if self.fp.A_DisplayMode == 0:
                        nodeA = node
                    else:
                        nodeA = node.copy()
                        clds = nodeA.getChildren()
                        s2 = clds[2]
                        s2.whichChild.setValue(dpms[ix])

                    marker.addChild(nodeA)

                c = view.getSoRenderManager().getCamera()
                if val != 0:
                    c.orientation = App.Rotation(
                        AxisAngle[val-1][0], AxisAngle[val-1][1]).Q
                else:
                    c.orientation = App.Rotation(fp.A_Axis, fp.A_Angle).Q

                sg = view.getSceneGraph()
                sg.removeChild(1)
                sg.removeChild(0)

                # hier die lichter einfuegen
                lis = []
                for ob in self.fp.Group:
                    # break

                    print("!!", ob, ob.Label, ob.on)

                    try:
                        ob.mode
                    except:
                        continue

                    print("verarbeitung", ob.mode, ob.on)
                    if ob.on and ob.ViewObject.Visibility:

                        if ob.mode == "DirectionalLight":
                            continue
                            # ignore dirlights
                            l = coin.SoDirectionalLight()
                            # marker.insertChild(l,0)
                            #lis += [l]

                        if ob.mode == "SpotLight":
                            l = coin.SoSpotLight()
                            l.cutOffAngle.setValue(0.4)
                            l.dropOffRate.setValue(0.)
                            l.location.setValue(coin.SbVec3f(
                                ob.location.x, ob.location.y, ob.location.z,))

                            l.direction.setValue(coin.SbVec3f(
                                ob.direction.x, ob.direction.y, ob.direction.z,))
                            l.color.setValue(coin.SbColor(
                                ob.color[0], ob.color[1], ob.color[2]))
                        # marker.insertChild(l,0)

                            lis += [l]

                sg.addChild(marker)
                print("makeshadow ..........!")
                mkshadow(marker, lis)
                print("------------------done-----------------")

                for ob in self.fp.Group:

                    try:
                        ob.mode
                    except:
                        continue

                    print("verarbeitung", ob.mode, ob.on)
                    if ob.on and ob.ViewObject.Visibility:

                        if ob.mode == "DirectionalLight":

                            l = coin.SoDirectionalLight()
                            l.direction.setValue(coin.SbVec3f(-1, 1, 0))
                            l.color.setValue(coin.SbColor(1, 0, 0))
                            l.direction.setValue(coin.SbVec3f(
                                ob.direction.x, ob.direction.y, ob.direction.z,))
                            l.color.setValue(coin.SbColor(
                                ob.color[0], ob.color[1], ob.color[2]))

                            marker.insertChild(l, 0)

                        if ob.mode == "PointLight":
                            l = coin.SoPointLight()
                            l.location.setValue(coin.SbVec3f(
                                ob.location.x, ob.location.y, ob.location.z,))
                            l.color.setValue(coin.SbColor(
                                ob.color[0], ob.color[1], ob.color[2]))
                            marker.insertChild(l, 0)

            return

        if prop.endswith("DisplayMode"):
            w = getattr(self.fp, prop)
            if w < 0:
                setattr(self.fp, prop, 0)
            if w > 3:
                setattr(self.fp, prop, 3)
            # updatencontenth2(self.v,fp.obja,fp.objb,fp.objs,fp,False)
            return

        if prop.endswith("OrientationMode"):
            val = getattr(self.fp, prop)
            if val >= len(AxisAngle) or val < 0:
                setattr(self.fp, prop, val % len(AxisAngle))
            val = getattr(self.fp, prop)
            if val != 0:
                if prop == "A_OrientationMode":
                    self.fp.A_Axis = AxisAngle[val-1][0]
                    self.fp.A_Angle = AxisAngle[val-1][1]
                if prop == "B_OrientationMode":
                    self.fp.B_Axis = AxisAngle[val-1][0]
                    self.fp.B_Angle = AxisAngle[val-1][1]
                if prop == "C_OrientationMode":
                    self.fp.C_Axis = AxisAngle[val-1][0]
                    self.fp.C_Angle = AxisAngle[val-1][1]
                if prop == "D_OrientationMode":
                    self.fp.D_Axis = AxisAngle[val-1][0]
                    self.fp.D_Angle = AxisAngle[val-1][1]
            return

        if prop.startswith("A_"):
            c = self.v.getViewer(0).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(self.fp.A_Axis, self.fp.A_Angle).Q

            view = self.v.getViewer(0)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("B_"):
            c = self.v.getViewer(1).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(self.fp.B_Axis, self.fp.B_Angle).Q

            view = self.v.getViewer(1)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("C_"):
            c = self.v.getViewer(2).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.C_Axis, fp.C_Angle).Q

            view = self.v.getViewer(2)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if prop.startswith("D_"):
            c = self.v.getViewer(3).getSoRenderManager().getCamera()
            c.orientation = App.Rotation(fp.D_Axis, fp.D_Angle).Q

            view = self.v.getViewer(3)
            reg = view.getSoRenderManager().getViewportRegion()
            marker = view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker, reg)

        if self.fp.fitAll:
            self.v.fitAll()

    def onDocumentRestored(self, fp):
        self.fp=fp
        print(["onDocumentRestored", str(fp.Label) +
              ": "+str(self.fp.Proxy.__class__.__name__)])
        self.fp.ViewObject.Visibility = False

    def execute(self, fp):
        self.onChanged(fp, "Shape")


class Nurbs_ViewProviderDR:
    ''' view provider class Nurbs_for dark room'''
    fp=Object=None
    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj
        self.fp=obj.Object

    def onDelete(self, obj, subelements):
        print("on Delete Quadview")
        print(obj)
        print(subelements)
        obj.Object.Proxy.v.close()
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "HeadlightIntensity"
        rGrp.SetInt(atr, 100)
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "BackgroundColor"
        rGrp.SetUnsigned(atr, 1437270015)
        return True

    def onChanged(self, obj, prop):
        if obj == None:
            return
        print("onchange H2", prop)
        if prop == "Visibility" and not obj.Visibility:
            rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
            atr = "HeadlightIntensity"
            rGrp.SetInt(atr, 100)
            rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
            atr = "BackgroundColor"
            rGrp.SetUnsigned(atr, 1437270015)

            print("close it")
            print(obj.Object.Proxy.v)
            App.v = obj.Object.Proxy.v
            obj.Object.Proxy.v.close()
            try:
                _ = obj.Object.Proxy.v
                obj.Object.Proxy.v.hide()
            except:
                pass
        if prop == "Visibility" and obj.Visibility:
            self.fp = obj.Object
            title = self.fp.Label
            v = Gui.createViewer(2, title)
            for i in range(2):
                v.getViewer(i).setEnabledNaviCube(False)

            setsizeDR(title)

            self.fp.Proxy.v = v
            self.fp.Proxy.onChanged(self.fp, "Shape")

            rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
            atr = "HeadlightIntensity"
            rGrp.SetInt(atr, 0)
            rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
            atr = "BackgroundColor"
            rGrp.SetUnsigned(atr, 0)
            v.fitAll()

#TODO:This is not correct .. I don't understand the code
def setsizeDR(title):

    mw = Gui.getMainWindow()
    mdiarea = mw.findChild(QtGui.QMdiArea)
    sws = mdiarea.subWindowList()
    print(sws)

    for i, w2 in enumerate(sws):
        print(w2.windowTitle())
        if w2.windowTitle() == title:
            print (len(w2.children()))
            child_=w2.children()
            print("...........")
            print (child_)
            va=child_[3]
            print((va.children()))
           # spa = va.children()[2]
           # spa.setSizes([10, 0])
            #va = w2.children()[3]        #->>>>>>FIXME
            #spa = va.children()[2]       #->>>>>>FIXME
            #spa.setSizes([10, 0])


class Nurbs_CreateDarkRoom:
    configureVal=[]
    def __init__(self, configureVal=[1, 1, 1, 1, 1, ]):
        self.configureVal=configureVal
        
    def Activated(self):

        # the superstar
        obja = Gui.Selection.getSelection()[0]
        # and the set
        objs = Gui.Selection.getSelection()[1:]

        title = "Darkroom for "+obja.Label

        v = Gui.createViewer(2, title)
        for i in range(2):
            v.getViewer(i).setEnabledNaviCube(False)

        setsizeDR(title)

        a = App.ActiveDocument.addObject(
            "App::DocumentObjectGroupPython", "MyDarkRoom")
        Nurbs_DarkRoom(a, title)
        Nurbs_ViewProviderDR(a.ViewObject)

        a.Proxy.v = v

        a.obja = obja
        a.objs = objs

        # add some lights to start the party ...

        # with shadows dir-lights do not work inside the shadow group
        if self.configureVal[0]:
            la = Nurbs_createlight("DirectionalLight").Activated()
            la.location = App.Vector(-100, -100, 0)
            la.direction = la.location*(-1)
            a.addObject(la)

        if self.configureVal[1]:
            la = Nurbs_createlight('DirectionalLight').Activated()
            la.location = App.Vector(200, -100, 0)
            la.direction = la.location*(-1)
            la.color = (0.3, 0., 0.)
            a.addObject(la)

        if self.configureVal[2]:
            la = Nurbs_createlight("SpotLight").Activated()
            la.mode = "SpotLight"
            la.location = App.Vector(10, -20, 400)
            la.direction = App.Vector(0, 0, -1)
            la.color = (0.3, 0., 1.)
            a.addObject(la)

        if self.configureVal[3]:
            la = Nurbs_createlight("PointLight").Activated()
            la.mode = "PointLight"
            la.location = App.Vector(10, -20, 400)
            la.direction = App.Vector(0, 0, -1)
            la.color = (0.3, 0., 1.)
            a.addObject(la)

        # the shadow light test env

        if self.configureVal[4]:

            ff = 0.1
            la = Nurbs_createlight("SpotLight").Activated()
            la.mode = "SpotLight"
            la.location = App.Vector(0, 0, 300)
            la.direction = App.Vector(-20, 10, -300)
            la.color = (0.3, 0., 1.)
            la.color = (0.9+ff*random.random(), ff *
                        random.random(), ff*random.random())
            a.addObject(la)

            la = Nurbs_createlight("SpotLight").Activated()
            la.mode = "SpotLight"
            la.location = App.Vector(0, 0, 300)
            la.direction = App.Vector(0, 0, -300)
            la.color = (0.3, 0., 1.)
            la.color = (ff*random.random(), 0.9+ff *
                        random.random(), ff*random.random())
            a.addObject(la)

            la = Nurbs_createlight("SpotLight").Activated()
            la.mode = "SpotLight"
            la.location = App.Vector(50, 10, 300)
            la.direction = App.Vector(10, 20, -300)
            la.color = (0.3, 0., 1.)
            la.color = (ff*random.random(), ff *
                        random.random(), 0.9+ff*random.random())
            a.addObject(la)

        # dark the environment
        a.On = True
        a.Proxy.onChanged(a, "Shape")
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "HeadlightIntensity"

        rGrp.SetInt(atr, 0)
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "BackgroundColor"
        rGrp.SetUnsigned(atr, 0)
        v.fitAll()

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("NurbsCreateDarkRoom")
        return {'Pixmap': NURBSinit.ICONS_PATH+'workspace.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsCreateDarkRoom"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs CreateDarkRoom", _tooltip)}

Gui.addCommand("Nurbs_CreateDarkRoom", Nurbs_CreateDarkRoom())


class Nurbs_ViewProviderL:
    ''' view provider class Nurbs_for the Light node'''

    def __init__(self, obj):
        obj.Proxy = self
        self.Object = obj

    def onDelete(self, obj, subelements):
        print("on Delete ")
        print(obj)
        return True

    def onChanged(self, obj, prop):
        print("onchange", prop)
        obj.Object.touch()
        App.ActiveDocument.recompute()


class Nurbs_Light(PartFeature):
    ''' a parametric light node'''

    def __init__(self, obj, label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyVector", "direction",
                        ).direction = App.Vector(-1, -1, -1)
        obj.addProperty("App::PropertyVector", "location",
                        ).location = App.Vector(100, 100, 100)
        obj.addProperty("App::PropertyColor", "color",).color = (0.2, 0.2, 0.)
        obj.addProperty("App::PropertyEnumeration", "mode",).mode = [
            'DirectionalLight', 'SpotLight', 'PointLight']
        obj.addProperty("App::PropertyBool", "on",).on = True

    def execute(self, fp):
        print("execute done")


class Nurbs_createlight:
    def __init__(self, name='SpotLight'):
        self.name=name
    def Activated(self):
        a = App.ActiveDocument.addObject("Part::FeaturePython", self.name)
        Nurbs_Light(a)
        a.mode = self.name
        Nurbs_ViewProviderL(a.ViewObject)
        return a

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbscreatelight")
        return {'Pixmap': NURBSinit.ICONS_PATH+'workspace2h.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbscreatelight"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs createlight", _tooltip)}


Gui.addCommand("Nurbs_createlight", Nurbs_createlight())


class Nurbs_LightON:
    def Activated(self):
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "HeadlightIntensity"
        rGrp.SetInt(atr, 100)
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "BackgroundColor"
        rGrp.SetUnsigned(atr, 1437270015)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap': NURBSinit.ICONS_PATH+'light_on.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbslightON"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs lightON", _tooltip)}


Gui.addCommand("Nurbs_LightON", Nurbs_LightON())


class Nurbs_LightOFF():
    def Activated(self):
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "HeadlightIntensity"
        rGrp.SetInt(atr, 0)
        rGrp = App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr = "BackgroundColor"
        rGrp.SetUnsigned(atr, 0)

    def GetResources(self):
        
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Nurbs_LightOFF")
        return {'Pixmap': NURBSinit.ICONS_PATH+'light_off.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "Nurbs_LightOFF"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456 Nurbs LightOFF", _tooltip)}

Gui.addCommand("Nurbs_LightOFF", Nurbs_LightOFF())
