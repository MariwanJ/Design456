#***************************************************************************
#*                                                                         *
#*  This file is part of the Open Source Design456 Workbench - FreeCAD.    *
#*                                                                         *
#*  Copyright (C) 2021                                                     *
#*																		   *
#*                                                                         *
#*  This library is free software; you can redistribute it and/or          *
#*  modify it under the terms of the GNU Lesser General Public             *
#*  License as published by the Free Software Foundation; either           *
#*  version 2 of the License, or (at your option) any later version.       *
#*                                                                         *
#*  This library is distributed in the hope that it will be useful,        *
#*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
#*  Lesser General Public License for more details.                        *
#*                                                                         *
#*  You should have received a copy of the GNU Lesser General Public       *
#*  License along with this library; if not, If not, see                   *
#*  <http://www.gnu.org/licenses/>.                                        *
#*                                                                         *
#*  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
#***************************************************************************
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
#TODO: Do we need this? I must check it later
class FACE_D:
	def __init__(self, view):
	   self.view = view
	   v=Gui.activeDocument().activeView()
		
	def getDirectionAxis(self):
		try:
			s=Gui.Selection.getSelectionEx()
			obj=s[0]
			faceSel = obj.SubObjects[0]
			dir = faceSel.normalAt(0,0)
			if dir.z == 1 :
				return "z"
			elif dir.y==1 :
				return "y"
			else :
				return "x"
		except ImportError as err:
			App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
								   "{err}\n".format(err=str(err)))
				
	def MousePosition(self, info):
		try:
			down = (info["State"] == "DOWN")
			pos = info["Position"]
			#if (down):
			FreeCAD.Console.PrintMessage("Clicked on position: ("+str(pos[0])+", "+str(pos[1])+")\n")
			pnt = self.view.getPoint(pos)
			FreeCAD.Console.PrintMessage("World coordinates: " + str(pnt) + "\n")
			info = self.view.getObjectInfo(pos)
			FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n")
			o = ViewObserver(v)
			c = v.addEventCallback("SoMouseButtonEvent",o.logPosition)
			return pnt
		except ImportError as err:
			App.Console.PrintError("'FACE_D.getDirectionAxis' Failed. "
								   "{err}\n".format(err=str(err)))
			
	def ExtractFace(self):
		try:
			s = Gui.Selection.getSelectionEx()
			for o in s:
				objName = o.ObjectName
				sh = o.Object.Shape.copy()
				if hasattr(o.Object, "getGlobalPlacement"):
					gpl = o.Object.getGlobalPlacement()
					sh.Placement = gpl
				for name in o.SubElementNames:
					fullname = objName+"_"+name
					newobj = o.Document.addObject("Part::Feature",fullname)
					newobj.Shape = sh.getElement(name)
			App.ActiveDocument.recompute()
			return self.newobj
				#o.Object.ViewObject.Visibility = False
		except ImportError as err:
			App.Console.PrintError("'FACE_D.ExtractFace' Failed. "
								   "{err}\n".format(err=str(err)))	