import nuke
import superAutoCrop

# you can change the shortcut here; use 'None' if you do not want a shortcut
SHORTCUT = '['

ICON = 'superAutoCrop.png'

# Add the command to Nuke's toolbar, assign a shortcut, and an icon
toolbar = nuke.menu('Nodes')
customToolbar = toolbar.addMenu('CQN Tools')
customToolbar.addCommand('superAutoCrop', 'superAutoCrop.super_auto_crop()', SHORTCUT, icon=ICON)
