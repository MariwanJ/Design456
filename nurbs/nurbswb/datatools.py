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
# * Modified and adapted to Desing456 by:                                  *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

''' a collection of data nodes for floatlists, integerlists, vectorlist, matrixes etc
these nodes are used as properties in other nodes
an example is the dynamic offset node which controls the offset by a floatlist
'''




from say import *
import nurbswb.pyob

## A list for Floats

class FloatList(nurbswb.pyob.FeaturePython):
    '''a list of floats'''

    ##\cond
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = self.__class__.__name__
        nurbswb.pyob.ViewProvider(obj.ViewObject) 


    def onChanged(proxy,obj,prop):
        '''run myExecute for property prop: relativePosition and vertexNumber'''

        if prop.startswith("val"):
            data=[]
            for i in range(obj.size):
                data.append(getattr(obj, "val%03d" % (i)))
            print (data)
            obj.datalist=data

        if prop=='factor': # scale to the new factor
            try: 
                oldfactor=proxy.oldfactor
                for i in range(obj.size):
                    s=getattr(obj, "val%03d" % (i))
                    setattr(obj, "val%03d" % (i),s*obj.factor/oldfactor)
            except:
                sayexc()

    def onBeforeChange(proxy,obj,prop):
        # store the old value for transformation
        if prop=='factor':
            proxy.oldfactor=obj.factor

    ##\endcond



## create a FloatList node
# 
# *Properties*
#
#  - **size** - length of the list (default 12,hiddeen)
#  - **factor** - to scale the values (default 10) 
#  - **val001 ... val999**
#  - **datalist**  - all values as list (hidden)
# 
# @image html plane.svg
#
# example to use  DynaOffset
# .




def createFloatlist(name="Floatlist"):
    '''create a FloatList node'''

    obj = App.ActiveDocument.addObject("Part::FeaturePython",name)

    obj.addProperty("App::PropertyInteger", "factor", "Base").factor=10
    obj.addProperty("App::PropertyInteger", "size", "Base").size=12
    obj.addProperty("App::PropertyFloatList", "datalist", "Values")

    for i in range(obj.size):
        obj.addProperty("App::PropertyFloat", "val%03d" % (i), "Values")
        setattr(obj, "val%03d" % (i),obj.factor/2)
    
    obj.setEditorMode("datalist", 2) 
    obj.setEditorMode("size", 2) 
    obj.setEditorMode("Placement", 2) 

    FloatList(obj)
    obj.Proxy.onChanged(obj,"val")
    return obj


##  method for workbench menu entry

def runFloatlist():
    ''' create the default FloatList'''
    createFloatlist()
