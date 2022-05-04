[1mdiff --git a/DirectModeling/Design456_SmartExtrudeRotate.py b/DirectModeling/Design456_SmartExtrudeRotate.py[m
[1mindex 46b5714..d55eb40 100644[m
[1m--- a/DirectModeling/Design456_SmartExtrudeRotate.py[m
[1m+++ b/DirectModeling/Design456_SmartExtrudeRotate.py[m
[36m@@ -114,9 +114,9 @@[m [mdef callback_Rotate(userData: fr_degreewheel_widget.userDataObject = None):[m
             #TODO:EXPERIMENTAL CODE : FIXME:[m
             nor = faced.getNormalized(linktocaller.ExtractedFaces[0])[m
             bas = faced.getBase(linktocaller.ExtractedFaces[0])[m
[31m-            # linktocaller.wheelObj.w_Rotation[0] = nor.x[m
[31m-            # linktocaller.wheelObj.w_Rotation[1] = nor.y[m
[31m-            # linktocaller.wheelObj.w_Rotation[2] = nor.z[m
[32m+[m[32m            linktocaller.wheelObj.w_Rotation[0] = bas.x[m
[32m+[m[32m            linktocaller.wheelObj.w_Rotation[1] = bas.y[m
[32m+[m[32m            linktocaller.wheelObj.w_Rotation[2] = bas.z[m
 [m
     if (linktocaller.RotateLBL is not None):[m
         linktocaller.RotateLBL.setText("Rotation Axis= " + "(" +[m
[36m@@ -680,11 +680,11 @@[m [mclass Design456_SmartExtrudeRotate:[m
             if self.faceDir == "+z" or self.faceDir == "-z":[m
                 self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str[m
                     (0.0) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0],[m
[31m-                    self.setupRotation, [2.0, 2.0, 2.0], 2,facingdir)[m
[32m+[m[32m                    self.setupRotation, [5.0, 5.0, 5.0], 2,facingdir)[m
             else:[m
                 self.wheelObj = Fr_DegreeWheel_Widget([self.FirstLocation, App.Vector(0, 0, 0)], str([m
                     0.0) + "°", 1, FR_COLOR.FR_RED, [0, 0, 0, 0],[m
[31m-                    self.setupRotation, [2.0, 2.0, 2.0], 1,facingdir)[m
[32m+[m[32m                    self.setupRotation, [5.0, 5.0, 5.0], 1,facingdir)[m
 [m
             # Define the callbacks. We have many callbacks here.[m
             # TODO: FIXME:[m
