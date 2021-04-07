
import FreeCAD as App
import FreeCADGui as Gui


def run():
    ''' auxiliary method applies placement from the label,
     to move objects (sketch) to the desired place in the room'''

    for y in Gui.Selection.getSelection():
        if y.Label.startswith('t='):
            exec(y.Label)
            print (t)
            print (y.Placement)
            y.Placement=t #.inverse()
