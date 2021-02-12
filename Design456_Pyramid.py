# ***************************************************************************
# *																		   *
# *	This file is part of the Open Source Design456 Workbench - FreeCAD.	   *
# *																		   *
# *	Copyright (C) 2021													   *
# *																		   *
# *																		   *
# *	This library is free software; you can redistribute it and/or		   *
# *	modify it under the terms of the GNU Lesser General Public			   *
# *	License as published by the Free Software Foundation; either		   *
# *	version 2 of the License, or (at your option) any later version.	   *
# *																		   *
# *	This library is distributed in the hope that it will be useful,		   *
# *	but WITHOUT ANY WARRANTY; without even the implied warranty of		   *
# *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU	   *
# *	Lesser General Public License for more details.						   *
# *																		   *
# *	You should have received a copy of the GNU Lesser General Public	   *
# *	License along with this library; if not, If not, see				   *
# *	<http://www.gnu.org/licenses/>.										   *
# *																		   *
# *	Author : Mariwan Jalal	 mariwan.jalal@gmail.com					   *
# ***************************************************************************
import sys
import os
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
import Design456Init 
sys.path.append(Design456Init.PYRAMID_PATH)
import polyhedrons
from PySide import QtCore, QtGui

class Design456_Pyramid:
	list= ["Pyramid",
			"Tetrahedron",
			"Hexahedron",
			"Octahedron",
			"Dodecahedron",
			"Icosahedron",
			"Icosahedron_truncated",
			"Geodesic_sphere"
			] 
			   
	"""Design456 Pyramid Toolbar"""
	def GetResources(self):
		return{
				'Pixmap' :	 Design456Init.PYRAMID_ICON_PATH+	'/Pyramid.svg',
				'MenuText': 'Pyramid',
				'ToolTip':	'Pyramid'
			}
	
	def IsActive(self):
		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True
 
	def Activated(self):
		self.appendToolbar("Pyramid",self.list) # creates a new toolbar with your commands
		self.appendMenu("Pyramid",self.list) # creates a new menu
		
