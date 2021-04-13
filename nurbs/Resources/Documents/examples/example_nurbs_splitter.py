# run first nurbs.py with randomB test
 
import os

try:
    import numpy as np 
except ImportError:
    print ("Trying to Install required module: numpy")
    os.system('python -m pip3 install numpy')
import Draft

ps=App.ps
ps.reshape(20,10,3)
bs=App.ActiveDocument.Nurbs.Proxy.bs
poles=np.array(bs.getPoles())
# poles.reshape(20,10,3)


uknots=bs.getUKnots()
vknots=bs.getVKnots()


kps=[]
for u in uknots:
    for v in vknots:
        kps.append(bs.value(u,v))

kps=np.array(kps)
kps=kps.reshape(len(uknots),len(vknots),3)

kps.shape
# gitter der knoten
polygons=[]
for u in range(len(uknots)):
    pts=[App.Vector(tuple(v)) for v in kps[u]]
    #Draft.makeWire(pts)
    polygons.append(Part.makePolygon(pts))

kpsv=kps.swapaxes(0,1)


for t in range(len(vknots)):
    pts=[App.Vector(tuple(v)) for v in kpsv[t]]
    #Draft.makeWire(pts)
    polygons.append(Part.makePolygon(pts))

comp=Part.makeCompound(polygons)
Part.show(comp)


# zerlegen in 5 teilflaechen 
def segment(bs,iu,lu,iv,lv):
    bs2=bs.copy()
    bs2segment(uknots[iu],uknots[iu+lu],vknots[iv],vknots[iv+lv])
    Part.show(bs2.toShape())
    return bs2




bseg=segment(bs,3,2,2,9)
egs=App.ActiveDocument.ActiveObject.Shape.Edges
ff=App.ActiveDocument.ActiveObject.Shape.Faces[0]
pp=bseg.getPoles()

mau=len(uknots)
mav=len(vknots)



segment(bs,0,3,0,mav-1)
segment(bs,3+2,mau-1-3-2,0,mav-1)

segment(bs,3,2,0,2)
segment(bs,3,2,2+9,mav-1-2-9)

pp=np.array(pp)
pp.shape





# volumenkoerper aus flaeche
def createSocket(obj):
    egs=obj.Shape.Edges
    ffs=[ff]
    b=[]
    odds=[]
    for e in egs:
        p1=e.Vertexes[0].Point
        p2=e.Vertexes[1].Point
        p3=App.Vector(p2)
        p3.z = -100
        if p3 not in b:
            b.append(p3)
        p4 = App.Vector(p1)
        p4.z = -100
        if p4 not in b:
            b.append(p4)

        pol=Part.makePolygon([p1,p4,p3,p2])
        Part.show(pol)
        pj=App.ActiveDocument.ActiveObject
        Part.show(e)
        ej=App.ActiveDocument.ActiveObject


        Draft.upgrade([pj,ej],delete=True)
        ej=App.ActiveDocument.ActiveObject
        Draft.upgrade(ej,delete=True)
        ffs.append(App.ActiveDocument.ActiveObject.Shape.Faces[0])
        odds.append(App.ActiveDocument.ActiveObject)

    b.append(b[0])
    pol=Part.makePolygon(b)
    Part.show(pol)
    ej=App.ActiveDocument.ActiveObject
    Draft.upgrade(ej,delete=True)
    ffs.append(App.ActiveDocument.ActiveObject.Shape.Faces[0])
    odds.append(App.ActiveDocument.ActiveObject)

    ss=Part.makeShell(ffs)
    so=Part.makeSolid(ss)
    Part.show(so)

    for j in odds:  
        App.ActiveDocument.removeObject(j.Name)


