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
from draftutils.translate import translate  # for translate
import Design456Init
import FACE_D as faced
import DraftGeomUtils
import math
import BOPTools.SplitFeatures

__updated__ = '2022-09-15 22:17:26'


#TODO : FIXME: 
# Fence

class ViewProviderFence:

    obj_name = "Fence"

    def __init__(self, obj, obj_name):
        self.obj_name = ViewProviderFence.obj_name
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
    
    def __getstate__(self):
        return None
    
    def __setstate__(self):
        return None
    
    def getIcon(self):
        return (Design456Init.ICON_PATH + 'Fence.svg')

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

class BaseFence:
    """ Fence shape based on several parameters
    """
    Placement=App.Placement()
    def __init__(self, obj,
                 _width=30.00,
                 _height=10.00,
                 _thickness=2,
                 _sections=4,
                 _connectionWidth=1.00,
                 _sectionWidth=2.00,
                 _bottomDistance=1.00,
                 _topDistance=6.00,
                 _sharpLength=1.00,
                 _waveDepth=3.0,
                 _netDistance=0.5,
                 _netThickness=0.80,
                 _type=4,
                 ):

        obj.addProperty("App::PropertyLength", "Width", "Fence",
                        "Width of the Fence").Width = _width
                        
        obj.addProperty("App::PropertyLength", "Height", "Fence",
                        "Height of the Fence").Height = _height

        obj.addProperty("App::PropertyLength", "Thickness", "Fence",
                        "Thickness of the Fence").Thickness = _thickness

        obj.addProperty("App::PropertyLength", "netThickness", "Fence",
                        "Thickness of the Fence").netThickness = _netThickness #This is a percentage of the total thickness
        
        obj.addProperty("App::PropertyLength", "ConnectionWidth", "Fence",
                        "Connections Width between sections").ConnectionWidth = _connectionWidth

        obj.addProperty("App::PropertyInteger", "Sections", "Sections",
                        "Fence type").Sections = _sections

        obj.addProperty("App::PropertyLength", "SectionWidth", "Sections",
                        "Section Width of the Fence").SectionWidth = _sectionWidth

        obj.addProperty("App::PropertyLength", "waveDepth", "Sections",
                        "Section Width of the Fence").waveDepth = _waveDepth

        obj.addProperty("App::PropertyLength", "BottomDistance", "Fence",
                        "Connection Bottom distance").BottomDistance = _bottomDistance

        obj.addProperty("App::PropertyLength", "TopDistance", "Fence",
                        "Top connection distance").TopDistance = _topDistance

        obj.addProperty("App::PropertyLength", "SharpLength", "Fence",
                        "Sharp part length").SharpLength= _sharpLength
        
        obj.addProperty("App::PropertyLength", "NetDistance", "Fence",
                        "Sharp part length").NetDistance= _netDistance

        obj.addProperty("App::PropertyInteger", "Type", "Fence",
                        "Fence base type").Type = _type
        obj.Proxy = self
        BaseFence.placement=obj.Placement

       
    def oneElementWavedFence(self,Xoffsett,smallWidth,waveOffset):
        CoreStart=(smallWidth-self.SectionWidth)/2
        zOffset=-self.Height/2
        newobj=None
        #Left side         
        p10=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset)

        p11=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)

        p12=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)

        p13=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)

        p14=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)

        p15=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
        
        p16=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
        
        p17=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p18=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p19=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-self.SharpLength-waveOffset)
        
        p20=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+(self.SectionWidth)/2,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-waveOffset)
        
        #Right side 

        p39=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-self.SharpLength-waveOffset)
        
        p38=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)

        
        p37=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p36=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
                                
        p35=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)                                
                                
        p34=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)
        
 
        p33=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)


        p32=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p31=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p30=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset)
        
 
        newobj=Part.Face(Part.Wire(Part.makePolygon([p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p39,p38,p37,p36,p35,p34,p33,p32,p31,p30,p10])))
        objExtr=newobj.extrude(App.Vector(0,self.Thickness,0))
        return objExtr
    
                
    
    def oneElementNormalFence(self,Xoffsett,smallWidth):
        CoreStart=(smallWidth-self.SectionWidth)/2
        zOffset=-self.Height/2
        newobj=None
        #Left side         
        p10=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset)

        p11=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)

        p12=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)

        p13=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)

        p14=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)

        p15=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
        
        p16=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
        
        p17=App.Vector(BaseFence.Placement.Base.x+Xoffsett,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p18=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p19=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-self.SharpLength)
        
        p20=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+(self.SectionWidth)/2,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2)
        
        #Right side 

        
        p39=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-self.SharpLength)
        
        p38=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)

        
        p37=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p36=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
                                
        p35=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)                                
                                
        p34=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)
        
 
        p33=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)


        p32=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p31=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p30=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.SectionWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset)
        
        if self.Type==0:        
            newobj=Part.Face(Part.Wire(Part.makePolygon([p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p39,p38,p37,p36,p35,p34,p33,p32,p31,p30,p10])))
        elif self.Type==1:
            e1=(Part.makePolygon([p10,p11,p12,p13,p14,p15,p16,p17,p18,p19]))
            e2=(Part.ArcOfCircle(p19,p20,p39))
            e3=(Part.makePolygon([p39,p38,p37,p36,p35,p34,p33,p32,p31,p30,p10]))
            newobj=Part.Face(Part.Wire([e1,e2.toShape(),e3]) )
        objExtr=newobj.extrude(App.Vector(0,self.Thickness,0))
        return objExtr
    
    def normalFence(self):
        obj1=None
        try:
            smallWidth=self.Width/self.Sections
            objs=[]
            offset=0
            obj1=self.oneElementNormalFence(offset,smallWidth)
            for i in range(1, self.Sections):
                offset=i*smallWidth
                objs.append(self.oneElementNormalFence(offset,smallWidth))
            if(len(objs)>1):
                return (obj1.fuse(objs)).removeSplitter()
            else:
                return obj1.removeSplitter()
            
        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def wavedFence(self):
        #Wavy length
        try:
            smallWidth=self.Width/self.Sections          
            objs=[]
            offset=0
            angle=math.radians(180/(self.Sections-1))
            angels=[]
            if (self.Sections/2 ==int(self.Sections/2)):
                for i in range(0,int(self.Sections/2)-1):
                  angels.append(angle*i)
                angels.append(angle*self.Sections/2)
                angels.append(angle*self.Sections/2)
                for i in range(int(self.Sections/2)+1,self.Sections):
                  angels.append(angle*i)
            else:
                for i in range(0,self.Sections):
                  angels.append(angle*i)
            for i in range(0, self.Sections):
                offset=(i*smallWidth)
                objs.append(self.oneElementWavedFence(offset,smallWidth,abs(self.waveDepth*math.cos(angels[i]))))

            obj1=objs[0]
            objs.pop(0)  #Remove it from the list to allow fuse without problem
            if(len(objs)>1):
                return (obj1.fuse(objs)).removeSplitter()
            else:
                return obj1.removeSplitter()
    
        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
 
    def Uniform_X_Formed(self):

        
        #this is simpler than other types. a X and = combined together
        
        
        Cp1=App.Vector(BaseFence.Placement.Base.x,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.BottomDistance)              #Bottom-Left
        
        Cp2=App.Vector(BaseFence.Placement.Base.x+self.NetDistance,
                       BaseFence.Placement.Base.y, 
                       BaseFence.Placement.Base.z-self.Height/2+self.BottomDistance+self.NetDistance)              #Bottom-Left 2


        Cp3=App.Vector(BaseFence.Placement.Base.x+self.Width,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.BottomDistance)              #Bottom-Right 1


        Cp4=App.Vector(BaseFence.Placement.Base.x-self.NetDistance+self.Width,
                       BaseFence.Placement.Base.y, 
                       BaseFence.Placement.Base.z-self.Height/2+self.BottomDistance+self.NetDistance)              #Bottom-Right 2



        Cp55=App.Vector(BaseFence.Placement.Base.x,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.TopDistance+self.NetDistance)              #Bottom-Left

        Cp56=App.Vector(BaseFence.Placement.Base.x+self.Width,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.TopDistance+self.NetDistance)              #Bottom-Left

        Cp5=App.Vector(BaseFence.Placement.Base.x,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.TopDistance)                 #top-Left 1
        
        
        Cp6=App.Vector(BaseFence.Placement.Base.x+self.NetDistance,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.TopDistance+self.NetDistance)                #Top-Left 2


        Cp7=App.Vector(BaseFence.Placement.Base.x+self.Width,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.TopDistance)                 #Top-Right 1      
        
             
        Cp8=App.Vector(BaseFence.Placement.Base.x-self.netThickness+self.Width,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-self.Height/2+self.TopDistance)                 #Top-Right 2
        

        '''         
                    c55                                             c56 
                Cp5  Cp6                                          Cp7  Cp8

                Cp1  Cp2                                          Cp3  Cp4
        '''
        bar1=(Part.Face(Part.Wire(Part.makePolygon([Cp3,Cp7,Cp8,Cp4,Cp3])))).extrude(App.Vector(0,self.Thickness,0))            
        bar2=(Part.Face(Part.Wire(Part.makePolygon([Cp1,Cp5,Cp6,Cp2,Cp1])))).extrude(App.Vector(0,self.Thickness,0))            
        bar3=(Part.Face(Part.Wire(Part.makePolygon([Cp1,Cp7,Cp8,Cp2,Cp1])))).extrude(App.Vector(0,self.Thickness,0))            
        bar4=(Part.Face(Part.Wire(Part.makePolygon([Cp3,Cp5,Cp6,Cp4,Cp3])))).extrude(App.Vector(0,self.Thickness,0))            
        bar5=(Part.Face(Part.Wire(Part.makePolygon([Cp5,Cp8,Cp56,Cp55,Cp5])))).extrude(App.Vector(0,self.Thickness,0))            
        obj1=Part.Face(Part.Wire(Part.makePolygon([self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8,self.p1])))
        objT=obj1.extrude(App.Vector(0,self.Thickness,0))
        objNew=objT.fuse([bar1,bar2,bar3,bar4,bar5])
        return objNew.removeSplitter()

    
    def NetFence(self):
        try:
            smallWidth=self.Width/self.Sections          
            objs=[]
            offset=0
            obj1=None
            '''
                            p1  p8                              p4                    
                                                        p5      
                            
                                p7                      p6      
                            p2                                   p3
            '''
            #Net shapes vertices
            #Lines will have self.netDistance width and will have space of the same size
            NrOfNetLines=int(self.Height/(self.NetDistance))
            TopInnerPointLeft =self.p8
            TopInnerPointRight=self.p5

            BottomInnerPointLeft=self.p7
            BottomInnerPointRight=self.p6
            oneSeg=[]
            netObj=[]
            oneSeg2=[]
            netObj2=[]

            _height=self.Width-self.SectionWidth*2
            step=self.NetDistance
            step1=self.NetDistance*2
            xChange1=0
            xChange2=0
            zChange1=0
            zChange2=0
            firstTimeL=0
            firstTimeR=0
            yExtrude= self.Thickness*self.netThickness
            yOffset=((1-self.netThickness)*self.Thickness)/2
            #from left to right
            while (_height>=step1 or xChange2<(TopInnerPointRight.x-self.NetDistance*4)):
                oneSeg.clear()
                if step< (self.Height-self.SectionWidth):  #SectionWidth is the width of the frame
                    #LeftSide is less than the height .. change only the Z
                    h1=step
                    h2=step1
                    xChange2=xChange1=0    #Just to make clear what values they have
                else:
                    #Leftside is more than the height.. keep the max height and move only the X
                    h1=self.Height-self.SectionWidth
                    if firstTimeL==0:
                        xChange1=xChange1+self.NetDistance
                        firstTimeL=1
                    else:
                        xChange1=xChange1+self.NetDistance*2
                    h2=h1
                    xChange2=xChange1+self.NetDistance
                    
                oneSeg.append(BottomInnerPointLeft+App.Vector(xChange1,yOffset, h1))
                oneSeg.append(BottomInnerPointLeft+App.Vector(xChange2,yOffset, h2))    
                
                                                  
                if step1>=TopInnerPointRight.x:
                    if firstTimeR==0:
                        zChange2=zChange1+self.NetDistance*2
                        firstTimeR=1
                    else:
                        zChange2=zChange1+self.NetDistance
                        
                    zChange1=zChange2+self.NetDistance
                    oneSeg.append(BottomInnerPointRight+App.Vector(self.NetDistance,yOffset, zChange1))
                    oneSeg.append(BottomInnerPointRight+App.Vector(self.NetDistance,yOffset, zChange2))                
                else:
                    oneSeg.append(BottomInnerPointLeft+App.Vector(step1-self.NetDistance,yOffset, zChange1))
                    oneSeg.append(BottomInnerPointLeft+App.Vector(step-self.NetDistance,yOffset, zChange2))
                #Net shape
                netObj.append(Part.Face(Part.makePolygon([*oneSeg,oneSeg[0]])))

                oneSeg2=oneSeg.copy()
                for i in range(0,len(oneSeg2)):
                    pass
                    oneSeg2[i].x=self.p3.x- oneSeg[i].x
                netObj2.append(Part.Face(Part.makePolygon([*oneSeg2,oneSeg2[0]])))
                
                step=step+self.NetDistance*2
                step1=step+self.NetDistance       
                 
            f=netObj[0]
            netObj.remove(netObj[0])
            netObjExtruded=(f.fuse([*netObj2,*netObj])).extrude(App.Vector(0,yExtrude,0))
  
            #frame
            obj1=Part.Face(Part.Wire(Part.makePolygon([self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8,self.p1])))
            obj1Extruded=obj1.extrude(App.Vector(0,self.Thickness,0))            
            objNew=obj1Extruded.fuse(netObjExtruded)
            return objNew.removeSplitter()
    
        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def createObject(self):
        try:
            finalObj=None
            if self.Type==0 or self.Type==1:
                finalObj=self.normalFence()
            elif self.Type==2:
                finalObj=self.wavedFence()
            elif self.Type==3:
                finalObj=self.NetFence()
            elif self.Type==4:
                finalObj=self.Uniform_X_Formed()
            return finalObj
        except Exception as err:
            App.Console.PrintError("'execute Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    def execute(self, obj):


        self.Width = float(obj.Width)        
        self.Height = int(obj.Height)
        self.Thickness = int(obj.Thickness)
        self.SectionWidth = float(obj.SectionWidth)
        self.Type = int(obj.Type)
        self.BottomDistance = float(obj.BottomDistance)
        self.TopDistance = float(obj.TopDistance)
        self.SharpLength = float(obj.SharpLength)
        self.ConnectionWidth = float(obj.ConnectionWidth)
        self.Sections = int(obj.Sections)
        self.waveDepth=float(obj.waveDepth)
        self.NetDistance=float(obj.NetDistance)
        self.netThickness=float(obj.netThickness)
        
        
        #Frame shape vertices
        self.p1=App.Vector(BaseFence.Placement.Base.x, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)
        self.p2=App.Vector(BaseFence.Placement.Base.x, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2)
        self.p3=App.Vector(BaseFence.Placement.Base.x+self.Width, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2)
        self.p4=App.Vector(BaseFence.Placement.Base.x+self.Width, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)
        
        self.p5=App.Vector(BaseFence.Placement.Base.x+self.Width-self.SectionWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)            
        self.p6=App.Vector(BaseFence.Placement.Base.x+self.Width-self.SectionWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2+self.SectionWidth)
        self.p7=App.Vector(BaseFence.Placement.Base.x+self.SectionWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2+self.SectionWidth)
        self.p8=App.Vector(BaseFence.Placement.Base.x+self.SectionWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)            
        
        #Both distances cannot crosse each other 
        if self.BottomDistance == self.TopDistance or self.BottomDistance > self.TopDistance:
            self.BottomDistance = self.TopDistance -(1.0)
            obj.BottomDistance=self.BottomDistance
        elif self.TopDistance < self.BottomDistance:
            self.TopDistance = self.BottomDistance + (1.0)
            obj.TopDistance=self.TopDistance
        if self.netThickness>1.00 or self.netThickness<0.00:
            self.netThickness=1.00 #We don't allow values bigger than 1 or less than 0
        obj.Shape = self.createObject()

class Design456_Fence:
    def GetResources(self):
        return {'Pixmap': Design456Init.ICON_PATH + 'Fence.svg',
                'MenuText': "Fence",
                'ToolTip': "Generate a Fence"}

    def Activated(self):
        newObj = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Fence")
        plc = App.Placement()
        plc.Base = App.Vector(0, 0, 0)
        plc.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
        newObj.Placement = plc

        BaseFence(newObj)
        ViewProviderFence(newObj.ViewObject, "Fence")
        v = Gui.ActiveDocument.ActiveView
        App.ActiveDocument.recompute()
        faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Fence', Design456_Fence())