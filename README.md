# Design456 FreeCAD Workbench 

[![](http://img.youtube.com/vi/upgNYkZRY7I/0.jpg)](http://www.youtube.com/watch?v=upgNYkZRY7I "Design456 Workbench")

**Important Note:** **WIP!!!** Please feel free to suggest, contribute, join, help, debug etc... I am new to both Python and FreeCAD Python. My background is in other languages. I hope you find this workbench useful. 

### Aim 
FreeCAD primarily utilizes a parametric modeling paradigm. This workbench will work to develop a 'direct modeling' approach. This approach is more common in popular CAD solutions. For example, clicking on a face and being able to extrude by moving the mouse, instead of specifying a the distance by entering a number in to a text field.  

### Install 

1. `cd  ~/.FreeCAD/Mod`
2. `git clone --recurse-submodules -j8 https://github.com/MariwanJ/Design456`
3. Restart FreeCAD

Result: The Design456 workbench should no be available in the workbench drop-down menu

**Note:** Please keep this workbench up-to-date by pulling changes from this repository via `git`. This can be done before each time Design456 will be used.  

1. `cd  ~/.FreeCAD/Mod/Design456`
2. `git pull`
3. Restart FreeCAD

### Usage

### Inspiration

Initial inspiration came from exploring the a template workbench named D3D-Printer-Workbench. Thanks to the author. Other workbenches will be inspected to see what other code can be re-used. 

### Notes

- Use Face to extract a face from a side.  
- You cannot use `Extrude` to Extrude a side. Instead use the other function `Copy-Face-Extrude`  
- Tutorials and guides will be written /made later 

### Feedback

Please leave comments, bugs, fixes in the issue queue of this repository.

### Relevant Links

* FreeCAD forum thread [announcing Design456 workbench](https://forum.freecadweb.org/viewtopic.php?f=8&t=54893)  

### Developer

Mariwan Jalal 2021-01-29
