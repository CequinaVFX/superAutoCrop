import nuke
import superAutoCrop

# you can change the shortcut here; use 'None' if you do not want a shortcut
SHORTCUT = '['
# Set an icon; use 'None' if you do not want a one
ICON = 'AutoCrop.png'

# Add the command to Nuke's toolbar, assign a shortcut, and an icon
toolbar = nuke.menu('Nodes')
customToolbar = toolbar.addMenu('Custom Tools', icon='Modify.png')
customToolbar.addCommand('superAutoCrop', 'superAutoCrop.super_auto_crop()', SHORTCUT, icon=ICON)
