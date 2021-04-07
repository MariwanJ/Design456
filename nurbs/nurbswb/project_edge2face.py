


import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui


from PySide import QtGui
import Part,Mesh,Draft,Points


def run():

	try:
		[sourcex,targetx]=Gui.Selection.getSelectionEx()
		s=sourcex.SubObjects[0]
		f=targetx.SubObjects[0]

	except:
		[source,target]=Gui.Selection.getSelection()

		s=source.Shape.Edge1
		f=target.Shape.Face1

	p=f.makeParallelProjection(s, App.Vector(0,0,1))
	Part.show(p)



def OLDrunAll():

		wires=[]
		alls=Gui.Selection.getSelection()
		target=alls[-1]
		for source in alls[:-1]:
			for s in source.Shape.Edges:

				f=target.Shape.Face1

				p=f.makeParallelProjection(s, App.Vector(0,0,1))
				wires += p.Wires[0].Edges
#				print p.Vertexes[0].Point
#				print p.Vertexes[1].Point
#				Part.show(p)

		Part.show(Part.Compound(wires))
		FreeCAD.w=wires

		#---------------------------------


		wsort=[wires[0]]
		for i,w  in enumerate(wires):
			if i==0: continue
			w2=wsort[-1]
			print min(
				(w.Vertexes[0].Point-w2.Vertexes[0].Point).Length,
				(w.Vertexes[1].Point-w2.Vertexes[0].Point).Length,
				(w.Vertexes[0].Point-w2.Vertexes[1].Point).Length,
				(w.Vertexes[1].Point-w2.Vertexes[1].Point).Length,
				)
			if (w.Vertexes[0].Point-w2.Vertexes[1].Point).Length< 0.1:
				wsort += [w]
			elif (w.Vertexes[0].Point-w2.Vertexes[0].Point).Length< 0.1:
				wsort += [w]
			elif (w.Vertexes[1].Point-w2.Vertexes[1].Point).Length< 0.1:
				print "gedreht"
				w.reverse()
				wsort += [w]
			elif (w.Vertexes[1].Point-w2.Vertexes[0].Point).Length< 0.1:
				print "gedreht"
				w.reverse()
				wsort += [w]

			else:
				print "Fehler"
				raise Exception("Gehrte")


		w=Part.Wire(wsort)
		Part.show(w)

		
		#----------------------------------
		
#		ww=Part.__sortEdges__(wires)
#		FreeCAD.ww=ww
#		FreeCAD.wires=wires
#		assert len(ww) == len(wires)
		
#		w=Part.Wire(ww)
#		Part.show(w)
		pts=w.discretize(200)
		Draft.makeBSpline(pts)

def runAll():

		pointgrps=[]
		wires=[]
		alls=Gui.Selection.getSelection()
		target=alls[-1]
		for source in alls[:-1]:
			
			pgs=[]
			for s in source.Shape.Edges:

				f=target.Shape.Face1

				p=f.makeParallelProjection(s, App.Vector(0,0,1))
				wires += p.Wires[0].Edges
#				print p.Vertexes[0].Point
#				print p.Vertexes[1].Point
##				Part.show(p)
				print "Diskret"
				pgs += p.Wires[0].discretize(200)
#				Draft.makeWire(p.Wires[0].discretize(200))

			pointgrps += [pgs]

#		Part.show(Part.Compound(wires))
		FreeCAD.w=wires
		FreeCAD.pointgrps=pointgrps
		concatenateWires(pointgrps)
		return


		#---------------------------------

		pointgrps=[]

		wsort=[wires[0]]
		for i,w  in enumerate(wires):
			if i==0: continue
			w2=wsort[-1]
			print min(
				(w.Vertexes[0].Point-w2.Vertexes[0].Point).Length,
				(w.Vertexes[1].Point-w2.Vertexes[0].Point).Length,
				(w.Vertexes[0].Point-w2.Vertexes[1].Point).Length,
				(w.Vertexes[1].Point-w2.Vertexes[1].Point).Length,
				)
			if (w.Vertexes[0].Point-w2.Vertexes[1].Point).Length< 0.1:
				wsort += [w]
			elif (w.Vertexes[0].Point-w2.Vertexes[0].Point).Length< 0.1:
				wsort += [w]
			elif (w.Vertexes[1].Point-w2.Vertexes[1].Point).Length< 0.1:
				print "gedreht"
				w.reverse()
				wsort += [w]
			elif (w.Vertexes[1].Point-w2.Vertexes[0].Point).Length< 0.1:
				print "gedreht"
				w.reverse()
				wsort += [w]

			else:
				print "Fehler"
				raise Exception("Gehrte")

			w=Part.Wire(wsort)
#			Part.show(w)


			#----------------------------------
			
	#		ww=Part.__sortEdges__(wires)
	#		FreeCAD.ww=ww
	#		FreeCAD.wires=wires
	#		assert len(ww) == len(wires)
			
	#		w=Part.Wire(ww)
	#		Part.show(w)

			pts=w.discretize(200)
			pointgrps +=[pts]

			Draft.makeBSpline(pts)

#		concatenateWires(pointgrps)



def concatenateBSplines():
	''' Draft BSsplines  zusammenfuegen'''

	import Draft
	
	wires=[]
	for s in Gui.Selection.getSelection():
		wires += [s.Points]
		print wires
		print s.Label

	concatenateWires(wires)


def concatenateWires(wires):

	pts=wires[0]

#	print pts
#	print  wires[0][0]
#	print  wires[1][1]

	dista= min(
				(wires[0][0]-wires[1][0]).Length,
				(wires[0][0]-wires[1][-1]).Length,
				(wires[0][-1]-wires[1][0]).Length,
				(wires[0][-1]-wires[1][-1]).Length
			)


	if dista == (wires[0][0]-wires[1][0]).Length or  dista == (wires[0][0]-wires[1][-1]).Length:
		print "Drehe Start"
		pts.reverse()

	wa=pts

	for w in wires[1:]:
		dista= min(
					(wa[-1]-w[0]).Length,
					(wa[-1]-w[-1]).Length,
				)
		wb=w
		if dista == (wa[-1]-w[-1]).Length:
			print "Drehe"
			wb.reverse()

		pts += wb
		wa = wb

	print len(pts)

	pts2=[]
	for i,p in enumerate(pts):
		if  (p-pts[i-1]).Length<0.001:
			print "Doppel",i
			print (p-pts[i-1]).Length
		else:
			pts2 += [p]


	import Draft
	Draft.makeWire(pts2)
	Draft.makeBSpline(pts2)






import numpy as np

def splitCurve():
	# split an recombine curve
	sw=Gui.Selection.getSelection()[0]
	
	w=sw.Shape.Edges[0]
	#App.ActiveDocument.BSpline001.Shape

	step=10
	anz=int(round(w.Curve.length()/step+1))
	pts=w.discretize(anz)

	pxy=[FreeCAD.Vector(p.x,p.y,0) for p in pts]

	for i in range(anz):
		print (pts[i]-pts[i-1]).Length

	len=round(w.Curve.length()+1)/anz

	psz=[FreeCAD.Vector(len*i,0,p.z) for i,p in enumerate(pts)]
	psz=[FreeCAD.Vector(0,len*i,p.z) for i,p in enumerate(pts)]

	# split
	wsz=Draft.makeWire(psz)
	wxy=Draft.makeWire(pxy)


def combineCurve():
	# recombine
	[wsz,wxy]=Gui.Selection.getSelection()
	pts=[FreeCAD.Vector(b.x,b.y,a.z) for a,b in zip(wsz.Points,wxy.Points)]
	aa=Draft.makeWire(pts)
	ptsb=aa.Shape.discretize(40)
	Draft.makeBSpline(ptsb)
	
	for i,p in enumerate(pts):
		if i == 0:  ptsa = []
		else:
			t=p-pts[i-1]
			t.normalize()
			t*=10
			n=FreeCAD.Vector(0,0,1)
			h=t.cross(n).normalize() *10
			
			ptsa += [p,p+h,pts[i-1]+h,pts[i-1]-h,p-h,p] 

	Draft.makeWire(ptsa)
	
	


