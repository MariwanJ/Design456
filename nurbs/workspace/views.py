# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- special view support
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD as App
import FreeCADGui as Gui




from PySide import QtCore,QtGui
from pivy import coin
import numpy as np
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


Gui=FreeCADGui
import Part

class PartFeature:
    ''' base class for part feature '''
    def __init__(self, obj):
        obj.Proxy = self

# grundmethoden zum sichern

    def attach(self,vobj):
        self.Object = vobj.Object

    def claimChildren(self):
        return self.Object.Group

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

class ViewProvider:
    ''' view provider class for Tripod'''
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

    def onDelete(self, obj, subelements):
        print ("on Delete Quadview")
        print (obj)
        print (subelements)
        obj.Object.Proxy.v.close()
        return True

    def onChanged(self, obj, prop):
            print ("onchange",prop)
            if prop=="Visibility" and not obj.Visibility:
                obj.Object.Proxy.v.close()
            if prop=="Visibility" and obj.Visibility:
                fp=obj.Object
                title=fp.Label
                v=Gui.createViewer(4,title)
                for i in range(4):
                    v.getViewer(i).setEnabledNaviCube(False)
                updatencontent(v,fp.objs,fp)
                fp.Proxy.v=v

class ViewProviderH2:
    ''' view provider class for Tripod'''
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

    def onDelete(self, obj, subelements):
        print ("on Delete Quadview")
        print (obj)
        print (subelements)
        obj.Object.Proxy.v.close()
        return True

    def onChanged(self, obj, prop):
            if obj==None: return
            print ("onchange H2",prop)
            if prop=="Visibility" and not obj.Visibility:
                print ("close it")
                try: 
                    _=obj.Object.Proxy.v  
                    obj.Object.Proxy.v.close()
                except: 
                    pass
            if prop=="Visibility" and obj.Visibility:
                fp=obj.Object
                title=fp.Label
                v=Gui.createViewer(4,title)
                for i in range(4):
                    v.getViewer(i).setEnabledNaviCube(False)
                resizeWindows(v,fp)
                # updatencontenth2(v,fp.obja,fp.objb,fp.objs,fp)
                fp.Proxy.v=v




class QuadView(PartFeature):
    def __init__(self, obj,label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyVector","A Axis","V00")
        obj.addProperty("App::PropertyFloat","A Angle","V00")
        obj.addProperty("App::PropertyInteger","A DisplayMode","V00")
        obj.addProperty("App::PropertyInteger","A OrientationMode","V00")

        obj.A_Axis=App.Vector(1,0,0)
        obj.A_Angle=90

        obj.addProperty("App::PropertyVector","B Axis","V01")
        obj.addProperty("App::PropertyFloat","B Angle","V01")
        obj.addProperty("App::PropertyInteger","B DisplayMode","V01")
        obj.addProperty("App::PropertyInteger","B OrientationMode","V01")

        obj.B_Axis=App.Vector(1,1,1)
        obj.B_Angle=120

        obj.addProperty("App::PropertyVector","C Axis","V10")
        obj.addProperty("App::PropertyFloat","C Angle","V10")
        obj.addProperty("App::PropertyInteger","C DisplayMode","V10")
        obj.addProperty("App::PropertyInteger","C OrientationMode","V10")


        obj.addProperty("App::PropertyVector","D Axis","V11")
        obj.addProperty("App::PropertyFloat","D Angle","V11")
        obj.addProperty("App::PropertyInteger","D DisplayMode","V11")
        obj.addProperty("App::PropertyInteger","D OrientationMode","V11")

        obj.D_Axis=App.Vector(1,0,1)
        obj.D_Angle=45


        obj.addProperty("App::PropertyBool","DisplayMode","Render")
        obj.addProperty("App::PropertyBool","fitAll","Render")
        obj.addProperty("App::PropertyLinkList","objs","Render")

        if label != None:
            obj.Label = label


    def onChanged(self, fp, prop):

        print ("on changed .....",fp.Label,prop)
        if not fp.ViewObject.Visibility: return

        try: self.v
        except: return

        AxisAngle=[
                (App.Vector(1,1,1),120),
                (App.Vector(1,1,1),-120),
                
                (App.Vector(1,0,1),45),
                (App.Vector(1,0,1),60),
                (App.Vector(1,0,1),30),
                
                (App.Vector(1,0,0),90),
                (App.Vector(1,0,0),-90),
                
                (App.Vector(-1,0,0),90),
                (App.Vector(-1,0,0),-90),
                
            ]


        if prop=="Shape": 
            # updatencontent(self.v,fp.objs,fp,False,False)
            dpms=[fp.A_DisplayMode,fp.B_DisplayMode,fp.C_DisplayMode,fp.D_DisplayMode]
            vals=[fp.A_OrientationMode,fp.B_OrientationMode,fp.C_OrientationMode,fp.D_OrientationMode]
            for ix in range(4):
                objs=fp.objs
                view=self.v.getViewer(ix)
                val=vals[ix]
                marker = coin.SoSeparator()
                for objx in objs:
                    print ("run ",objx.Label)
                    node= objx.ViewObject.RootNode

                    if fp.DisplayMode:
                        nodeA=node.copy()
                        clds=nodeA.getChildren()
                        s2=clds[2]
                        s2.whichChild.setValue(0)
                    else:
                        nodeA=node

                    if fp.A_DisplayMode==0:
                        nodeA=node
                    else:
                        nodeA=node.copy()
                        clds=nodeA.getChildren()
                        s2=clds[2]
                        s2.whichChild.setValue(dpms[ix])

                    marker.addChild(nodeA)

                c=view.getSoRenderManager().getCamera()
                if val !=0:
                    c.orientation=App.Rotation(    AxisAngle[val-1][0],AxisAngle[val-1][1]).Q

                #replace the objects
                sg=view.getSceneGraph()
                sg.removeChild(0)
                sg.addChild(marker)

            return


        if prop.endswith("DisplayMode"):
            w=getattr(fp,prop)
            if w<0: setattr(fp,prop,0)
            if w>3: setattr(fp,prop,3)
            updatencontent(self.v,fp.objs,fp,False)
            return

        if prop.endswith("OrientationMode"):
            val=getattr(fp,prop)
            if val>=len(AxisAngle)or val<0: setattr(fp,prop,val%len(AxisAngle))
            val=getattr(fp,prop)
            if val!=0:
                if prop=="A_OrientationMode":
                    fp.A_Axis=AxisAngle[val-1][0]
                    fp.A_Angle=AxisAngle[val-1][1]
                if prop=="B_OrientationMode":
                    fp.B_Axis=AxisAngle[val-1][0]
                    fp.B_Angle=AxisAngle[val-1][1]
                if prop=="C_OrientationMode":
                    fp.C_Axis=AxisAngle[val-1][0]
                    fp.C_Angle=AxisAngle[val-1][1]
                if prop=="D_OrientationMode":
                    fp.D_Axis=AxisAngle[val-1][0]
                    fp.D_Angle=AxisAngle[val-1][1]
            return


        if prop.startswith("A_"):
            c=self.v.getViewer(0).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.A_Axis,fp.A_Angle).Q

            view=self.v.getViewer(0)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("B_"):
            c=self.v.getViewer(1).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.B_Axis,fp.B_Angle).Q

            view=self.v.getViewer(1)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("C_"):
            c=self.v.getViewer(2).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.C_Axis,fp.C_Angle).Q

            view=self.v.getViewer(2)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("D_"):
            c=self.v.getViewer(3).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.D_Axis,fp.D_Angle).Q

            view=self.v.getViewer(3)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if fp.fitAll:
            self.v.fitAll()


    def onDocumentRestored(self, fp):
        print(["onDocumentRestored",str(fp.Label)+ ": "+str(fp.Proxy.__class__.__name__)])
        fp.ViewObject.Visibility=False
        return
        #+# todo: the view restore does not woprk as expected
        #title=fp.Label
        #v=Gui.createViewer(4,title)
        #updatencontent(v,fp.objs,fp)
        #fp.Proxy.v=v




#---------------------------



def createquadview():

    objs=Gui.Selection.getSelection()

    labels=[obj.Label for obj in objs]
    title=', '.join(labels)

    v=Gui.createViewer(4,title)
    for i in range(4):
        v.getViewer(i).setEnabledNaviCube(False)


    a=App.ActiveDocument.addObject("Part::FeaturePython","MyQuadView")
    QuadView(a,"QuadView for "+ title )
    ViewProvider(a.ViewObject)

    updatencontent(v,objs,a)

    a.Proxy.v=v
    a.objs=objs


def updatencontent(viewer,objs,fp,clearSel=True,fit=True):

    print ("update content",fp,fp.Label)

    try:
        view=viewer.getViewer(0)
    except:
        title=fp.Label
        viewer=Gui.createViewer(4,title)
        for i in range(4):
            viewer.getViewer(i).setEnabledNaviCube(False)

        fp.Proxy.v=viewer

    v=viewer
    view=v.getViewer(0)
    rm=view.getSoRenderManager()
    print ("######################")
    rm.setCamera( coin.SoOrthographicCamera())

    marker = coin.SoSeparator()

    for objx in objs:
        try: objgx=objx.Group
        except: objgx=[objx]
        for objx in objgx:
            print ("run ",objx.Label)
            node= objx.ViewObject.RootNode

            if fp.A_DisplayMode==0:
                nodeA=node
            else:
                nodeA=node.copy()
                clds=nodeA.getChildren()
                s2=clds[2]
                s2.whichChild.setValue(fp.A_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.A_Axis,fp.A_Angle).Q

    reg=view.getSoRenderManager().getViewportRegion()
    marker=view.getSoRenderManager().getSceneGraph()
    c.viewAll(marker,reg)

    #------------------------------------

    view=v.getViewer(1)
    marker = coin.SoSeparator()
    for objx in objs:
        try: objgx=objx.Group
        except: objgx=[objx]
        for objx in objgx:
            node= objx.ViewObject.RootNode

            if fp.B_DisplayMode==0:
                nodeA=node
            else:
                nodeA=node.copy()
                clds=nodeA.getChildren()
                s2=clds[2]
                s2.whichChild.setValue(fp.B_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.B_Axis,fp.B_Angle).Q

    #------------------------------------

    view=v.getViewer(2)
    marker = coin.SoSeparator()
    for objx in objs:
        try: objgx=objx.Group
        except: objgx=[objx]
        for objx in objgx:
            node= objx.ViewObject.RootNode

            if fp.C_DisplayMode==0:
                nodeA=node
            else:
                nodeA=node.copy()
                clds=nodeA.getChildren()
                s2=clds[2]
                s2.whichChild.setValue(fp.C_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.C_Axis,fp.C_Angle).Q

    #------------------------------------

    view=v.getViewer(3)
    marker = coin.SoSeparator()
    for objx in objs:
        try: objgx=objx.Group
        except: objgx=[objx]
        for objx in objgx:

            node= objx.ViewObject.RootNode

            if fp.D_DisplayMode==0:
                nodeA=node
            else:
                nodeA=node.copy()
                clds=nodeA.getChildren()
                s2=clds[2]
                s2.whichChild.setValue(fp.D_DisplayMode)

            marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.D_Axis,fp.D_Angle).Q

    #------------------------------------

    if fit:
        v.fitAll()

    if clearSel:
        Gui.Selection.clearSelection()


#
# two horizontal windows ...
#

def XXupdatencontenth2(viewer,obja,objb):
    #+# todo: update like quadview

    v=viewer

    node= obja.ViewObject.RootNode

    view=v.getViewer(0)
    view.setSceneGraph(node)

    view=v.getViewer(1)
    marker = coin.SoSeparator()
    t = coin.SoTransform()
    t.rotation.setValue(coin.SbVec3f((1,0,0)),-np.pi/2)
    marker.addChild(t)
    marker.addChild(node)
    view.setSceneGraph(marker)

    node=objb.ViewObject.RootNode

    view=v.getViewer(2)
    marker = coin.SoSeparator()
    t = coin.SoTransform()
    t.rotation.setValue(coin.SbVec3f((1,0,0)),-np.pi/2)
    marker.addChild(t)
    marker.addChild(node)
    view.setSceneGraph(marker)

    view=v.getViewer(3)
    marker = coin.SoSeparator()
    marker.addChild(node)
    view.setSceneGraph(marker)

    v.fitAll()
    v.viewTop()



def updatencontenth2(viewer,obja,objb,objs,fp,clearSel=True,fit=True):

    print ("update content",fp,fp.Label)

    try:
        view=viewer.getViewer(0)
    except:
        title=fp.Label
        viewer=Gui.createViewer(4,title)
        for i in range(4):
            viewer.getViewer(i).setEnabledNaviCube(False)

        fp.Proxy.v=viewer

    v=viewer
    view=v.getViewer(0)
    rm=view.getSoRenderManager()
    print ("######################")
    rm.setCamera( coin.SoOrthographicCamera())

    marker = coin.SoSeparator()

    for objx in objs+[obja]:
        print ("run 0",objx.Label)
        node= objx.ViewObject.RootNode

        if fp.A_DisplayMode==0:
            nodeA=node
        else:
            nodeA=node.copy()
            clds=nodeA.getChildren()
            s2=clds[2]
            s2.whichChild.setValue(fp.A_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.A_Axis,fp.A_Angle).Q

    reg=view.getSoRenderManager().getViewportRegion()
    marker=view.getSoRenderManager().getSceneGraph()
    c.viewAll(marker,reg)

    #------------------------------------

    view=v.getViewer(1)
    marker = coin.SoSeparator()
    for objx in objs +[objb]:
        print ("run 1",objx.Label)
        node= objx.ViewObject.RootNode

        if fp.B_DisplayMode==0:
            nodeA=node
        else:
            nodeA=node.copy()
            clds=nodeA.getChildren()
            s2=clds[2]
            s2.whichChild.setValue(fp.B_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.B_Axis,fp.B_Angle).Q

    #------------------------------------

    view=v.getViewer(2)
    marker = coin.SoSeparator()
    for objx in objs + [objb]:
        print ("run 2",objx.Label)
        node= objx.ViewObject.RootNode

        if fp.C_DisplayMode==0:
            nodeA=node
        else:
            nodeA=node.copy()
            clds=nodeA.getChildren()
            s2=clds[2]
            s2.whichChild.setValue(fp.C_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.C_Axis,fp.C_Angle).Q

    #------------------------------------

    view=v.getViewer(3)
    marker = coin.SoSeparator()
    for objx in objs +[obja]:
        print ("run 3",objx.Label)
        node= objx.ViewObject.RootNode

        if fp.D_DisplayMode==0:
            nodeA=node
        else:
            nodeA=node.copy()
            clds=nodeA.getChildren()
            s2=clds[2]
            s2.whichChild.setValue(fp.D_DisplayMode)

        marker.addChild(nodeA)

    view.setSceneGraph(marker)

    c=view.getSoRenderManager().getCamera()
    c.orientation=App.Rotation(fp.D_Axis,fp.D_Angle).Q

    #------------------------------------

    if fit:
        v.fitAll()

    if clearSel:
        Gui.Selection.clearSelection()




class ViewH2(PartFeature):
    def __init__(self, obj,label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyVector","A Axis","V00")
        obj.addProperty("App::PropertyFloat","A Angle","V00")
        obj.addProperty("App::PropertyInteger","A DisplayMode","V00")
        obj.addProperty("App::PropertyInteger","A OrientationMode","V00")

        obj.A_Axis=App.Vector(1,0,0)
        obj.A_Angle=90

        obj.addProperty("App::PropertyVector","B Axis","V01")
        obj.addProperty("App::PropertyFloat","B Angle","V01")
        obj.addProperty("App::PropertyInteger","B DisplayMode","V01")
        obj.addProperty("App::PropertyInteger","B OrientationMode","V01")

        obj.B_Axis=App.Vector(1,1,1)
        obj.B_Angle=120

        obj.addProperty("App::PropertyVector","C Axis","V10")
        obj.addProperty("App::PropertyFloat","C Angle","V10")
        obj.addProperty("App::PropertyInteger","C DisplayMode","V10")
        obj.addProperty("App::PropertyInteger","C OrientationMode","V10")


        obj.addProperty("App::PropertyVector","D Axis","V11")
        obj.addProperty("App::PropertyFloat","D Angle","V11")
        obj.addProperty("App::PropertyInteger","D DisplayMode","V11")
        obj.addProperty("App::PropertyInteger","D OrientationMode","V11")

        obj.D_Axis=App.Vector(1,0,1)
        obj.D_Angle=45


        obj.addProperty("App::PropertyBool","DisplayMode","Render")
        obj.addProperty("App::PropertyBool","fitAll","Render")
        obj.addProperty("App::PropertyLinkList","objs","Render")

        obj.addProperty("App::PropertyLink","obja","Render")
        obj.addProperty("App::PropertyLink","objb","Render")

        if label != None:
            obj.Label = label


    def onChanged(self, fp, prop):

        print ("on changed .....",fp.Label,prop)
#        print ("deanctivated"
#        return

        if not fp.ViewObject.Visibility: return

        try: self.v
        except: return

        AxisAngle=[
                (App.Vector(1,1,1),120),
                (App.Vector(1,1,1),-120),
                
                (App.Vector(1,0,1),45),
                (App.Vector(1,0,1),60),
                (App.Vector(1,0,1),30),
                
                (App.Vector(1,0,0),90),
                (App.Vector(1,0,0),-90),
                
                (App.Vector(-1,0,0),90),
                (App.Vector(-1,0,0),-90),
                
            ]


        if prop=="Shape": 
            # updatencontent(self.v,fp.objs,fp,False,False)
            dpms=[fp.A_DisplayMode,fp.B_DisplayMode,fp.C_DisplayMode,fp.D_DisplayMode]
            vals=[fp.A_OrientationMode,fp.B_OrientationMode,fp.C_OrientationMode,fp.D_OrientationMode]
            for ix in range(4):
                objs=fp.objs
                view=self.v.getViewer(ix)
                val=vals[ix]
                marker = coin.SoSeparator()
                for objx in objs:
                    print ("run ",objx.Label)
                    node= objx.ViewObject.RootNode

                    if fp.DisplayMode:
                        nodeA=node.copy()
                        clds=nodeA.getChildren()
                        s2=clds[2]
                        s2.whichChild.setValue(0)
                    else:
                        nodeA=node

                    if fp.A_DisplayMode==0:
                        nodeA=node
                    else:
                        nodeA=node.copy()
                        clds=nodeA.getChildren()
                        s2=clds[2]
                        s2.whichChild.setValue(dpms[ix])

                    marker.addChild(nodeA)

                c=view.getSoRenderManager().getCamera()
                if val !=0:
                    c.orientation=App.Rotation(    AxisAngle[val-1][0],AxisAngle[val-1][1]).Q

                #replace the objects
                sg=view.getSceneGraph()
                sg.removeChild(0)
                sg.addChild(marker)

            return


        if prop.endswith("DisplayMode"):
            w=getattr(fp,prop)
            if w<0: setattr(fp,prop,0)
            if w>3: setattr(fp,prop,3)
            updatencontenth2(self.v,fp.obja,fp.objb,fp.objs,fp,False)
            return

        if prop.endswith("OrientationMode"):
            val=getattr(fp,prop)
            if val>=len(AxisAngle)or val<0: setattr(fp,prop,val%len(AxisAngle))
            val=getattr(fp,prop)
            if val!=0:
                if prop=="A_OrientationMode":
                    fp.A_Axis=AxisAngle[val-1][0]
                    fp.A_Angle=AxisAngle[val-1][1]
                if prop=="B_OrientationMode":
                    fp.B_Axis=AxisAngle[val-1][0]
                    fp.B_Angle=AxisAngle[val-1][1]
                if prop=="C_OrientationMode":
                    fp.C_Axis=AxisAngle[val-1][0]
                    fp.C_Angle=AxisAngle[val-1][1]
                if prop=="D_OrientationMode":
                    fp.D_Axis=AxisAngle[val-1][0]
                    fp.D_Angle=AxisAngle[val-1][1]
            return


        if prop.startswith("A_"):
            c=self.v.getViewer(0).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.A_Axis,fp.A_Angle).Q

            view=self.v.getViewer(0)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("B_"):
            c=self.v.getViewer(1).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.B_Axis,fp.B_Angle).Q

            view=self.v.getViewer(1)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("C_"):
            c=self.v.getViewer(2).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.C_Axis,fp.C_Angle).Q

            view=self.v.getViewer(2)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("D_"):
            c=self.v.getViewer(3).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.D_Axis,fp.D_Angle).Q

            view=self.v.getViewer(3)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if fp.fitAll:
            self.v.fitAll()


    def onDocumentRestored(self, fp):
        print(["onDocumentRestored",str(fp.Label)+ ": "+str(fp.Proxy.__class__.__name__)])
        fp.ViewObject.Visibility=False
        return
        #+# todo: the view restore does not woprk as expected


def resizeWindows(v,a):

    title="Horizontal views for "+a.obja.Label+" and "+a.objb.Label

    mw=FreeCADGui.getMainWindow()
    mdiarea=mw.findChild(QtGui.QMdiArea)

    sws=mdiarea.subWindowList()

    print( title)
    print ("windows ...")
    for i,w2 in enumerate(sws):
        print ("XX--!"+str(w2.windowTitle()))

    for i,w2 in enumerate(sws):
        print ("!!"+str(w2.windowTitle()))
        if  w2.windowTitle()==title:


#            print w2.children()
            va=w2.children()[3]

#            print va.children()
            sp=va.children()[2]

            spa=sp.children()[0]
            spa.setSizes([10,0])

            spa=sp.children()[1]
            spa.setSizes([10,0])

            print ("update content h2 -- start ")
            updatencontenth2(v,a.obja,a.objb,a.objs,a,False)
            print ("update content h2 -- done")
            #return



def createh2():

    obja=Gui.Selection.getSelection()[0]
    objb=Gui.Selection.getSelection()[1]
    objs=Gui.Selection.getSelection()[2:]

    title="Horizontal views for "+obja.Label+" and "+objb.Label

#    v=Gui.createViewer(4,title)

    a=App.ActiveDocument.addObject("Part::FeaturePython","MyViewH2")
    ViewH2(a,title )
    ViewProviderH2(a.ViewObject)

#    a.Proxy.v=v
    a.obja=obja
    a.objb=objb
    a.objs=objs

    a.ViewObject.Visibility=False


#------------------------------------------------------
def mkshadow(sgg,lis):

    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="HeadlightIntensity"
    v=rGrp.GetInt(atr)

    #set headlight on
    rGrp.SetInt(atr,100)

    # or off
    rGrp.SetInt(atr,0)

    # myCustomNode=Gui.ActiveDocument.ActiveView.getSceneGraph()


    sggs=sgg.getChildren()
    cs=[c.copy() for c in sggs]
    for i in range(len(cs)):
        sgg.removeChild(0)


    sotype=coin.SoType.fromName("ShadowGroup")
    sg=sotype.createInstance()
    sg.getTypeId().getName()
    sg.quality=1

    sgg.insertChild(sg,0)
    ss=sg


    ff=0.5

    if 0:
        l=coin.SoSpotLight()
        l.direction.setValue(coin.SbVec3f(-20,10,-300))
        l.color.setValue(coin.SbColor(ff*random.random(),ff*random.random(),ff*random.random()))
        l.location.setValue(coin.SbVec3f(0,0,300))
        l.cutOffAngle.setValue(0.4)
        l.dropOffRate.setValue(0.)
        ss.insertChild(l,0)

        l=coin.SoSpotLight()
        l.direction.setValue(coin.SbVec3f(0,0,-300))
        l.color.setValue(coin.SbColor(ff*random.random(),ff*random.random(),ff*random.random()))
        l.location.setValue(coin.SbVec3f(0,0,300))
        l.cutOffAngle.setValue(0.4)
        l.dropOffRate.setValue(0.)
        ss.insertChild(l,0)


        l=coin.SoSpotLight()
        l.direction.setValue(coin.SbVec3f(10,20,-300))
        l.color.setValue(coin.SbColor(1,0,0))
        l.color.setValue(coin.SbColor(ff*random.random(),ff*random.random(),ff*random.random()))
        l.location.setValue(coin.SbVec3f(50,10,300))
        l.cutOffAngle.setValue(.35)
        l.dropOffRate.setValue(0.)
        ss.insertChild(l,0)

    else:
        for lig in lis:
            ss.insertChild(lig,0)

    ll=len(cs)
    for i in range(len(cs)):
        sotype=coin.SoType.fromName("SoShadowStyle")
        inst=sotype.createInstance()
        print (inst.getTypeId().getName() )# => ShadowStyle)
        inst.style=3
        ss.insertChild(inst,0)
        ss.addChild(cs[ll-1-i])


    Gui.SendMsgToActiveView("ViewFit")


    print ("children von sg")
    ssc=sg.getChildren()
    for c in ssc:
        print (c)




#-------------------------------------

class DarkRoom(PartFeature):
    def __init__(self, obj,label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyBool","On","Render")

        obj.addProperty("App::PropertyVector","A Axis","V00")
        obj.addProperty("App::PropertyFloat","A Angle","V00")
        obj.addProperty("App::PropertyInteger","A DisplayMode","V00")
        obj.addProperty("App::PropertyInteger","A OrientationMode","V00")

        obj.A_Axis=App.Vector(1,0,1)
        obj.A_Angle=60

        obj.addProperty("App::PropertyVector","B Axis","V01")
        obj.addProperty("App::PropertyFloat","B Angle","V01")
        obj.addProperty("App::PropertyInteger","B DisplayMode","V01")
        obj.addProperty("App::PropertyInteger","B OrientationMode","V01")

        obj.B_Axis=App.Vector(1,1,1)
        obj.B_Angle=120

        obj.addProperty("App::PropertyVector","C Axis","V10")
        obj.addProperty("App::PropertyFloat","C Angle","V10")
        obj.addProperty("App::PropertyInteger","C DisplayMode","V10")
        obj.addProperty("App::PropertyInteger","C OrientationMode","V10")


        obj.addProperty("App::PropertyVector","D Axis","V11")
        obj.addProperty("App::PropertyFloat","D Angle","V11")
        obj.addProperty("App::PropertyInteger","D DisplayMode","V11")
        obj.addProperty("App::PropertyInteger","D OrientationMode","V11")

        obj.D_Axis=App.Vector(1,0,1)
        obj.D_Angle=45


        obj.addProperty("App::PropertyBool","DisplayMode","Render")
        obj.addProperty("App::PropertyBool","fitAll","Render")
        obj.addProperty("App::PropertyLinkList","objs","Render")

        obj.addProperty("App::PropertyLink","obja","Render")
        obj.addProperty("App::PropertyLink","objb","Render")
        
        

        if label != None:
            obj.Label = label


    def onChanged(self, fp, prop):
        if not fp.On: return

        print ("on changed .....",fp.Label,prop)

        if fp == None: return
        if not fp.ViewObject.Visibility: return

        try: self.v
        except: return

        AxisAngle=[
                (App.Vector(1,1,1),120),
                (App.Vector(1,1,1),-120),
                
                (App.Vector(1,0,1),45),
                (App.Vector(1,0,1),60),
                (App.Vector(1,0,1),30),
                
                (App.Vector(1,0,0),90),
                (App.Vector(1,0,0),-90),
                
                (App.Vector(-1,0,0),90),
                (App.Vector(-1,0,0),-90),
                
            ]


        if prop=="Shape" or prop=="Group": 
            dpms=[fp.A_DisplayMode,fp.B_DisplayMode,fp.C_DisplayMode,fp.D_DisplayMode]
            vals=[fp.A_OrientationMode,fp.B_OrientationMode,fp.C_OrientationMode,fp.D_OrientationMode]
            for ix in [0]:
                objs=fp.objs
                view=self.v.getViewer(ix)
                val=vals[ix]
                marker = coin.SoSeparator()
                for objx in objs+[fp.obja]:
                    print ("run ",objx.Label)
                    node= objx.ViewObject.RootNode

                    if fp.DisplayMode:
                        nodeA=node.copy()
                        clds=nodeA.getChildren()
                        s2=clds[2]
                        s2.whichChild.setValue(0)
                    else:
                        nodeA=node

                    if fp.A_DisplayMode==0:
                        nodeA=node
                    else:
                        nodeA=node.copy()
                        clds=nodeA.getChildren()
                        s2=clds[2]
                        s2.whichChild.setValue(dpms[ix])

                    marker.addChild(nodeA)

                c=view.getSoRenderManager().getCamera()
                if val != 0:
                    c.orientation=App.Rotation(    AxisAngle[val-1][0],AxisAngle[val-1][1]).Q
                else:
                    c.orientation=App.Rotation(    fp.A_Axis,fp.A_Angle).Q
                    
                sg=view.getSceneGraph()
                sg.removeChild(1)
                sg.removeChild(0)

                # hier die lichter einfuegen
                lis=[]
                for ob in fp.Group:
                    #break

                    print ("!!",ob,ob.Label,ob.on)

                    try: ob.mode
                    except: continue

                    print ("verarbeitung",ob.mode,ob.on)
                    if ob.on and ob.ViewObject.Visibility:

                        if ob.mode=="DirectionalLight":
                            continue
                            # ignore dirlights
                            l=coin.SoDirectionalLight()
                            #marker.insertChild(l,0)
                            #lis += [l]

                        if ob.mode=="SpotLight":
                            l=coin.SoSpotLight()
                            l.cutOffAngle.setValue(0.4)
                            l.dropOffRate.setValue(0.)
                            l.location.setValue(coin.SbVec3f(ob.location.x,ob.location.y,ob.location.z,))

                            l.direction.setValue(coin.SbVec3f(ob.direction.x,ob.direction.y,ob.direction.z,))
                            l.color.setValue(coin.SbColor(ob.color[0],ob.color[1],ob.color[2]))
                        #marker.insertChild(l,0)

                            lis += [l]




                sg.addChild(marker)
                print ("makeshadow ..........!")
                mkshadow(marker,lis)
                print ("------------------done-----------------")


                for ob in fp.Group:

                    try: ob.mode
                    except: continue

                    print ("verarbeitung",ob.mode,ob.on)
                    if ob.on and ob.ViewObject.Visibility:

                        if ob.mode=="DirectionalLight":

                            l=coin.SoDirectionalLight()
                            l.direction.setValue(coin.SbVec3f(-1,1,0))
                            l.color.setValue(coin.SbColor(1,0,0))
                            l.direction.setValue(coin.SbVec3f(ob.direction.x,ob.direction.y,ob.direction.z,))
                            l.color.setValue(coin.SbColor(ob.color[0],ob.color[1],ob.color[2]))

                            marker.insertChild(l,0)

                        if ob.mode=="PointLight":
                            l=coin.SoPointLight()
                            l.location.setValue(coin.SbVec3f(ob.location.x,ob.location.y,ob.location.z,))
                            l.color.setValue(coin.SbColor(ob.color[0],ob.color[1],ob.color[2]))
                            marker.insertChild(l,0)

            return


        if prop.endswith("DisplayMode"):
            w=getattr(fp,prop)
            if w<0: setattr(fp,prop,0)
            if w>3: setattr(fp,prop,3)
            #updatencontenth2(self.v,fp.obja,fp.objb,fp.objs,fp,False)
            return


        if prop.endswith("OrientationMode"):
            val=getattr(fp,prop)
            if val>=len(AxisAngle)or val<0: setattr(fp,prop,val%len(AxisAngle))
            val=getattr(fp,prop)
            if val!=0:
                if prop=="A_OrientationMode":
                    fp.A_Axis=AxisAngle[val-1][0]
                    fp.A_Angle=AxisAngle[val-1][1]
                if prop=="B_OrientationMode":
                    fp.B_Axis=AxisAngle[val-1][0]
                    fp.B_Angle=AxisAngle[val-1][1]
                if prop=="C_OrientationMode":
                    fp.C_Axis=AxisAngle[val-1][0]
                    fp.C_Angle=AxisAngle[val-1][1]
                if prop=="D_OrientationMode":
                    fp.D_Axis=AxisAngle[val-1][0]
                    fp.D_Angle=AxisAngle[val-1][1]
            return


        if prop.startswith("A_"):
            c=self.v.getViewer(0).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.A_Axis,fp.A_Angle).Q

            view=self.v.getViewer(0)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("B_"):
            c=self.v.getViewer(1).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.B_Axis,fp.B_Angle).Q

            view=self.v.getViewer(1)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("C_"):
            c=self.v.getViewer(2).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.C_Axis,fp.C_Angle).Q

            view=self.v.getViewer(2)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if prop.startswith("D_"):
            c=self.v.getViewer(3).getSoRenderManager().getCamera()
            c.orientation=App.Rotation(fp.D_Axis,fp.D_Angle).Q

            view=self.v.getViewer(3)
            reg=view.getSoRenderManager().getViewportRegion()
            marker=view.getSoRenderManager().getSceneGraph()
            c.viewAll(marker,reg)

        if fp.fitAll:
            self.v.fitAll()






    def onDocumentRestored(self, fp):
        print(["onDocumentRestored",str(fp.Label)+ ": "+str(fp.Proxy.__class__.__name__)])
        fp.ViewObject.Visibility=False


    def execute(self, fp):
        self.onChanged(fp,"Shape")



class ViewProviderDR:
    ''' view provider class for dark room'''
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

    def onDelete(self, obj, subelements):
        print ("on Delete Quadview")
        print (obj)
        print (subelements)
        obj.Object.Proxy.v.close()
        rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr="HeadlightIntensity"
        rGrp.SetInt(atr,100)
        rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
        atr="BackgroundColor"
        rGrp.SetUnsigned(atr,1437270015)

        return True

    def onChanged(self, obj, prop):
            if obj==None: return
            print ("onchange H2",prop)
            if prop=="Visibility" and not obj.Visibility:
                rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
                atr="HeadlightIntensity"
                rGrp.SetInt(atr,100)
                rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
                atr="BackgroundColor"
                rGrp.SetUnsigned(atr,1437270015)


                print ("close it")
                print (obj.Object.Proxy.v )
                App.v=obj.Object.Proxy.v 
                obj.Object.Proxy.v.close()
                try: 
                    _=obj.Object.Proxy.v  
                    obj.Object.Proxy.v.hide()
                except: 
                    pass
            if prop=="Visibility" and obj.Visibility:
                fp=obj.Object
                title=fp.Label
                v=Gui.createViewer(2,title)
                for i in range(2):
                    v.getViewer(i).setEnabledNaviCube(False)

                setsizeDR(title)
                
                fp.Proxy.v=v
                fp.Proxy.onChanged(fp,"Shape")

                rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
                atr="HeadlightIntensity"
                rGrp.SetInt(atr,0)
                rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
                atr="BackgroundColor"
                rGrp.SetUnsigned(atr,0)
                v.fitAll()
                



def setsizeDR(title):

    mw=FreeCADGui.getMainWindow()
    mdiarea=mw.findChild(QtGui.QMdiArea)
    sws=mdiarea.subWindowList()

    for i,w2 in enumerate(sws):
        if  w2.windowTitle()==title:
            va=w2.children()[3]
            spa=va.children()[2]
            spa.setSizes([10,0])




def createdarkroom():

    # the superstar
    obja=Gui.Selection.getSelection()[0]
    # and the set
    objs=Gui.Selection.getSelection()[1:]

    title="Darkroom for "+obja.Label

    v=Gui.createViewer(2,title)
    for i in range(2):
        v.getViewer(i).setEnabledNaviCube(False)

    setsizeDR(title)


    a=App.ActiveDocument.addObject("App::DocumentObjectGroupPython","MyDarkRoom")
    DarkRoom(a,title )
    ViewProviderDR(a.ViewObject)

    a.Proxy.v=v

    a.obja=obja
    a.objs=objs

    # add some lights to start the party ...
    
    # with shadows dir-lights do not work inside the shadow group
    if 1:
        la=createlight('DirectionalLight')
        la.location=App.Vector(-100,-100,0)
        la.direction=la.location*(-1) 
        a.addObject(la)

    if 1:
        la=createlight('DirectionalLight')
        la.location=App.Vector(200,-100,0)
        la.direction=la.location*(-1) 
        la.color=(0.3,0.,0.)
        a.addObject(la)

    if 1:
        la=createlight("SpotLight")
        la.mode="SpotLight"
        la.location=App.Vector(10,-20,400)
        la.direction=App.Vector(0,0,-1) 
        la.color=(0.3,0.,1.)
        a.addObject(la)

    if 1:
        la=createlight("PointLight")
        la.mode="PointLight"
        la.location=App.Vector(10,-20,400)
        la.direction=App.Vector(0,0,-1) 
        la.color=(0.3,0.,1.)
        a.addObject(la)


    # the shadow light test env

    if 1:

        ff=0.1
        la=createlight("SpotLight")
        la.mode="SpotLight"
        la.location=App.Vector(0,0,300)
        la.direction=App.Vector(-20,10,-300) 
        la.color=(0.3,0.,1.)
        la.color=(0.9+ff*random.random(),ff*random.random(),ff*random.random())
        a.addObject(la)

        la=createlight("SpotLight")
        la.mode="SpotLight"
        la.location=App.Vector(0,0,300)
        la.direction=App.Vector(0,0,-300) 
        la.color=(0.3,0.,1.)
        la.color=(ff*random.random(),0.9+ff*random.random(),ff*random.random())
        a.addObject(la)

        la=createlight("SpotLight")
        la.mode="SpotLight"
        la.location=App.Vector(50,10,300)
        la.direction=App.Vector(10,20,-300) 
        la.color=(0.3,0.,1.)
        la.color=(ff*random.random(),ff*random.random(),0.9+ff*random.random())
        a.addObject(la)






    # dark the environment
    a.On=True
    a.Proxy.onChanged(a,"Shape")
    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="HeadlightIntensity"
    rGrp.SetInt(atr,0)
    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="BackgroundColor"
    rGrp.SetUnsigned(atr,0)

    v.fitAll()



class ViewProviderL:
    ''' view provider class for the Light node'''
    def __init__(self, obj):
        obj.Proxy = self
        self.Object=obj

    def onDelete(self, obj, subelements):
        print ("on Delete ")
        print (obj)
        return True

    def onChanged(self, obj, prop):
            print ("onchange",prop)
            obj.Object.touch()
            App.ActiveDocument.recompute()



class Light(PartFeature):
    ''' a parametric light node''' 
    def __init__(self, obj,label=None):
        PartFeature.__init__(self, obj)

        obj.addProperty("App::PropertyVector","direction",).direction=App.Vector(-1,-1,-1)
        obj.addProperty("App::PropertyVector","location",).location=App.Vector(100,100,100)
        obj.addProperty("App::PropertyColor","color",).color=(0.2,0.2,0.)
        obj.addProperty("App::PropertyEnumeration","mode",).mode=['DirectionalLight','SpotLight','PointLight']
        obj.addProperty("App::PropertyBool","on",).on=True

    def execute(self,fp):
        print ("execute done")


def createlight(name="SpotLight"):

    a=App.ActiveDocument.addObject("Part::FeaturePython",name)
    Light(a)
    a.mode=name
    ViewProviderL(a.ViewObject)    
    return a



def lightOn():
    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="HeadlightIntensity"
    rGrp.SetInt(atr,100)
    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="BackgroundColor"
    rGrp.SetUnsigned(atr,1437270015)

def lightOff():
    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="HeadlightIntensity"
    rGrp.SetInt(atr,0)
    rGrp=App.ParamGet('User parameter:BaseApp/Preferences/View')
    atr="BackgroundColor"
    rGrp.SetUnsigned(atr,0)
