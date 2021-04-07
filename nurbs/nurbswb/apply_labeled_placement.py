
import FreeCAD
import FreeCADGui as Gui


def run():
	''' hilfsmethode wendet Placement aus dem Label an, 
	um Objekte(Sketch) an die gewuenschte Stelle im Raum zu verschieben'''

	for y in Gui.Selection.getSelection():
		if y.Label.startswith('t='):
			exec(y.Label)
			print t
			print y.Placement
			y.Placement=t #.inverse()
