#add new widget to the main windows
'''
The FreeCAD 3D visualization basically works like this:

    There is a general rectangular Area in which everything is rendered with OpenGL.
     This is what you see as 3D view. This are is a QT widget called QGraphicsView.
      The widget is embedded in the overall UI, and allows to render all kinds of opengl stuff in it.
    One thing that is rendered onto the QGraphicsView is the Coin3D scene graph. 
    Hence in this step, everything thats in the scene graph is put onto the render area
    Other things can than be rendered on top of that. There are some spare examples around over freeCAD, 
    for example the FEM postprocessing scales. Basically anything OpenGL can be drawn

This means for your idea you have 2 options: First to add everything you need to the scenegraph,
 and use coin to achieve your functionality. Or second, use OpenGL to draw everything ontop afterwards.

The second step is made very easy by the fact, that a QGraphicsView allows to add default QtWidgets to it which are than rendered via opengl. here is a simple example (works when you have a document open): 
'''
from PySide2 import QtWidgets

def findInChildren(obj, searched):
	for child in obj.children():
		if isinstance(child, searched):
			return child
		else: 
			res = findInChildren(child, searched)
			if res:
				return res

	return None

view = findInChildren(Gui.getMainWindow(), QtWidgets.QGraphicsView)
widget = QtWidgets.QLineEdit()

proxy = view.scene().addWidget(widget)







        self.view.removeEventCallbackPivy( coin.SoLocation2Event.getClassTypeId(), self.cursorCB)
        self.view.removeEventCallbackPivy( coin.SoKeyboardEvent.getClassTypeId(), self.keyboardCB)
        self.view.removeEventCallbackPivy( coin.SoMouseButtonEvent.getClassTypeId(), self.clicCB)
        
        
        
        
         if (type(event) == coin.SoKeyboardEvent):
            key = ""
            try:
                key = event.getKey()
            except ValueError:
                # there is no character for this value
                key = ""
            if key == coin.SoKeyboardEvent.LEFT_CONTROL:
                if event.getState() == coin.SoButtonEvent.DOWN:
                    self.snap = True
                elif event.getState() == coin.SoButtonEvent.UP:
                    self.snap = False
            elif key == coin.SoKeyboardEvent.RETURN:
                self.accept()
                self.finish()
            elif key == coin.SoKeyboardEvent.BACKSPACE and event.getState() == coin.SoButtonEvent.UP:
                self.removePole()
            elif key == coin.SoKeyboardEvent.I and event.getState() == coin.SoButtonEvent.UP:
                self.increaseDegree()
            elif key == coin.SoKeyboardEvent.D and event.getState() == coin.SoButtonEvent.UP:
                self.decreaseDegree()
            elif key == coin.SoKeyboardEvent.ESCAPE:
                self.abort()
                self.finish()
                
                





App.newDocument()
v=Gui.activeDocument().activeView()
 
#This class logs any mouse button events. As the registered callback function fires twice for 'down' and
#'up' events we need a boolean flag to handle this.
class ViewObserver:
   def __init__(self, view):
       self.view = view
   
   def logPosition(self, info):
       down = (info["State"] == "DOWN")
       pos = info["Position"]
       if (down):
           FreeCAD.Console.PrintMessage("Clicked on position: ("+str(pos[0])+", "+str(pos[1])+")\n")
           pnt = self.view.getPoint(pos)
           FreeCAD.Console.PrintMessage("World coordinates: " + str(pnt) + "\n")
           info = self.view.getObjectInfo(pos)
           FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n")
o = ViewObserver(v)
c = v.addEventCallback("SoMouseButtonEvent",o.logPosition)






 if (type.isDerivedFrom(SoLocation2Event::getClassTypeId())) {
     this->lockrecenter = TRUE;
     const SoLocation2Event * const event = (const SoLocation2Event *) ev;
     if (this->currentmode == NavigationStyle::ZOOMING) {
         this->zoomByCursor(posn, prevnormalized);
         processed = TRUE;getObjectInfo
     }
     else if (this->currentmode == NavigationStyle::PANNING) {
         float ratio = vp.getViewportAspectRatio();
         panCamera(viewer->getCamera(), ratio, this->panningplane, posn, prevnormalized);
         processed = TRUE;
     }
     else if (this->currentmode == NavigationStyle::DRAGGING) {
         this->addToLog(event->getPosition(), event->getTime());
         this->spin(posn);
         processed = TRUE;
     }
 }




 // Keyboard handling
if (type.isDerivedFrom(SoKeyboardEvent::getClassTypeId())) {
    const SoKeyboardEvent * const event = (const SoKeyboardEvent *) ev;
    const SbBool press = event->getState() == SoButtonEvent::DOWN ? TRUE : FALSE;
    switch (event->getKey()) {
    case SoKeyboardEvent::LEFT_CONTROL:
    case SoKeyboardEvent::RIGHT_CONTROL:
        this->ctrldown = press;
        break;
    case SoKeyboardEvent::LEFT_SHIFT:
    case SoKeyboardEvent::RIGHT_SHIFT:
        this->shiftdown = press;
        break;
    case SoKeyboardEvent::LEFT_ALT:
    case SoKeyboardEvent::RIGHT_ALT:
        this->altdown = press;
        break;
    case SoKeyboardEvent::H:
        processed = TRUE;
        viewer->saveHomePosition();
        break;
    case SoKeyboardEvent::S:
    case SoKeyboardEvent::HOME:
    case SoKeyboardEvent::LEFT_ARROW:
    case SoKeyboardEvent::UP_ARROW:
    case SoKeyboardEvent::RIGHT_ARROW:
    case SoKeyboardEvent::DOWN_ARROW:
        if (!this->isViewing())
            this->setViewing(true);
        break;
    default:
        break;
    }
}





"""
    def mouseEvents(self, mouseEvent):
        #Address mouse activities.
        event = mouseEvent.getEvent()
        if event.getTypeId() == coin.SoLocation2Event.getClassTypeId():
            FreeCAD.Console.PrintMessage("We are in SoLocation2Event\n")
        elif event.getTypeId() == coin.SoMouseButtonEvent.getClassTypeId():
            FreeCAD.Console.PrintMessage("We are in SoMouseButtonEvent\n")
        else:
            
            FreeCAD.Console.PrintMessage("We are in nothing")
                def mouseEvents(self, mouseEvent):


            #Address mouse activities.
        event = mouseEvent.getEvent()
        if type(event) == coin.SoMouseButtonEvent:
            FreeCAD.Console.PrintMessage("We are in SoMouseButtonEvent")
        elif type(event) == coin.SoLocation2Event:
            FreeCAD.Console.PrintMessage("We are in SoLocation2Event")
        else:
            FreeCAD.Console.PrintMessage("We are in nothing")



   def kb_cb(self, event_callback):
        event = event_callback.getEvent()
        if (type(event) == coin.SoKeyboardEvent):
            key = ""
            try:
                key = event.getKey()
            except ValueError:
                # there is no character for this value
                key = ""
            if key == coin.SoKeyboardEvent.LEFT_CONTROL:
                if event.getState() == coin.SoButtonEvent.DOWN:
                    self.snap = True
                elif event.getState() == coin.SoButtonEvent.UP:
                    self.snap = False
            elif key == coin.SoKeyboardEvent.RETURN:
                self.accept()
                self.finish()
            elif key == coin.SoKeyboardEvent.BACKSPACE and event.getState() == coin.SoButtonEvent.UP:
                self.removePole()
            elif key == coin.SoKeyboardEvent.I and event.getState() == coin.SoButtonEvent.UP:
                self.increaseDegree()
            elif key == coin.SoKeyboardEvent.D and event.getState() == coin.SoButtonEvent.UP:
                self.decreaseDegree()
            elif key == coin.SoKeyboardEvent.ESCAPE:
                self.abort()
                self.finish()
                
class ButtonTest:
    def __init__(self):
        self.view = Gui.ActiveDocument.ActiveView
        self.callback = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.getMouseClick) 

    def getMouseClick(self, event_cb):
        event = event_cb.getEvent()
        if event.getState() == coin.SoMouseButtonEvent.DOWN:
            print("Alert!!! A mouse button has been improperly clicked!!!")
            self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(), self.callback)

ButtonTest()



SoFile.getClassId()


"""




        self.info = ["LMB : add pole",
                     "Del : remove last pole",
                     "I / D : Increase / Decrease degree",
                     "Left CTRL : snap",
                     "Enter : Accept",
                     "Esc : Abort"]
                     
                     
                     
                     
    def checkIfEventIsRelevantForWidget(self, widget):
        handelV = App.Vector(self.lastEventXYZ.Coin_x,self.lastEventXYZ.Coin_y, self.lastEventXYZ.Coin_z)
        v1 = App.Vector(widget.x, widget.y, widget.z)
        v2 = App.Vector(widget.x+widget.w, widget.y +widget.h, widget.z+widget.t)
        distance = handelV.distanceToLine(v1, v2)
        if distance == 0:
            return True
        else:
            return False