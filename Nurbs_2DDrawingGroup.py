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

import os, sys
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
sys.path.append(Design456Init.NURBS_PATH)
sys.path.append(Design456Init.NURBS_WB_PATH)
sys.path.append(Design456Init.NURBS_PLOT_PATH)

import create_sole_sketch

class Design456_Nurbs_2DDrawingGroup:

    """Design456 Part 2D Drawing"""

    def GetCommands(self):
        """3D Modifying Tools."""
        return ("runSole",
                

                )

    def GetResources(self):
        import Design456Init
        from PySide.QtCore import QT_TRANSLATE_NOOP
        """Set icon, menu and tooltip."""
        _tooltip = ("Different Tools - Nurbs")
        return {'Pixmap':  NURBS_ICON_PATH + '/Design456_Nurbs.svg',
                'MenuText': QT_TRANSLATE_NOOP("Design456", "NurbsTools"),
                'ToolTip': QT_TRANSLATE_NOOP("Design456", _tooltip)}

Gui.addCommand("Design456_Nurbs_2DDrawingGroup", Design456_Nurbs_2DDrawingGroup())



# Move an object to the location of the mouse click on another surface
class Design456_Nurbs_DrawOnFace:
    """ Draw on any face.
    """
    def Activated(self):
        try:
            pass
        except Exception as err:
            App.Console.PrintError("'Magnet' Failed. "
                                   "{err}\n".format(err=str(err)))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    def GetResources(self):
        return {
            'Pixmap': Design456Init.NURBS_ICON_PATH + '/draw.svg',
            'MenuText': 'Nurbs Draw',
                        'ToolTip':  'Nrubs Draw'
        }


Gui.addCommand('Design456_Nurbs_DrawOnFace', Design456_Nurbs_DrawOnFace())
Design456_Magnet.__doc__ = """To be added later
                            """