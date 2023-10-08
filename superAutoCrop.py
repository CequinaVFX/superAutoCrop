#******************************************************
# I created this tool as a thankful gift to my mentor and friend Emerson Bonadias.
#
# version: 2.1.3
# date: October 09 2023
#
# license: MIT
# author: Luciano Cequinel [lucianocequinel@gmail.com]
#******************************************************

import nuke

def input_AutoCrop(selNode):

    z = nuke.Panel('superAutoCrop')

    frame_range = nuke.FrameRange('%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()))

    z.addSingleLineInput('frame range', frame_range)

    z.setWidth(300)
    result = z.show()

    if result:
        fr = z.value('frame range')
        run_AutoCrop(selNode, fr)
    else:
        print('superAutoCrop aborted!')
        return

def run_AutoCrop(selNode, fr):

        print()
        try:
            a, b = fr.split('-')
        except:
            print('Error: ', fr)
            message = nuke.ask('You should use - (hyphen) to separate IN and OUT. Ex.: 10-60\nTry again?')

            if message == True:
                input_AutoCrop(selNode)
            else:
                return

        try:
            a, b = fr.split('-')
            frame_range = nuke.FrameRange('%s-%s' % (a, b))
        except:
            print('Error: ', fr)
            message = nuke.ask('Something wrong on frame range typing.\nTry again?')

            if message == True:
                input_AutoCrop(selNode)
            else:
                return

        selNode = nuke.selectedNode()
        nkRoot = nuke.root()

        # get output from selected node
        output = nuke.dependentNodes(nuke.INPUTS, selNode)

        # Get Width & Height
        wNode = selNode.width()
        hNode = selNode.height()

        # Create a CurveTool

        print('creating CurveTool...')

        cTool = nuke.nodes.CurveTool()
        cTool.setInput(0, selNode)
        cTool['operation'].setValue('Auto Crop')
        cTool['channels'].setValue('alpha')
        print('...using alpha only...')
        
        cTool['resetROI'].setValue('True')
        cTool.knob("ROI").setValue( [ 0, 0 , selNode.width() , selNode.height() ] )
        cTool.setInput(0, selNode)

        #Execute CurveTool
        print('executing AutoCrop...')
        nuke.execute(cTool, frame_range.first(), frame_range.last())

        # create a group

        print('creating Nodes...')

        grAutoCrop = nuke.createNode('Group')

        grAutoCrop.setName('superAutoCrop_%s_' % (selNode.name()), uncollide=True)
        grAutoCrop.knob('tile_color').setValue(31552)
        grAutoCrop.knob('note_font').setValue('Verdana bold')

        grAutoCrop.begin()

        # create an Input node
        grInput = nuke.createNode('Input')

        # Create New Crop with data from CurveTool
        nCrop = nuke.createNode('Crop')
        nCrop.knob("box").copyAnimations(cTool.knob("autocropdata").animations())

        nCrop.setInput(0, grInput)

        nCrop.knob('tile_color').setValue(31552) #01050
        nCrop.knob('note_font').setValue('Verdana bold')

        nuke.autoplace(nCrop)

        # create an Output node
        grOutput = nuke.createNode('Output')
        grOutput.setInput(0, nCrop)

        grOutput.hideControlPanel()

        nuke.autoplace(grOutput)

        grAutoCrop.end()

        grAutoCrop.setInput(0, selNode)

        output = nuke.toNode(output[0].name())
        output.setInput(0, grAutoCrop)

        nuke.autoplace(grAutoCrop)

        # Create knobs to control the bounding box
        tab = nuke.Tab_Knob('Size Control')
        grAutoCrop.addKnob(tab)
        
        gS = nuke.Double_Knob('genSize',"Proportional Size")
        gS.setRange(0,300)
        grAutoCrop.addKnob(gS)

        gSoft = nuke.Double_Knob('genSoftness',"Softness")
        gSoft.setRange(0,100)
        grAutoCrop.addKnob(gSoft)

        div = nuke.Text_Knob("divider","")
        grAutoCrop.addKnob(div)

        lS = nuke.Double_Knob('lSize',"Left")
        lS.setRange(-50,50)
        grAutoCrop.addKnob(lS)

        rS = nuke.Double_Knob('rSize',"Right")
        rS.setRange(-50,50)
        grAutoCrop.addKnob(rS)

        tS = nuke.Double_Knob('tSize',"Top")
        tS.setRange(-50,50)
        grAutoCrop.addKnob(tS)
        
        bS = nuke.Double_Knob('bSize',"Bottom")
        bS.setRange(-50,50)
        grAutoCrop.addKnob(bS)

        c = nuke.Text_Knob('c0', '')
        grAutoCrop.addKnob(c)

        c = nuke.Text_Knob('c1', '', '<font color = "#EF4E3D">Version 2.1.0 - August/2023')
        grAutoCrop.addKnob(c)

        c = nuke.Text_Knob('c2', '', '<font color = "#EF4E3D">Created by Luciano Cequinel')
        grAutoCrop.addKnob(c)

        c = nuke.Text_Knob('c3', '', '<font color = "#EF4E3D">Check for updates <a href=\"https://www.cequinavfx.com"><font color=#EF4E3D><b>here</a>')
        grAutoCrop.addKnob(c)

        # Set expressions to knobs
        grAutoCrop['genSize'].setValue(50)

        grName = grAutoCrop.name()

        nCrop.knob('box').setExpression('(curve) + ((%s.knob.lSize) + (%s.knob.genSize) *-1)' %(grName, grName), 0 )
        nCrop.knob('box').setExpression('(curve) + ((%s.knob.bSize) + (%s.knob.genSize) *-1)' %(grName, grName), 1)
        nCrop.knob('box').setExpression('(curve) + (%s.knob.rSize) + (%s.knob.genSize)' %(grName, grName), 2)
        nCrop.knob('box').setExpression('(curve) + (%s.knob.tSize) + (%s.knob.genSize)' %(grName, grName), 3)

        nCrop.knob('softness').setExpression('(%s.knob.genSoftness)' %(grName))

        # Delete CurveTool
        nuke.delete(cTool)

        print('AutoCrop successfully created')


def superAutoCrop():

    # get the selected node
    selNode = nuke.selectedNodes()

    if len(selNode) < 1:
        nuke.message('Select any node!')
        return

    elif len(selNode) > 1:
       nuke.message('Select just one node!')
       return

    elif len(selNode) == 0:
        nuke.message('Select any node!')
        return

    else:
        selNode = nuke.selectedNode()

        if selNode.Class() == 'Viewer':
            nuke.message("Select node can't be a Viewer")
            return
        else:
            run = input_AutoCrop(selNode)
            return


if __name__ == '__main__':
    run = superAutoCrop()
