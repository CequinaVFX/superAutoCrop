import nuke
import superAutoCrop

# you can change shortcut here, use None if you do not want a shortcut
SHORTCUT = '['

#Add a menu and assign a shortcut
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', icon='Modify.png')
cqnTools.addCommand('superAutoCrop', 'superAutoCrop.superAutoCrop()', SHORTCUT, icon='AutoCrop.png')