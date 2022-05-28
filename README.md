# Design456 FreeCAD Workbench 

Video Showcase:

[![](http://img.youtube.com/vi/pmGW4OxVbYw/0.jpg)](https://www.youtube.com/watch?v=pmGW4OxVbYw "Design456 Workbench")

**Important Note:** **WIP!!!** Please feel free to suggest, contribute, join, help, debug etc... I am new to both Python and FreeCAD Python. My background is in other languages. I hope you find this workbench useful.

### Aim 
FreeCAD primarily utilizes a parametric modeling paradigm. This workbench will work to develop 'direct modeling' approach. Currently, this approach will be accomplished interactively using the viewerport widgets.  For example, clicking on a face and being able to extrude or push/pull by moving the mouse, instead of specifying a the distance by entering a number in to a text field.

### Background
Direct modeling approach has lately become more common in popular CAD solutions. This involves directly modifying the geometry without relying on the parameter based feature tree. While not completely replacing the parametric based approach, this approach is good for interoperability, making complex designs with rapid iterations, and using with minimal prior training.

### Install 

1. `cd  ~/.FreeCAD/Mod`
2. `git clone https://github.com/MariwanJ/Design456`
3. Restart FreeCAD

Result: The Design456 workbench should now be available in the workbench drop-down menu

**Note:** Please keep this workbench up-to-date by pulling changes from this repository via `git`. This can be done before each time Design456 will be used.  

1. `cd  ~/.FreeCAD/Mod/Design456`
2. `git pull`
3. Restart FreeCAD

### Usage

### Inspiration

Initial inspiration came from exploring the a template workbench named D3D-Printer-Workbench. Thanks to the author. Other workbenches will be inspected to see what other code can be re-used. 

<style>{color:Blue;}
### FreeCAD is broken and unreliable
Many of my tools fails due to the internal failure of OCC or FreeCAD as a whole. I wounder if Direct modeling will be possible while the union, cut, ..etc basic operaions fails totally in some cases. 

[![](http://img.youtube.com/vi/GLnkoe0oK8U/0.jpg)](https://www.youtube.com/watch?v=GLnkoe0oK8U "How broken is FreeCAD?")
</style>

### Notes

- You need to use latest FreeCAD to not get problems with this WB. Update your local version of Design456 regularly by daily basis.
- Caution: It's recommended to work on a copy of your object even if Undo is functional now. If you find out it works on your test object, then apply it to your original object.  
- There might be other issues, as I am the sole developer on this project, it is difficult to do all the work quickly. I have in my plan to test all these functions in quite depth. But at the moment, I wish to implement them and learn how I can do them. I am still in the beginning of the learning process.  
- Tutorials and guides will be written /made later
- Check out my videos to know how to use the tools.   

### Feedback

Please leave comments, bugs, fixes in the issue queue of this repository.

### Relevant Links

* FreeCAD forum thread [announcing Design456 workbench](https://forum.freecadweb.org/viewtopic.php?f=8&t=54893)    (No more used 2022-01-20)
* FreeCAD forum thread [progress Design456 workbench](https://forum.freecadweb.org/viewtopic.php?f=10&t=55866&p=480589#p480589) (No more used 2022-01-20)
### Developer

Mariwan Jalal 2021-01-29
