#***************************************************************************
#*																		   *
#*	Open source - FreeCAD												   *
#*	Design456 Workbench													   *
#*	Auth : Mariwan Jalal and others										   *
#***************************************************************************
import os
import FreeCAD as App
__dir__ = os.path.dirname(__file__)
ICON_PATH = os.path.join( __dir__, 'Resources/icons' )
IMAGE_PATH = os.path.join( __dir__, 'Resources/images' )
TABLE_PATH = os.path.join( __dir__, 'tables' )
#PART
App.addImportType("BREP format (*.brep *.brp)","Part")
App.addExportType("BREP format (*.brep *.brp)","Part")
App.addImportType("IGES format (*.iges *.igs)","Part")
App.addExportType("IGES format (*.iges *.igs)","Part")
App.addImportType("STEP with colors (*.step *.stp)","Import")
App.addExportType("STEP with colors (*.step *.stp)","Import")

App.__unit_test__ += [ "TestPartApp" ]
