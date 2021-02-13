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
import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Draft
import Part
import Design456Init


class Design456_Tool_Magnet:
    obj1 = obj2 = None
    sub1 = sub2 = None
    clickpos1 = clickpos2 = None
    doc = obj = sub = None
    # Obj1 will be moved on top of Object2

    def __init__(self, view):
        self.view = view

    def setPreselection(self, doc, obj, sub):                # Preselection object
        # The part of the object name
        self.doc = doc
        self.obj = obj
        self.sub = sub
        #App.Console.PrintMessage(str(sub) + "\n")

    """
    def addSelection(self,doc,obj,sub,pnt):               # Selection object
        App.Console.PrintMessage("addSelection"+ "\n")
        # Name of the document
        App.Console.PrintMessage(str(doc)+ "\n")
        App.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # The part of the object name
        App.Console.PrintMessage(str(sub)+ "\n")
        # Coordinates of the object
        App.Console.PrintMessage(str(pnt)+ "\n")
        App.Console.PrintMessage("______"+ "\n")
    """

    def logPosition(self, info):
        down = (info["State"] == "DOWN")
        pos = info["Position"]
        if (down):
            if(self.clickpos1 == None):
                self.clickpos1 = self.view.getPoint(pos)
            elif(self.clickpos2 == None):
                self.clickpos2 = self.view.getPoint(pos)
            else:
                clickpos1 = self.view.getPoint(pos)
                clickpos2 = None
        self.setSelection(self.doc, self.obj, self.sub)

    def Magnet(self, OBJ1, OBJ2):
        # Move OBJ1 to be on Top2
        print(self.clickpos2)
        print(OBJ1.Placement)
        OBJ1.Placement = self.clickpos2
        App.ActiveDocument.recompute()
        print(OBJ1.Placement)

    def removeSelection(self, doc, obj, sub):                # Delete the selected object
        #App.Console.PrintMessage("removeSelection" + "\n")
        return

    def setSelection(self, doc, obj, sub):                           # Selection in ComboView
        if (self.obj1 == None):
            self.obj1 = obj
            self.sub1 = sub
        elif(self.obj2 == None):
            self.obj2 = obj
            self.sub2 = sub
        else:
            # We have two objects do the job.
            self.Magnet(self.obj1, self.obj2)

    # If click on the screen, clear the selection
    def clearSelection(self, doc):
        # If click on another object, clear the previous object
        return
        #App.Console.PrintMessage("clearSelection" + "\n")


v = Gui.activeDocument().activeView()
s = Design456_Tool_Magnet(v)
# install the function mode resident

c = v.addEventCallback("SoMouseButtonEvent", s.logPosition)
Gui.Selection.addObserver(s)
# FreeCADGui.Selection.removeObserver(s)
