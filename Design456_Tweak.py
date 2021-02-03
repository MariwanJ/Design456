import ImportGui
import FreeCAD as App
import FreeCADGui as Gui
import Design456Init
from PySide import QtGui, QtCore # https://www.freecadweb.org/wiki/PySide
import Draft
import Part
from draftguitools import gui_move
from draftutils.messages import _msg, _err
from draftutils.translate import translate

#Modify this command to be TWEAK 
class Design456_Tweak:
	def __init__(self):
		#super(Design456_Tweak, self).__init__()
		return
	def Activated(self):
		try:
			move_subshapes()
			#super(Design456_Tweak, self).Activated()
			return
		except ImportError as err:
			App.Console.PrintError("'ExtrudeFace' Failed. "
								   "{err}\n".format(err=str(err)))

		vector = App.Vector(0,0,2)

		def was_face_selected(self,face, selected_vertexes):
			for v in face.Vertexes:
				if was_vertex_selected(v, selected_vertexes):
					return True
			return False

		def was_edge_selected(self,edge, selected_vertexes):
			for v in edge.Vertexes:
				if was_vertex_selected(v, selected_vertexes):
					return True
			return False

		def was_vertex_selected(self,v, selected_vertexes):
			for sv in selected_vertexes:
				if v.X == sv.X and v.Y == sv.Y and v.Z == sv.Z:
					return True
			return False

		def move_subshapes(self,vector):
			sel=Gui.Selection.getSelectionEx()
			
			objects={}
			
			for s in sel:
				if not s.Object.Name in objects:
					objects[s.Object.Name]=[]
				if s.SubObjects:
					objects[s.Object.Name].extend(s.SubObjects)
			
			for name in objects: # for each object
			
				# collect all selected vertexes
				selected_vertexes=[]
				for se in objects[name]:
					selected_vertexes.extend(se.Vertexes)
				print(selected_vertexes)

				# get the object and its shape
				obj = App.ActiveDocument.getObject(name)
				shape = obj.Shape.copy()

				# check which face contains selected vertexes
				selected_faces = []
				non_selected_faces = []
				i=1
				for face in shape.Faces: # for every face
					if was_face_selected(face, selected_vertexes):
						selected_faces.append(str(i))
					else:
						non_selected_faces.append(face)
					i += 1
				print(selected_faces)	 
				print(non_selected_faces)	 

				new_faces = []
				# obtain new faces from selected ones
				for face_index in selected_faces:
					face = obj.getSubObject("Face"+ face_index)
					# check which edge has been touched
					i=1
					new_edges = []
					for edge in face.OuterWire.Edges:
						if edge.Curve.TypeId != 'Part::GeomLine':
							print("command works only with straight edges")
							return
						if was_edge_selected(edge, selected_vertexes):
							print("Face"+ face_index + " Touched edge index: "+ str(i) )
							new_edge_vertexes = []
							for v in edge.Vertexes:
								if was_vertex_selected(v, selected_vertexes):
									new_edge_vertexes.append((v.X + vector.x, v.Y + vector.y, v.Z + vector.z)) 
									# to be added with the translation vector
								else:
									new_edge_vertexes.append((v.X, v.Y, v.Z))
							e = Part.makeLine(new_edge_vertexes[0], new_edge_vertexes[1])
							new_edges.append(e)
						else:
							print("Face"+ face_index + " Non touched edge index: "+ str(i) )
							new_edges.append(edge)

						i += 1

					# create the new face
					w = Part.Wire(new_edges)
					f = Part.Face(w)
					new_faces.append(f)
					#Part.show(f)
				new_faces.extend(non_selected_faces)
				
				shell = Part.makeShell(new_faces)
				solid = Part.makeSolid(shell)
				Part.show(solid)
		disp = App.Vector(10,0,0)
		move_subshapes(disp)
			

	def GetResources(self):
		return {
				'Pixmap' : Design456Init.ICON_PATH + '/Tweak.svg',
				'MenuText': 'Tweak',
				'ToolTip':	'Tweak the Object'
				}
Gui.addCommand('Design456_Tweak', Design456_Tweak())