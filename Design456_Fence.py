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
import Part
from draftutils.translate import translate  # for translate
import Design456Init
import FACE_D as faced
import math

__updated__ = '2022-09-30 21:52:18'


#TODO : FIXME: Add more shapes!!
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
                 _frameWidth=2,             #Out side frame
                 _innerSecWidth=2,
                 _sections=4,
                 _connectionWidth=1.00,
                 _bottomDistance=2.00,
                 _topDistance=8.00,
                 _sharpLength=1.00,
                 _waveDepth=3.0,
                 _netDistance=0.5,
                 _netThickness=0.80,
                 _type=0,
                 ):

        obj.addProperty("App::PropertyLength", "Width", "Fence Widths",
                        "Width of the Fence").Width = _width
                        
        obj.addProperty("App::PropertyLength", "Height", "Fence",
                        "Height of the Fence").Height = _height

        obj.addProperty("App::PropertyLength", "Thickness", "Fence Thicknesses",
                        "Thickness of the Fence").Thickness = _thickness

        obj.addProperty("App::PropertyLength", "FrameWidth", "Fence Widths",
                        "Fence Frame Width").FrameWidth = _frameWidth               # X axis

        obj.addProperty("App::PropertyLength", "InnerSecWidth", "Fence Widths",
                        "Fence Inner section Width").InnerSecWidth = _innerSecWidth  # X axis  
        
        obj.addProperty("App::PropertyLength", "netThickness", "Fence Thicknesses",
                        "Thickness of the Fence").netThickness = _netThickness #This is a percentage of the total thickness
        
        obj.addProperty("App::PropertyLength", "ConnectionWidth", "Fence Widths",
                        "Connections Width between sections").ConnectionWidth = _connectionWidth    # Z axis

        obj.addProperty("App::PropertyInteger", "Sections", "Sections",
                        "Fence type").Sections = _sections

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

    #type 0 &1
    def oneElementNormalFence(self,Xoffsett,smallWidth):
        CoreStart=(smallWidth-self.InnerSecWidth)/2
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
        
        p20=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+(self.InnerSecWidth)/2,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2)
        
        #Right side 

        p39=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-self.SharpLength)
        
        p38=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)

        
        p37=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p36=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
                                
        p35=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)                                
                                
        p34=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)
        
 
        p33=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)


        p32=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p31=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p30=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
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
    
    #Type 0&1
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
  
               
    #Type 2
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
    #Type 2
    def oneElementWavedFence(self,Xoffsett,smallWidth,waveOffset):
        CoreStart=(smallWidth-self.InnerSecWidth)/2
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
        
        p20=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+(self.InnerSecWidth)/2,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-waveOffset)
        
        #Right side 

        p39=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+self.Height/2-self.SharpLength-waveOffset)
        
        p38=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)

        
        p37=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance+self.ConnectionWidth)
        
        p36=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)
                                
        p35=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.TopDistance)                                
                                
        p34=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)
        
 
        p33=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance+self.ConnectionWidth)


        p32=App.Vector(BaseFence.Placement.Base.x+Xoffsett+smallWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p31=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset+self.BottomDistance)
        
        p30=App.Vector(BaseFence.Placement.Base.x+Xoffsett+CoreStart+self.InnerSecWidth,
                       BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z+zOffset)
        
 
        newobj=Part.Face(Part.Wire(Part.makePolygon([p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p39,p38,p37,p36,p35,p34,p33,p32,p31,p30,p10])))
        objExtr=newobj.extrude(App.Vector(0,self.Thickness,0))
        return objExtr
         
    #Type 3        
    def NetFence(self):
        try:
            obj1=None
            '''
                            p1  p8                              p4                    
                                                        p5      
                            
                                p7                      p6      
                            p2                                   p3
            '''
            #Net shapes vertices
            #Lines will have self.netDistance width and will have space of the same size
            TopInnerPointRight=self.p5
            BottomInnerPointLeft=self.p7
            BottomInnerPointRight=self.p6
            oneSeg=[]
            netObj=[]
            oneSeg2=[]
            netObj2=[]

            _height=self.Width-self.FrameWidth*2
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
                if step< (self.Height-self.FrameWidth):  #FrameWidth is the width of the frame
                    #LeftSide is less than the height .. change only the Z
                    h1=step
                    h2=step1
                    xChange2=xChange1=0    #Just to make clear what values they have
                else:
                    #Leftside is more than the height.. keep the max height and move only the X
                    h1=self.Height-self.FrameWidth
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
    
    #Tupe 4
    def Uniform_X_Formed(self):
        #this is simpler than other types. a X and = combined together
        offset=self.Height/2
        
        Cp1=App.Vector(BaseFence.Placement.Base.x,BaseFence.Placement.Base.y,
                       BaseFence.Placement.Base.z-offset+self.BottomDistance)            
        
        Cp2=App.Vector(Cp1.x+self.NetDistance,Cp1.y,Cp1.z+self.NetDistance)
        Cp3=App.Vector(Cp1.x+self.Width-self.NetDistance,Cp1.y,Cp1.z+self.NetDistance)
        Cp4=App.Vector(Cp1.x+self.Width,Cp1.y,Cp1.z)
        Cp5=App.Vector(Cp1.x,Cp1.y,Cp1.z+self.TopDistance)                                             
        Cp6=App.Vector(Cp5.x+self.NetDistance,Cp5.y,Cp5.z-self.NetDistance)             
        Cp7=App.Vector(Cp5.x-self.NetDistance+self.Width,Cp5.y,Cp5.z-self.NetDistance)                             
        Cp8=App.Vector(Cp5.x+self.Width,Cp5.y,Cp5.z) 
        
        '''         
                Cp5                                                Cp8
                        Cp6                                  Cp7  
                                                             
                    
                     Cp2                                  Cp3      
                Cp1                                             Cp4
        '''
        bar1=(Part.Face(Part.Wire(Part.makePolygon([Cp1,Cp4,Cp3,Cp2,Cp1])))).extrude(App.Vector(0,self.Thickness,0))            
        bar2=(Part.Face(Part.Wire(Part.makePolygon([Cp5,Cp6,Cp7,Cp8,Cp5])))).extrude(App.Vector(0,self.Thickness,0))            
        bar3=(Part.Face(Part.Wire(Part.makePolygon([Cp2,Cp8,Cp7,Cp1,Cp2])))).extrude(App.Vector(0,self.Thickness,0))            
        bar4=(Part.Face(Part.Wire(Part.makePolygon([Cp5,Cp3,Cp4,Cp6,Cp5])))).extrude(App.Vector(0,self.Thickness,0))            
   
        obj1=Part.Face(Part.Wire(Part.makePolygon([self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8,self.p1])))
        objT=obj1.extrude(App.Vector(0,self.Thickness,0))
        objNew=objT.fuse([bar1,bar2,bar3,bar4])
        return objNew.removeSplitter()

    #Type 5
    def holeInBox_oneSegMent(self):
        '''
                            p1  p8                              p4                    
                                                        p5      
                            
                                p7                      p6      
                            p2                                   p3
        '''
        try:
            holes=[]
            from random import randrange
            holesX=int(self.Width-2*self.FrameWidth)
            yOffset=((1-self.netThickness)*self.Thickness)/2
            yExtrude= self.Thickness*self.netThickness
            _p1=App.Vector(self.p8.x,self.p8.y+yOffset,self.p8.z)
            _p2=App.Vector(self.p5.x,self.p5.y+yOffset,self.p5.z)
            _p3=App.Vector(self.p6.x,self.p6.y+yOffset,self.p6.z)
            _p4=App.Vector(self.p7.x,self.p7.y+yOffset,self.p7.z)
            box=Part.Face(Part.Wire(Part.makePolygon([_p1,_p2,_p3,_p4,_p1])))
            scale=0.6
            nPlc=BaseFence.Placement.copy()
            nPlc.Rotation.Angle=math.radians(90)
            nPlc.Rotation.Axis=App.Vector(1,0,0)
            total=int((self.Width-2*self.FrameWidth))
            if total<1:
                total=1
            # Scale in one direction
            mtr1= App.Matrix(1, 0, 0, 0,
                                    0, scale, 0, 0,
                                    0, 0, 1, 0,
                                    0, 0, 0,  1)

            for j in range (0,self.Height):
                for i in range(0,total):
                    if int((j+i)/2)==(j+i)/2:
                        r=0.35
                    else:
                        r=0.25
                    oneH=(Part.makeCylinder(r,self.Thickness*10,App.Vector(nPlc.Base.x+r*1.5+self.FrameWidth+i,
                                                nPlc.Base.z-self.Height/2+j*(2),
                                                nPlc.Base.y-self.Thickness*2)))
                    oneHS=oneH.transformGeometry(mtr1)
                    oneHS.Placement.Rotation=nPlc.Rotation
                    holes.append(oneHS)
            obj1=Part.Face(Part.Wire(Part.makePolygon([self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8,self.p1])))
            objNewT=obj1.extrude(App.Vector(0,self.Thickness,0))
            boxE=box.extrude(App.Vector(0,yExtrude,0))
            objNew=objNewT.fuse(boxE.cut(holes))
            return objNew
        
        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    #Type 5
    def holeInBox(self):
        return (self.holeInBox_oneSegMent())

    #Type 6
    def bricksSeg(self):
        try:
            yExtrude= self.Thickness*self.netThickness
            brickWidth=2
            brickHeight=1
            noOfBricksW=int((self.Width-self.FrameWidth)/brickWidth)
            noOfBricksZ=int((self.Height-self.FrameWidth)/brickHeight)
            bricks=[]
            oneMore=0
            if (self.FrameWidth==1):
                oneMore=1
            yOffset=((1-self.netThickness)*self.Thickness)/2    
            b1=self.p7+App.Vector(0,yOffset,0)                            
            for jj in range(1,noOfBricksZ+1):
                for i in range(1,noOfBricksW+oneMore):
                    if int(jj/2)==jj/2:
                        offset=App.Vector(0,0,0)
                    else:
                        offset=App.Vector(-brickWidth/2,0,0)
                        
                    if (i==1 and int(jj/2)!=jj/2):
                        rightB=App.Vector(brickWidth/2,0,0)
                        leftT=App.Vector(0,0,brickHeight)
                        rightT=rightB+leftT
                        offset=App.Vector(0, 0,0)
                    else:
                        rightB=App.Vector(brickWidth,0,0)
                        leftT=App.Vector(0,0,brickHeight)
                        rightT=rightB+leftT

                    a=[b1+offset,
                       b1+offset+rightB,
                       b1+offset+rightT,
                       b1+offset+leftT,
                       b1+offset]
                    brick=Part.Face(Part.Wire(Part.makePolygon(a)))
                    bricks.append(brick.extrude(App.Vector(0,yExtrude,0)))
                    b1=b1+App.Vector(brickWidth,0,0)
                if (offset.x==-brickWidth/2):
                    a=[b1+offset,
                        b1+offset+App.Vector(brickWidth/2,0,0),
                        b1+offset+leftT+App.Vector(brickWidth/2,0,0),
                        b1+offset+leftT,
                        b1+offset]
                    brick=Part.Face(Part.Wire(Part.makePolygon(a)))
                    bricks.append(brick.extrude(App.Vector(0,yExtrude,0)))
                b1=self.p7+App.Vector(0,0,jj*brickHeight)+App.Vector(0,yOffset,0)   
            obj1=Part.Face(Part.Wire(Part.makePolygon([self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8,self.p1])))
            objNewT=obj1.extrude(App.Vector(0,self.Thickness,0))
            objN=Part.Compound([objNewT,*bricks])
            return objN
        
        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
    #Type 7
    def curvedSectionSeg(self,sec):
        try:
            yExtrude=self.Thickness*self.netThickness
            yOffset=((1-self.netThickness)*self.Thickness)/2
            smallWidth=self.Width/self.Sections
            if (sec!=0):          
                offset=App.Vector((smallWidth)*sec,0,0)
            else:
                offset=App.Vector(smallWidth*sec,0,0)
                
            obj1=None
            #Left pin            
            np1=offset+self.p2     #Bottom left
            np2=offset+self.p1     #Top left
            np3=np1+App.Vector(self.FrameWidth,0,0)        
            np4=np2+App.Vector(self.FrameWidth,0,0)
            
            #Right pin            
            np5=np1+App.Vector(smallWidth-self.FrameWidth,0,0)
            np6=np2+App.Vector(smallWidth-self.FrameWidth,0,0)
            np7=np3+App.Vector(smallWidth-self.FrameWidth,0,0)
            np8=np4+App.Vector(smallWidth-self.FrameWidth,0,0)
            
            #upper side            
            #First Curve - upp
            apc1=np1+App.Vector(0,yOffset,self.TopDistance)                         #left point
            apc2=apc1+App.Vector(smallWidth/2,0,self.ConnectionWidth/2)       #middle point
            apc3=apc1+App.Vector(smallWidth,0,0)                              #right point

            #second curve - upp
            apc11=apc1-App.Vector(0,0,self.ConnectionWidth/2)                 #left point upper curve
            apc12=apc2-App.Vector(0,0,self.ConnectionWidth*2 )                #middle point upper curve
            apc13=apc3-App.Vector(0,0,self.ConnectionWidth/2)                 #right point upper curve
           
            aC11 = Part.Arc(apc1,apc2, apc3)                                    #curve upp TOP DISTANCE
            aC12 = Part.Arc(apc13,apc12, apc11)                                 #curve down TOP DISTANCE
            alin11=Part.makePolygon([apc1,apc11])                              #Line left between curves
            alin12=Part.makePolygon([apc3,apc13])                              #Line right between curves
            anObj=Part.Face(Part.Wire([aC11.toShape(),alin11,aC12.toShape(),alin12]))


            #Lower side
            bpc1=np1+App.Vector(0,yOffset,self.BottomDistance)                        #left point
            bpc2=bpc1+App.Vector(smallWidth/2,0,self.ConnectionWidth/2)       #middle point
            bpc3=bpc1+App.Vector(smallWidth,0,0)                              #right point
            
            #Upper side
            bpc11=bpc1-App.Vector(0,0,self.ConnectionWidth/2)                 #left point upper curve
            bpc12=bpc2-App.Vector(0,0,self.ConnectionWidth*2 )                #middle point upper curve
            bpc13=bpc3-App.Vector(0,0,self.ConnectionWidth/2)                 #right point upper curve
           
            bC11 = Part.Arc(bpc1,bpc2, bpc3)                                    #curve upp TOP DISTANCE
            bC12 = Part.Arc(bpc13,bpc12, bpc11)                                 #curve down TOP DISTANCE
            blin11=Part.makePolygon([bpc1,bpc11])                              #Line left between curves
            blin12=Part.makePolygon([bpc3,bpc13])                              #Line right between curves
            bnObj=Part.Face(Part.Wire([bC11.toShape(),blin11,bC12.toShape(),blin12]))
            eOBJ=bnObj.fuse(anObj).extrude(App.Vector(0,yExtrude,0))

            pin1=Part.Face(Part.Wire(Part.makePolygon([np1,np2,np4,np3,np1])))
            pin2=Part.Face(Part.Wire(Part.makePolygon([np5,np6,np8,np7,np5])))
            
            epin1=pin1.extrude(App.Vector(0,self.Thickness,0))
            epin2=pin2.extrude(App.Vector(0,self.Thickness,0))
            nObj=epin1.fuse([eOBJ,epin2]).removeSplitter()         
            return nObj 

        except Exception as err:
            App.Console.PrintError("'createObject Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    #Type 7
    
    def curvedSection(self):
        allOBJ=[]
        for i in range (0,self.Sections):
            allOBJ.append(self.curvedSectionSeg(i))
        
        first=allOBJ[0]
        allOBJ.pop(0)
        return first.fuse(allOBJ)
    
    #Type 8
    def MultiXSectionsSeg(self,seg):
        try:
            
            objN=None
            yExtrude= self.Thickness*self.netThickness
            yOffset=((1-self.netThickness)*self.Thickness)/2
            smallWidth=(self.Width-self.FrameWidth*(1-self.Sections))/(self.Sections)
            xOffset=App.Vector(seg*(smallWidth-self.FrameWidth),0,0)

            '''
                            p1  p4                      p8   p5                    
                                p44                     p88    
                            
                                p33                     p77       
                            p2  p3                      p7   p6
            '''        
            p1=self.p1+xOffset
            p2=self.p2+xOffset
            p3=p2+App.Vector(self.FrameWidth,0,0)
            p4=p1+App.Vector(self.FrameWidth,0,0)
            
            p5=p1+App.Vector(smallWidth,0,0)
            p6=p2+App.Vector(smallWidth,0,0)
            p7=p6-App.Vector(self.FrameWidth,0,0)
            p8=p5-App.Vector(self.FrameWidth,0,0)
            
            barP1=p4-App.Vector(self.NetDistance,0,0) +App.Vector(0,yOffset,0)
            barP2=p4+App.Vector(0,yOffset,0)
            barP3=p7+App.Vector(self.NetDistance,0,0)+App.Vector(0,yOffset,0)
            barP4=p7+App.Vector(0,yOffset,0)

            barP5=p3-App.Vector(self.NetDistance,0,0)+App.Vector(0,yOffset,0)
            barP6=p3+App.Vector(0,yOffset,0)
            barP7=p8+App.Vector(self.NetDistance,0,0)+App.Vector(0,yOffset,0)
            barP8=p8+App.Vector(0,yOffset,0)
            
            pin1=Part.Face(Part.Wire(Part.makePolygon([p1,p2,p3,p4,p1])))
            pin2=Part.Face(Part.Wire(Part.makePolygon([p8,p7,p6,p5,p8])))

            pin1x=Part.Face(Part.Wire(Part.makePolygon( [barP1,barP2,barP3,barP4,barP1] )))
            pin1y=Part.Face(Part.Wire(Part.makePolygon( [barP5,barP6,barP7,barP8,barP5] )))
            innerPart=(pin1x.fuse(pin1y)).extrude(App.Vector(0,yExtrude,0))
            frame=(pin1.fuse(pin2)).extrude(App.Vector(0,self.Thickness,0))
            finalObj=frame.fuse(innerPart)        
            return finalObj

        except Exception as err:
            App.Console.PrintError("'execute Fence' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
    
    #Type 8
    def MultiXSections(self):
        try:
            objNew=[]
            finalObj=None
            if self.Sections>1:
                for i in range(self.Sections):
                    objNew.append(self.MultiXSectionsSeg(i))
                first=objNew[0]
                if len(objNew)>2:
                    objNew.pop(0)
                else:
                    finalObj= objNew[0]
                finalObj= (first.fuse(objNew).removeSplitter())
            else:
                finalObj= (self.MultiXSectionsSeg(1))  
            yOffset=((1-self.netThickness)*self.Thickness+self.Thickness*self.netThickness)/2
            box=Part.Face(Part.Wire(Part.makePolygon([self.p1+App.Vector(0,yOffset),
                                                      self.p2+App.Vector(0,yOffset),
                                                      self.p3+App.Vector(0,yOffset),
                                                      self.p4+App.Vector(0,yOffset),
                                                      self.p1+App.Vector(0,yOffset)])))
            eBox=box.extrude(App.Vector(0,0.2,0))   #Hardcoded thickness  TODO: Is this good?
            return eBox.fuse(finalObj)

        except Exception as err:
            App.Console.PrintError("'execute Fence' Failed. "
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
            elif self.Type==5:
                finalObj=self.holeInBox()
            elif self.Type==6:
                finalObj=self.bricksSeg()
            elif self.Type==7:
                finalObj=self.curvedSection()
            elif self.Type==8:
                finalObj=self.MultiXSections()                                
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
        self.Type = int(obj.Type)
        self.BottomDistance = float(obj.BottomDistance)
        self.TopDistance = float(obj.TopDistance)
        self.SharpLength = float(obj.SharpLength)
        self.ConnectionWidth = float(obj.ConnectionWidth)
        self.Sections = int(obj.Sections)
        self.waveDepth=float(obj.waveDepth)
        self.NetDistance=float(obj.NetDistance)
        self.netThickness=float(obj.netThickness)
        self.FrameWidth=float(obj.FrameWidth)
        self.InnerSecWidth= float(obj.InnerSecWidth)
        '''
                        p1  p8                              p4                    
                                                    p5      
                        
                            p7                      p6      
                        p2                                   p3
        '''
        #Frame shape vertices
        self.p1=App.Vector(BaseFence.Placement.Base.x, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)
        self.p2=App.Vector(BaseFence.Placement.Base.x, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2)
        self.p3=App.Vector(BaseFence.Placement.Base.x+self.Width, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2)
        self.p4=App.Vector(BaseFence.Placement.Base.x+self.Width, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)
        
        self.p5=App.Vector(BaseFence.Placement.Base.x+self.Width-self.FrameWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)            
        self.p6=App.Vector(BaseFence.Placement.Base.x+self.Width-self.FrameWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2+self.FrameWidth)
        self.p7=App.Vector(BaseFence.Placement.Base.x+self.FrameWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z-self.Height/2+self.FrameWidth)
        self.p8=App.Vector(BaseFence.Placement.Base.x+self.FrameWidth, BaseFence.Placement.Base.y,BaseFence.Placement.Base.z+self.Height/2)            
        
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
        # if obj.Type!=1:
        #     obj.removeProperty("NetDistance")
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
        #faced.PartMover(v, newObj, deleteOnEscape=True)

Gui.addCommand('Design456_Fence', Design456_Fence())