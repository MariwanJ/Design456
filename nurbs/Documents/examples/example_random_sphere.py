import nurbswb.nurbs
import numpy as np
import random

def testRandomSphere():


	na=7
	b=5

	a= nurbswb.nurbs.makeNurbs(b,na)
	a.model="NurbsSphere"

	a.solid=False
	a.base=False
	#a.grid=False
	a.gridCount=20
	
	ps=a.Proxy.getPoints()
	print "points ps",len(ps)

	if 0:
		print "random .."
		ps=np.array(FreeCAD.ps).swapaxes(0,1)
		temp,ct=ps.shape
		ps[2] += 100*np.random.random(ct)
		ps=ps.swapaxes(0,1)
	#	ps[0:3]

	ps=np.array(ps)
	ps.resize(na,b,3)
	
	for k0 in range(15):
		k=random.randint(2,na-3)
		l=random.randint(1,b-1)
		for j in range(1):
			ps[k+j][l][2] += 100*random.random()
		rj=random.randint(0,1)
		print (k,rj)
		for j in range(rj):
			ps[k+j][l][2] += 100*random.random()

	for k0 in range(10):
		k=random.randint(2,na-3)
		l=random.randint(1,b-1)

		for j in range(1):
			ps[k+j][l][2] += 200*random.random()
		rj=random.randint(0,1)
		print (k,rj)
		for j in range(rj):
			ps[k+j][l][2] += 200*random.random()


	ps.resize(na*b,3)


	a.Proxy.togrid(ps)
#	a.Proxy.elevateVline(2,0)

	a.Proxy.updatePoles()
	a.Proxy.showGriduv()
	
	FreeCAD.a=a
	FreeCAD.ps=ps

	Gui.activeDocument().activeView().viewAxonometric()
	Gui.SendMsgToActiveView("ViewFit")




testRandomSphere()
