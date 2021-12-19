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

"""
This file will contain all event, handle, constants related to the interactive
part of the new widgets. It will keeps the events and translate them
to the desired standardized names.
Events will be defined here, mouse position will be saved here, last event..etc.
To understand how I think in making this widgets, please consider reading about
the FLTK toolkit. This is a flavour of https://www.fltk.org/.
Notice that we have two different windows system. One is for the Coin3D and 
the other is for QT Widget. 
That is why you will see different definitions here for each system.
This is only for coin3D. 
"""
# Struct to keep the mouse position in both world

import os
import sys
import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
from ThreeDWidgets.constant import FR_EVENTS
from dataclasses import dataclass
import time  # For double click detection

