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


'''
load height and length information for a sole from a sketcher file
filename is 'User parameter:Plugins/shoe').GetString("height profile")
the skeche contains exactly one bspline curve
'''



#\cond
import FreeCAD as App
import FreeCADGui as Gui



import os, 
global __dir__
__dir__ = os.path.dirname(.__file__)

spreadsheet_lib
reload (.spreadsheet_lib)
from .spreadsheet_lib import ssa2npa, npa2ssa, cellname

#\endcond
# from .errors import showdialog 

from .say import *

## load height profile from file
#

def run():

    try:
        aktiv=App.ActiveDocument
        if aktiv==None:
            showdialog("Fehler","no Sole Document","first open or create a sole document")

        fn=App.ParamGet('User parameter:Plugins/shoe').GetString("height profile")
        if fn=='':
            fn= __dir__+"/../testdata/heelsv3.fcstd"
            App.ParamGet('User parameter:Plugins/shoe').SetString("height profile",fn)

        dok=App.open(fn)

        sss=dok.findObjects("Sketcher::SketchObject")

        try:
            s=sss[0]
            c=s.Shape.Edge1.Curve
        except: 
            showdialog("Error","Height profile document has no sketch")


        pts=c.discretize(86)

        mpts=[]
        for i in [0,15,25,35,45,55,65,75,85]:
            mpts.append(pts[i])


        App.closeDocument(dok.Name)

        dok2=aktiv
        App.setActiveDocument(dok2.Name)

        ss=dok2.Spreadsheet




        # daten ins spreadsheet schreiben
        for s in range(8):
            cn=cellname(s+3,9)
            ss.set(cn,str(mpts[-s-1].y))

        # ferse hochlegen
        for j in range(7):
            cn=cellname(j+2,26)
            ss.set(cn,str((mpts[-1].y)))


        dok2.recompute()
        sole
        reload(.sole)
        .sole.run()
        dok2.recompute()

    except : showdialog() 
