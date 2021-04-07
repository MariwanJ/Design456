# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- create a parametric filled face
#--
#-- microelly 2017 v 0.2
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''a parametric filled face object based on 3 edges
the edges can be separate object but edges of complex shapes too
the numbers n1, n2, n3 defines the edge number of the underlying shape
'''


import FreeCAD
import FreeCADGui
App = FreeCAD
Gui = FreeCADGui

import Part


class PartFeature:

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj

# grundmethoden zum sichern

	def attach(self, vobj):
		self.Object = vobj.Object

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None


class ViewProvider:

	def __init__(self, obj):
		obj.Proxy = self
		self.Object = obj

	def __getstate__(self):
		return None

	def __setstate__(self, state):
		return None


def createShape(obj):
	'''create the FilledFace Shape for the edges of obj'''

	lls = []
	if obj.e1 != None:
		lls += [obj.e1.Shape.Edges[obj.n1 - 1]]
	if obj.e2 != None:
		lls += [obj.e2.Shape.Edges[obj.n2 - 1]]
	if obj.e3 != None:
		lls += [obj.e3.Shape.Edges[obj.n3 - 1]]

	# check wire closed !!!

	try:
		obj.Shape = Part.makeFilledFace(Part.__sortEdges__(lls))
	except:
		obj.Shape = Part.Shape()


class FilledFace(PartFeature):
	'''parametric filled face'''

	def __init__(self, obj):
		PartFeature.__init__(self, obj)

		obj.addProperty("App::PropertyLink", "e1", "Base")
		obj.addProperty("App::PropertyLink", "e2", "Base")
		obj.addProperty("App::PropertyLink", "e3", "Base")

		obj.addProperty("App::PropertyInteger", "n1", "Base")
		obj.addProperty("App::PropertyInteger", "n2", "Base")
		obj.addProperty("App::PropertyInteger", "n3", "Base")
		obj.n1 = 1
		obj.n2 = 1
		obj.n3 = 1

		ViewProvider(obj.ViewObject)

	def execute(proxy, obj):
		createShape(obj)


def createFilledFace(name="MyFilledFace"):
	'''create a FilledFace object'''

	ffobj = FreeCAD.activeDocument().addObject(
		"Part::FeaturePython", name)
	FilledFace(ffobj)
	return ffobj


if __name__ == '__main__':

	b = FreeCAD.activeDocument().addObject(
		"Part::FeaturePython", "MyFilledFace")
	FilledFace(b)
	'''
	b.e1 = App.ActiveDocument.Sketch
	b.e2 = App.ActiveDocument.Sketch001
	b.e3 = App.ActiveDocument.Sketch002
	b.n1 = 1
	b.n2 = 1
	b.n3 = 1
	createShape(b)
	b.ViewObject.Transparency = 60
	'''


#if 1:

	import Draft

	pts=[FreeCAD.Vector(p) for p in [(0,0,0),(100,0,0),(300,200,100)]]
	w1=Draft.makeBSpline(pts)

	pts=[FreeCAD.Vector(p) for p in [(0,0,0),(100,200,0),(300,200,100)]]
	w2=Draft.makeBSpline(pts)

	import nurbswb.filledface
	from nurbswb.filledface import createFilledFace

	ff=createFilledFace()
	ff.e1=w1
	ff.e2=w2
	App.activeDocument().recompute()
