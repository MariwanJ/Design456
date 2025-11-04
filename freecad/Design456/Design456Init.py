# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileCopyrightText: 2025 Mariwan Jalal ( mariwan.jalal@gmail.com )
# SPDX-FileNotice: Part of the Design456 addon.

from __future__ import unicode_literals

import os,sys
import FreeCAD as App
from draftutils.translate import translate   #for translate
"""
This file will add all paths needed for the Design456.
It makes life easier. By doing that you can import any file
in any of the subdirectories. Adding more subdirectories
needs be added here. 
ICON path should be always added as below 
'Resources/icons/' 

"""

__updated__ = '2022-10-05 20:55:16'


#Design456 
__dir__ = os.path.dirname(__file__)
ICON_PATH = os.path.join(__dir__, 'Resources/icons/')
IMAGE_PATH = os.path.join(__dir__, 'Resources/images/')
IMPORT_PATH= os.path.join(__dir__, 'Imported/')
UI_PATH = os.path.join(__dir__, 'Resources/ui/')
PATH_PREF=os.path.join(__dir__, 'Preferences/')
#Pyramid shapes 
PYRAMID_PATH = os.path.join(__dir__, 'PyramidMo/')
PYRAMID_ICON_PATH = os.path.join(__dir__, 'PyramidMo/Resources/icons/')

#Coin3D New widget system 
WIDGETS3D_PATH=os.path.join(__dir__,'ThreeDWidgets/')

#Direct Modeling implementation 
DIRECTMODELING_PATH=os.path.join(__dir__,'DirectModeling/')

#From DRAFT
__dirname__ = os.path.join(App.getResourceDir(), "Mod", "Draft")

# Defeaturing WB
DEFEATURING_WB = os.path.join(__dir__,'DefeaturingWB/')
DefeaturingWB_icons_path =  os.path.join( DEFEATURING_WB, 'Resources', 'icons')

# PART      #Causes issue  - Reported by luzpaz as per https://github.com/MariwanJ/Design456/issues/81#issuecomment-2306974570
#App.addImportType("BREP format (*.brep *.brp)", "Part")
#App.addExportType("BREP format (*.brep *.brp)", "Part")
#App.addImportType("IGES format (*.iges *.igs)", "Part")
#App.addExportType("IGES format (*.iges *.igs)", "Part")
#App.addImportType("STEP with colors (*.step *.stp)", "Import")
#App.addExportType("STEP with colors (*.step *.stp)", "Import")

#Desing456 WB Default  view 
#Default Extrusion direction, i.e. 2D/3D objects are placed on XY plane by default.
DefaultDirectionOfExtrusion='z' # We need to know this always. Any change in the plane should be saved here.

#Pointer to the workbench
pToWorkbench=None

App.__unit_test__ += ["TestPartApp"]
