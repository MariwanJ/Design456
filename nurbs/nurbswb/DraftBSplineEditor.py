from PySide import QtGui, QtCore

from PySide.QtCore import *
from PySide.QtGui import *

import numpy as np
import time
 
import FreeCAD,FreeCADGui,Part,Draft



# methods for the 3D object interface
def getArr(obj,scale=1):
	arr=[[p.x,p.y,p.z] for p in obj.Points]
	return np.array(arr)/scale

def setArr(arr,obj,scale=1):
	obj.Points=[FreeCAD.Vector(tuple(p)) for p in arr*scale]
	FreeCAD.ActiveDocument.recompute()




def np2tab(arr,tab):
	(xc,yc)=arr.shape
	for x in range(xc):
		for y in range(yc):
			newitem = QTableWidgetItem(str(arr[x,y]))
			tab.setItem(x, y, newitem)

def tab2np(tab):
	arr=[]
	rc=tab.rowCount()
	cc=tab.columnCount()
	for r in range(rc):
		for c in range(cc):
			arr.append(float(tab.item(r,c).text().replace(',', '.')))
	return np.array(arr).reshape(rc,cc)


def itemChanged(widget,*args):
	arr=tab2np(widget.table)
	widget.data=arr
	widget.target.update(arr,scale=widget.scale)
	rowcol(widget)


class MyTable(QTableWidget):
	def __init__(self, data, *args):
		QTableWidget.__init__(self, *args)
		self.data = data
		self.setdata()


	def setdata(self):
		(xc,yc)=self.data.shape
		for x in range(xc):
			for y in range(yc):
				newitem = QTableWidgetItem(str(self.data[x,y]))
				self.setItem(x, y, newitem)

		horHeaders=['x','y','z']
		self.setHorizontalHeaderLabels(horHeaders)


def pressed(index):
	print ("pressed",index.column(),index.row())

def rowcol(w,*args):
	print ("selection row/column changed")


	print (w,args)
	for i in w.table.selectedItems():
		print (i.row(),i.column())

	pts=[]
	for i in w.table.selectedItems():
		print (i.row(),i.column())
		pts.append(FreeCAD.Vector(w.data[i.row()]))

	print "huhuhuhsfsdfdf u"
	print pts
	print "selection changed ---------------",w.scale
	w.selection.update(pts,scale=w.scale)
	print "-----------------"

def rowcol2(w,*args):
	print ("2-------------------selection row/column changed")


	print (w,args)
	for i in w.table.selectedItems():
		print (i.row(),i.column())

	pts=[]
	for i in w.table.selectedItems():
		print (i.row(),i.column())
		pts.append(FreeCAD.Vector(w.data[i.row()]))
	print "huhuhuhu"
	print pts
	print "selection changed ---------------",w.scale
	w.selection.update(pts,scale=w.scale)
	print "-----------------"

def posfromsel(w):
	t=FreeCADGui.Selection.getSelectionEx()[0]
	v=t.PickedPoints[0]

	for i in w.table.selectedItems():
		print (i.row(),i.column())
#		v=[3,4,5]
		c=i.column()
		i.setText(str(v[c]))


def button(widget):
	arr=tab2np(widget.table)
	widget.setArr(arr,widget.obj,scale=widget.scale)
	widget.target.update(arr,scale=widget.scale)

def reload(widget):
	arr=getArr(widget.obj,scale=widget.scale)
	np2tab(arr,widget.table)

def die(widget):
	widget.target.die()
	widget.selection.die()
	widget.close()


class MyTarget():
	''' visualization of the dialog data'''

	def __init__(self):
		self.obj=FreeCAD.ActiveDocument.addObject("Part::Feature","__tmp" +str(time.time()))
		self.obj.ViewObject.PointSize=10
		self.obj.ViewObject.PointColor=(0.,0.,1.)
		self.obj.ViewObject.LineColor=(0.,0.,1.)

	def update(self,coor=[0,0,0],scale=1):
		pts=[FreeCAD.Vector(tuple(c)) for c in np.array(coor)*scale]
		try: 
			pol=Part.makePolygon(pts)
			self.obj.Shape=pol
		except: 
			pol=[]
			#vts=[Part.Vertex(pp) for pp in pts]
			#comp=Part.makeCompound(vts)
			if len(pts)>0:
				self.obj.Shape=Part.Vertex(pts[0]) 

	def die(self):
		try: FreeCAD.ActiveDocument.removeObject(self.obj.Name)
		except: pass



def pointEditor(obj,scale=1):

	w=QtGui.QWidget()
	box = QtGui.QVBoxLayout()
	w.setLayout(box)
	w.setGeometry(50, 30, 350, 630)
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	dt=Draft.getType(obj)
	if dt in ['BSpline','Wire','BezCurve']:
		w.setArr=setArr
		w.getArr=getArr
	else: 
		raise Exception("Unhandled type " + dt)

	w.scale=scale
	w.obj=obj
	arr=getArr(obj,scale=w.scale)
	w.data=arr/w.scale
	rs=arr.shape[0]


	w.target=MyTarget()
	w.target.update(arr,scale)
	
	w.selection=MyTarget()
	w.selection.obj.ViewObject.PointSize=15
	w.selection.obj.ViewObject.PointColor=(2.,0.,0.)


	w.table = MyTable(arr,rs,3)
	w.table.pressed.connect(pressed)
	y=lambda a,b: rowcol(w,a,b)
	y=lambda: rowcol(w)
	y2=lambda: rowcol2(w)
	w.table.currentCellChanged.connect(y2)
	w.table.itemSelectionChanged.connect(y)
	

	w.table.itemSelectionChanged.connect(lambda:itemChanged(w))
	w.table.itemChanged.connect(lambda:itemChanged(w))


	l=QtGui.QLabel("Editor Points of: " + obj.Label)
	box.addWidget(l)

	box.addWidget(w.table)

	b=QtGui.QPushButton("Get Pos from Selection")
	b.pressed.connect(lambda:posfromsel(w))
	box.addWidget(b)


	b=QtGui.QPushButton("Reload")
	b.pressed.connect(lambda:reload(w))
	box.addWidget(b)

	b=QtGui.QPushButton("Apply Table")
	b.pressed.connect(lambda:button(w))
	box.addWidget(b)

	b=QtGui.QPushButton("Close")
	b.pressed.connect(lambda:die(w))
	box.addWidget(b)

	w.show()
	return w


def run(scale=1):
	print "RUN ---",scale
	obj=FreeCADGui.Selection.getSelection()[0]
	print obj
	return pointEditor(obj,scale=scale)


def run2():
	#create the Bspline
	p1 = FreeCAD.Vector(0,0,0)
	p2 = FreeCAD.Vector(1,1,0)
	p3 = FreeCAD.Vector(0,2,0)
	p4 = FreeCAD.Vector(-1,1,0)
	p5 = FreeCAD.Vector(-1,1,3)
	
	import Draft
	Draft.makeBSpline([p1,p2,p3,p4,p5],closed=True)
	obj=FreeCAD.ActiveDocument.ActiveObject
	w=pointEditor(obj)
	w.show()
	return w

if __name__=='__main__':
	run()
