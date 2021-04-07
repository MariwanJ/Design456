# nurbs tools


import Part

def showIsoparametricUCurve(bsplinesurface,u=0.5):
	''' create a curve in 3D space '''
	bc=bsplinesurface.uIso(u)
	Part.show(bc.toShape())

def showIsoparametricVCurve(bsplinesurface,v=0.5):
	''' create a curve in 3D space '''
	bc=bsplinesurface.vIso(v)
	Part.show(bc.toShape())

# nurbswb lib
# sammlung von funktionen


def kruemmung(sf,u,v):
	'''calculate  curvature'''
	# aus tripod_2.py
	d=0.01
	d=0.0001
	t1,t2=sf.tangent(u,v)
	if t1 == None or t2 == None:
		print ("keine Tagenten fuer ",u,v) 
		return -1,-1

	t1=t1.multiply(d)
	t2=t2.multiply(d)
	
	vf=sf.value(u,v)

	vfw=vf+t1
	uu,vv=sf.parameter(vfw)
	vfw=sf.value(uu,vv)

	vfe=vf-t1
	uu,vv=sf.parameter(vfe)
	vfe=sf.value(uu,vv)

	ku=(vfw+vfe-vf-vf)
	ddu=(vfw-vf).Length
	ku= ku.multiply(1.0/ddu/ddu)

	vfn=vf+t2
	uu,vv=sf.parameter(vfn)
	vfn=sf.value(uu,vv)

	vfs=vf-t2
	uu,vv=sf.parameter(vfs)
	vfs=sf.value(uu,vv)

	kv=(vfn+vfs-vf-vf)
	ddv=(vfn-vf).Length
	kv= kv.multiply(1.0/ddv/ddv)

	#ku=round(ku.Length,3)
	#kv=round(kv.Length,3)
	# print ku
	ku=-ku.z
	kv=-kv.z

	ru=None
	rv=None
	if ku!=0: ru=round(1/ku,3)
	if kv!=0: rv=round(1/kv,3)

	# print ("Krmmungen:",ku,kv,"Krmmungsradien:", ru,rv)


	return ku,kv

#-------------------------------


