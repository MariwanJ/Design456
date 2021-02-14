# ***************************************************************************
# *                                                                         *
# *  This file is part of the Open Source Design456 Workbench - App.    *
# *                                                                         *
# *  Copyright (C) 2021                                                     *
# *																		   *
# *                                                                         *
# *  This library is free software; you can redistribute it and/or          *
# *  modify it under the terms of the GNU Lesser General Public             *
# *  License as published by the Free Software Foundation; either           *
# *  version 2 of the License, or (at your option) any later version.       *
# *                                                                         *
# *  This library is distributed in the hope that it will be useful,        *
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# *  Lesser General Public License for more details.                        *
# *                                                                         *
# *  You should have received a copy of the GNU Lesser General Public       *
# *  License along with this library; if not, If not, see                   *
# *  <http://www.gnu.org/licenses/>.                                        *
# *                                                                         *
# *  Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# ***************************************************************************

from PySide.QtCore import QT_TRANSLATE_NOOP
import Draft_rc
import FreeCAD as App
import FreeCADGui as Gui
__title__ = "FreeCAD Design456 Workbench - Init file"
__author__ = "Yorik van Havre <yorik@uncreated.net> DRAFT PART / Mariwan Jalal <mariwan.jalal@gmail.com> for Design456"
__url__ = "https://www.freecadweb.org"

import BOPTools  # as bop


class Design456_Workbench (Workbench):
    "Design456 Workbench object"

    def __init__(self):
        import Design456Init
        self.__class__.Icon = Design456Init.ICON_PATH + '/WorkbenchIcon.svg'
        self.__class__.MenuText = "Design456"
        self.__class__.ToolTip = "A workbench easy designing objects"

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        import Design456_Extrude  # import all	 needed files
        import Design456_Extract
        import Design456_ExtrudeFace
        import Design456_SplitObject
        import Design456_loftOnDirection


        import Design456_Part as designPart
        import Design456_Part_Tools as pUtils
        # from Part import CommandShapes	 #Tube	not working
        Gui.runCommand('Std_PerspectiveCamera', 1)

        self.list = ["Design456_Extrude",
                     "Design456_Extract",
                     "Design456_ExtrudeFace",
                     "Design456_SplitObject",
                     "Design456_loftOnDirection",
                     ]
        self.appendToolbar("Design456", self.list)
        self.appendMenu("Design456", self.list)
        print(designPart.Design456_Part_ToolBar.list)
        self.appendToolbar(
            "Design456_Part", designPart.Design456_Part_ToolBar.list)
        self.appendToolbar("Design456_Part_Tools",
                           pUtils.Design456_Part_Tools.list)
        self.appendMenu("Design456_Part",
                        designPart.Design456_Part_ToolBar.list)
        self.appendMenu("Design456_Part_Tools",
                        pUtils.Design456_Part_Tools.list)
        

        # Design456_Part
        #self.appendMenu(QT_TRANSLATE_NOOP("Draft", "&Drafting"), self.drawing_commands)

        # Design456_Part
        # DRAFT
        def QT_TRANSLATE_NOOP(context, text):
            return text

        # Run self-tests
        dependencies_OK = False
        try:
            from pivy import coin
            if Gui.getSoDBVersion() != coin.SoDB.getVersion():
                raise AssertionError("FreeCAD and Pivy use different versions "
                                     "of Coin. "
                                     "This will lead to unexpected behavior.")
        except AssertionError:
            App.Console.PrintWarning("Error: FreeCAD and Pivy "
                                         "use different versions of Coin. "
                                         "This will lead to unexpected "
                                         "behavior.\n")
        except ImportError:
            App.Console.PrintWarning("Error: Pivy not found, "
                                         "Draft Workbench will be disabled.\n")
        except Exception:
            App.Console.PrintWarning("Error: Unknown error "
                                         "while trying to load Pivy.\n")
        else:
            dependencies_OK = True

        if not dependencies_OK:
            return
        # END DRAFT
        # ADD Gear
        # END Gear
        """	 Doesn't work .. I Don't konw why.2020-02-06	
		#PART 
		import PartGui

		try:
			import BasicShapes.CommandShapes
		except ImportError as err:
			App.Console.PrintError("'BasicShapes' package cannot be loaded. "
								   "{err}\n".format(err=str(err)))

		try:
			import CompoundTools._CommandCompoundFilter
			import CompoundTools._CommandExplodeCompound
		except ImportError as err:
			App.Console.PrintError("'CompoundTools' package cannot be loaded. "
								   "{err}\n".format(err=str(err)))

		try:
			bop = __import__("BOPTools")
			bop.importAll()
			bop.addCommands()
			PartGui.BOPTools = bop
		except Exception as err:
			App.Console.PrintError("'BOPTools' package cannot be loaded. "
								   "{err}\n".format(err=str(err)))
		#END PART
		"""
        # Import Draft tools, icons
        try:
            import Draft_rc
            import DraftTools
            import DraftGui
            import DraftFillet
            Gui.addLanguagePath(":/translations")
            Gui.addIconPath(":/icons")
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Initializing one or more "
                                       "of the Draft modules failed, "
                                       "Draft will not work as expected.\n")
        try:
            # Set up command lists
            import draftutils.init_tools as it
            self.drawing_commands = it.get_draft_drawing_commands()
            self.annotation_commands = it.get_draft_annotation_commands()
            self.modification_commands = it.get_draft_modification_commands()
            self.context_commands = it.get_draft_context_commands()
            self.line_commands = it.get_draft_line_commands()
            self.utility_commands = it.get_draft_utility_commands()
            self.utility_small = it.get_draft_small_commands()

        # Set up toolbars
            self.appendToolbar(QT_TRANSLATE_NOOP(
                "Draft", "Draft creation tools"), self.drawing_commands)
            self.appendToolbar(QT_TRANSLATE_NOOP(
                "Draft", "Draft annotation tools"), self.annotation_commands)
            self.appendToolbar(QT_TRANSLATE_NOOP(
                "Draft", "Draft modification tools"), self.modification_commands)
            self.appendToolbar(QT_TRANSLATE_NOOP(
                "Draft", "Draft utility tools"), self.utility_small)

            # Set up menus
            self.appendMenu(QT_TRANSLATE_NOOP(
                "Draft", "&Drafting"), self.drawing_commands)
            self.appendMenu(QT_TRANSLATE_NOOP(
                "Draft", "&Annotation"), self.annotation_commands)
            self.appendMenu(QT_TRANSLATE_NOOP(
                "Draft", "&Modification"), self.modification_commands)
            self.appendMenu(QT_TRANSLATE_NOOP("Draft", "&Utilities"),
                            self.utility_commands + self.context_commands)

            # Set up preferences pages
            if hasattr(FreeCADGui, "draftToolBar"):
                if not hasattr(Gui.draftToolBar, "loadedPreferences"):
                    Gui.addPreferencePage(
                        ":/ui/preferences-draft.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                    Gui.addPreferencePage(
                        ":/ui/preferences-draftinterface.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                    Gui.addPreferencePage(
                        ":/ui/preferences-draftsnap.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                    Gui.addPreferencePage(
                        ":/ui/preferences-draftvisual.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                    Gui.addPreferencePage(
                        ":/ui/preferences-drafttexts.ui", QT_TRANSLATE_NOOP("Draft", "Draft"))
                    Gui.draftToolBar.loadedPreferences = True
                # END DRAFT
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Initializing one or more "
                                       "of the Draft modules failed, "
                                       "Draft will not work as expected.\n")

    def Activated(self):
        try:
            import WorkingPlane
            if not(App.ActiveDocument):
                App.newDocument()

            # FROM DRAFT
            if hasattr(FreeCADGui, "draftToolBar"):
                Gui.draftToolBar.Activated()
            if hasattr(FreeCADGui, "Snapper"):
                Gui.Snapper.show()
                import draftutils.init_draft_statusbar as dsb
                dsb.show_draft_statusbar()
            # Fix the view of the grid make it as 123D Design
            App.DraftWorkingPlane.alignToPointAndAxis(
                App.Vector(0.0, 0.0, 0.0), App.Vector(0, 0, 1), 0.0)
            Gui.Snapper.setGrid()
            Gui.activeDocument().activeView().viewTop()
            Gui.activeDocument().activeView().viewIsometric()
            for x in range(1, 12):
                Gui.ActiveDocument.ActiveView.zoomOut()

            App.Console.PrintLog(
                "Draft workbench activated Inside Design456.\n")
            App.Console.PrintMessage('Design456 workbench loaded\n')
            return
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Draft activation "
                                       "failed, "
                                       "Draft will not work as expected.\n")

    def Deactivated(self):
        try:
            "workbench deactivated"
            if hasattr(FreeCADGui, "draftToolBar"):
                Gui.draftToolBar.Deactivated()
            if hasattr(FreeCADGui, "Snapper"):
                Gui.Snapper.hide()
                import draftutils.init_draft_statusbar as dsb
                dsb.hide_draft_statusbar()
            App.Console.PrintLog(
                "Design456/Draft workbench deactivated.\n")
            return
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Draft deactivation failed\n")

    def ContextMenu(self, recipient):
        "right-clicks on screen"
        try:
            import Design456_Part as designPart
            import Design456_Tweak as twk
            self.appendContextMenu("Design456", self.list)
            # from DRAFT
            """Define an optional custom context menu."""
            # from Design456_PART
            self.appendContextMenu(
                "Design456_Part", designPart.Design456_Part_ToolBar.list)
            from DraftGui import translate
            if recipient == "View":
                if App.activeDraftCommand is None:
                    if Gui.Selection.getSelection():
                        self.appendContextMenu(
                            "Draft", self.drawing_commands + self.modification_commands)
                        self.appendContextMenu(
                            "Utilities", self.context_commands)
                    else:
                        self.appendContextMenu("Draft", self.drawing_commands)
                else:
                    if App.activeDraftCommand.featureName in (translate("draft", "Line"),
                                                                  translate(
                                                                      "draft", "Wire"),
                                                                  translate(
                                                                      "draft", "Polyline"),
                                                                  translate(
                                                                      "draft", "BSpline"),
                                                                  translate(
                                                                      "draft", "BezCurve"),
                                                                  translate("draft", "CubicBezCurve")):
                        self.appendContextMenu("", self.line_commands)
            else:
                if Gui.Selection.getSelection():
                    self.appendContextMenu("Utilities", self.context_commands)
            # END DRAFT
        except Exception as exc:
            App.Console.PrintError(exc)
            App.Console.PrintError("Error: Draft ContexMenu "
                                       "failed, "
                                       "Draft will not work as expected.\n")

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(Design456_Workbench())
# FROM DRAFT
# Preference pages for importing and exporting various file formats
# are independent of the loading of the workbench and can be loaded at startup
Gui.addPreferencePage(
    ":/ui/preferences-dxf.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))
Gui.addPreferencePage(
    ":/ui/preferences-dwg.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))
Gui.addPreferencePage(
    ":/ui/preferences-svg.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))
Gui.addPreferencePage(
    ":/ui/preferences-oca.ui", QT_TRANSLATE_NOOP("Draft", "Import-Export"))

App.__unit_test__ += ["TestDraftGui"]
