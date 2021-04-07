import FreeCAD,FreeCADGui, Part
App=FreeCAD
Gui=FreeCADGui




import random

def run():
	sel=Gui.Selection.getSelection()

	face=sel[0].Shape.Face1.Surface.toShape()
	# Part.show(face)

	#face=sel[0].Shape.Face1

	wireobs=sel[1:]

	print face
	wires=[]
	for w in wireobs:
		print w.Shape.Wires
		wires += [w.Shape.Wires[0]]


	es=wires
	if len(es)>0:
			splita=[]
			for i,e in enumerate(es):

				edges=e.Edges
				ee=edges[0]
				# if dirs[i]: ee.reverse()

				e.reverse()
				splita += [(e,face)]

			r=Part.makeSplitShape(face, splita)
			print r
			for fs in r:
				for f in fs:
					Part.show(f)
					App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
							random.random(),random.random(),random.random(),)


	else:
		Part.show(face)
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(
							random.random(),random.random(),random.random(),)




def extractWires():
	'''extract the wires'''
	sel=Gui.Selection.getSelection()
	w=sel[0]
	print w.Shape.Wires
	for i,wire in  enumerate(w.Shape.Wires):
		Part.show(wire)
		App.ActiveDocument.ActiveObject.Label="wire " + str(i+1) +" for "+  w.Label +" "
		wire.reverse()
		Part.show(wire)
		App.ActiveDocument.ActiveObject.Label="wire " + str(i+1) +" for " +  w.Label +" reverse "
		
