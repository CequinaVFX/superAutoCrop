# superAutoCrop
A tool that utilizes Nuke's original CurveTool to create an animated bounding box with controllers to adjust its size.

This tool was created as a thank-you gift for my mentor and friend, Emerson Bonadias.

## Installation
1. Rename the downloaded folder to **_superAutoCrop_** and place it inside your _.nuke_ folder.
2. Add the following line to your `init.py` file:
    ```python
    nuke.pluginAddPath('./superAutoCrop')
    ```
   For more information on locating the default .nuke directory, refer to [this guide](https://support.foundry.com/hc/en-us/articles/207271649-Q100048-Nuke-Directory-Locations).

## Usage
1. Select a node in Nuke.
2. Call the tool using the provided shortcut, or run it from the Toolbar.

### Shortcut
The default shortcut is `[` (open bracket). You can change this shortcut by editing line 6 of the `menu.py` file.

## Credits
Created by [Luciano Cequinel](https://www.cequinavfx.com).

To report bugs or make suggestions, please contact: lucianocequinel@gmail.com

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
