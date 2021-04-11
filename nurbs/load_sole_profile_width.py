
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
load width information for a sole from a sketcher file
filename is 'User parameter:Plugins/shoe').GetString("width profile")
there must be one sketch in it with constraints  l1-l12, r1-r12
'''


import FreeCAD
import FreeCADGui

import os
import 

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')

spreadsheet_lib
reload(.spreadsheet_lib)
sole
reload(.sole)


from .spreadsheet_lib import cellname

# from .errors import sayexc
from .say import *


def runa():
    ''' load the data from the first sketch in file fn
    writes the data into the spreadsheet 
    and recomputes the sole
    '''

#    raise Exception("test fehler")
    aktiv = App.ActiveDocument

    fna = App.ParamGet(
        'User parameter:Plugins/shoe').GetString("width profile")
    if fna == '':
        __dir__ = os.path.dirname(.__file__)
        fna = __dir__ + "/../testdata/breitev3.fcstd"
        App.ParamGet('User parameter:Plugins/shoe').SetString(
            "width profile", fna)

    dok = App.open(fna)
    sss = dok.findObjects("Sketcher::SketchObject")
    s = sss[0]

    # werte aus sketch holen
    rs = []
    ls = []
    for i in range(1, 12):
        rs += [s.getDatum('r' + str(i)).Value]
        ls += [s.getDatum('l' + str(i)).Value]

    App.closeDocument(dok.Name)

    # eigentliche Arbeitsdatei
    dok2 = aktiv
    App.setActiveDocument(dok2.Name)

    sss = dok2.findObjects("Sketcher::SketchObject")
#    print sss,dok2.Name
    ss = dok2.Spreadsheet

    # daten ins spreadsheet
    for s in range(1, 12):
        cn = cellname(s + 1, 14)
        ss.set(cn, str(rs[s - 1]))
        cn = cellname(s + 1, 15)
        ss.set(cn, str(ls[s - 1]))

    # aktualisieren
    dok2.recompute()
    .sole.run()
    dok2.recompute()


def run():
    ''' run with error handling'''
    try:
        runa()
    except:
        sayexc2(
            __name__, "was ist los--------------------------------------------------------------------")
