import nuke
import superAutoCrop

SHORTCUT = '['

#Add a menu and assign a shortcut
toolbar = nuke.menu('Nodes')
cqnTools = toolbar.addMenu('CQNTools', icon='Modify.png')
cqnTools.addCommand('superAutoCrop', 'superAutoCrop.superAutoCrop()', SHORTCUT, icon='AutoCrop.png')