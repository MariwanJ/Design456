'''
create a bspline surface over a list of curves
the curves are expected in the clones group

'''



import FreeCAD as App
import FreeCADGui as Gui
,Part



def run():
    allpts=[]
    # for obj in Gui.Selection.getSelection():


    for obj in App.ActiveDocument.clones.OutList:
        if obj.Label.startswith('t='):
            exec(obj.Label)
            #print t
            #print y.Placement
            obj.Placement=t #.inverse()


        print (len(obj.Shape.Edge1.Curve.getPoles()))
        pts=obj.Shape.Edge1.Curve.discretize(30)
        allpts.append(pts)

    bs=Part.BSplineSurface()
    bs.interpolate(allpts)
    sp=App.ActiveDocument.addObject("Part::Spline","Spline")
    sp.Shape=bs.toShape()
