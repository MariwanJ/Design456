# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2022                                                    *
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






import FreeCAD as App
import FreeCADGui as Gui
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from inspect import getmembers, isfunction

from pkgutil import iter_modules

directory="E:/TEMP/DOC/"
MainNoid=Node("FREECAD")

def retriveOneObj(_objName,nodename):
    mainNode=nodename
    _OldNode=nodename
    try:
        for objS  in getmembers(_objName): 
            Gui.updateGui()
            for tobj in getmembers(objS):
                if  type(tobj) is tuple:
                    nObj=Node(str(tobj),_OldNode)
                else:
                    nObj=Node(tobj.__name__,_OldNode)
        return mainNode
    except Exception as err:
        print (err)


def retriveAll():		
    freecad=Node(App.__name__)
    allNode=retriveOneObj(App,freecad)
    DotExporter(allNode).to_picture(directory+"freecad.png")



retriveAll()