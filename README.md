# tc_Popups

This is a set of plugins for Modo 901 which all feature a common mechanism: a pop-up search field. This emulates the behaviors found in many apps today (Nuke, Fusion, Softimage, Maya, Fabric Engine...)
The commands included here are:
* Get Item / Add To Schematic
* Get / Apply Material
* Select a Channel


### Get Item

![](http://www.timcrowson.com/wp-content/uploads/2015/05/popupgetItemSchematic.jpg)

**Global use:**
* Press **Alt+f1** to display a searchable pop-up list of all the item types available in Modo.
* Type to narrow the search results, or use the up/down arrow keys to make a selection.
* Press Return or click an item to create it in the scene.

**Schematic use:**
* *While hovering over a Schematic view*, press **Tab** to display the same searchable pop-up list.
* As above, make your selection either by typing or by navigating to it in the list.
* In addition to creating the item, it will also be added to the current workspace in the schematic.

**Command Information:**
* Adds a new command to Modo called *popup.getItem* which takes a single argument: *global|schematic*
* *popup.getItem global* is mapped to **Alt+f1**
* *popup.getItem schematic* is mapped to **Tab**, but only for Schematic views
* The list of items is derived procedurally at startup by parsing all the configs imported by Modo, looking for item type definitions. Certain arcane items will throw errors when created.



### Get Material

![](http://www.timcrowson.com/wp-content/uploads/2015/05/popup.getMaterial.jpg)

**Use:**
* Press **Alt+M** to display a searchable pop-up listing all the current material tags in the scene.
* Type to narrow the results, or make your selection via the up-down arrow keys or the left mouse button.
* Pressing Return or clicking on a material in the list will apply that material to the selected item or faces.
* If the list is empty (i.e. the search result came up blank),  a new material will be created and assigned.

**Command Information:** Adds a command called *popup.getMaterial* which is mapped to **Alt+M**


### Select Channel

![](http://www.timcrowson.com/wp-content/uploads/2015/05/popup.selectChannel.jpg)

**Use:**
* Press **Alt+I** to display a searchable pop-up listing all the channels of the currently selected item.
* Make your selection.
* Press Return to select the target channel.

**Command Information:** Adds a command called *popup.selectChannel* mapped to **Alt+I**
