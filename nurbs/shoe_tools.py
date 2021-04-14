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

'''tools for shoe editor'''

from say import *
import Design456Init

# toggle all position constraints of a gui selected shoe rib
#
# Rippe auswaehlen
# Menu Shoe -> toggle constraints of a rib  (oder symbol blaue sohle)
#
# Alle Positionsconstraints sind blau
#
# bei Wiederholung werden alle wieder rot
#


def toggleShoeSketch():
    '''toggle all position constraints of a gui selected shoe rib'''
    if len(Gui.Selection.getSelectionEx()) != 0:
        sk = Gui.Selection.getSelectionEx()[0]
    print("toggle sketch constraints for " + sk.Label)
    for i, c in enumerate(sk.Constraints):
        if c.Name.startswith('p') or c.Name.startswith('tang') or c.Name.startswith('Width'):
            print(c.Name)
            try:
                sk.toggleDriving(i)
        #        sk.setDriving(i,False)
            except:
                pass
