"""

Disclaimer:
    I created this tool as a thank-you gift for my mentor and friend, Emerson Bonadias.

"""

__author__ = 'Luciano Cequinel'
__contact__ = 'lucianocequinel@gmail.com'
__version__ = '2.3.1'
__release_date__ = 'July, 02 2024'
__license__ = 'MIT'


import nuke


def create_curve_tool(sel_node, frame_range):
    """ 
        Creates a Curve Tool node and executes the AutoCrop function.

        :param sel_node: The selected node to which the Curve Tool will be connected.
        :param frame_range: The frame range over which the AutoCrop operation will be executed.
        :return: The created Curve Tool node.
    """

    new_curvetool = nuke.nodes.CurveTool()

    new_curvetool['operation'].setValue('Auto Crop')
    new_curvetool['channels'].setValue('alpha')
    new_curvetool['resetROI'].setValue('True')
    new_curvetool.knob("ROI").setValue([0, 0, sel_node.width(), sel_node.height()])
    new_curvetool.setInput(0, sel_node)

    # Execute CurveTool
    print(' >>> executing AutoCrop...')
    nuke.execute(new_curvetool, frame_range.first(), frame_range.last())

    return new_curvetool


def create_group_node(sel_node, curve_tool, frame_range):
    """ 
        Creates a Group node containing an Input node, an animated Crop node, and an Output node.

        :param sel_node: The selected node to which the Group node will be connected.
        :param curve_tool: The Curve Tool node containing the AutoCrop data.
        :param frame_range: The frame range over which the Crop node will be animated.
        :return: A tuple containing the created Group node and the animated Crop node.
    """

    autocrop_group = nuke.createNode('Group')

    autocrop_group.setName('superAutoCrop', uncollide=True)
    autocrop_group['label'].setValue('from {}\nRange {}\n'
                                     'size [value proportional_size]'.format(sel_node.name(), frame_range))
    autocrop_group.knob('tile_color').setValue(31552)
    autocrop_group.knob('note_font').setValue('Verdana bold')

    # open group to insert nodes inside
    autocrop_group.begin()

    # create an Input node
    input_node_group = nuke.createNode('Input')

    # create New Crop and copy the animation from CurveTool
    crop_node = nuke.createNode('Crop')
    crop_node['box'].setAnimated()
    crop_node.knob("box").copyAnimations(curve_tool.knob("autocropdata").animations())

    crop_node.setInput(0, input_node_group)

    crop_node.knob('tile_color').setValue(31552)  # 01050
    crop_node.knob('note_font').setValue('Verdana bold')

    nuke.autoplace(crop_node)

    # create an Output node
    output_node_group = nuke.createNode('Output')
    output_node_group.setInput(0, crop_node)

    output_node_group.hideControlPanel()

    nuke.autoplace(output_node_group)

    autocrop_group.end()

    autocrop_group.setInput(0, sel_node)

    nuke.autoplace(autocrop_group)

    return autocrop_group, crop_node


def create_group_knobs(autocrop_group):
    """
        Creates custom knobs to control the crop size within the Group node.

        :param autocrop_group: The Group node to which the knobs will be added.
        :return: None
    """

    tab = nuke.Tab_Knob('Size Control')
    autocrop_group.addKnob(tab)

    size_knob = nuke.Double_Knob('proportional_size', "Proportional Size")
    size_knob.setRange(0, 300)
    autocrop_group.addKnob(size_knob)
    autocrop_group['proportional_size'].setValue(50)

    softness_knob = nuke.Double_Knob('softness', "Softness")
    softness_knob.setRange(0, 100)
    autocrop_group.addKnob(softness_knob)

    div = nuke.Text_Knob("divider", "")
    autocrop_group.addKnob(div)

    # each side controls
    left_size_knob = nuke.Double_Knob('left_size', "Left")
    left_size_knob.setRange(-50, 50)
    autocrop_group.addKnob(left_size_knob)

    right_size_knob = nuke.Double_Knob('right_size', "Right")
    right_size_knob.setRange(-50, 50)
    autocrop_group.addKnob(right_size_knob)

    top_knob = nuke.Double_Knob('top_size', "Top")
    top_knob.setRange(-50, 50)
    autocrop_group.addKnob(top_knob)

    bottom_knob = nuke.Double_Knob('bottom_size', "Bottom")
    bottom_knob.setRange(-50, 50)
    autocrop_group.addKnob(bottom_knob)

    # credits knobs
    credits_knobs_a = nuke.Text_Knob('credit_a', '')
    autocrop_group.addKnob(credits_knobs_a)

    credits_knobs_b = nuke.Text_Knob('credit_c', '', '<font color = "#EF4E3D">Created by {}'.format(__author__))
    autocrop_group.addKnob(credits_knobs_b)

    credits_knobs_c = nuke.Text_Knob('credit_b', '', '<font color = "#EF4E3D">Version {} - {}'
                                     .format(__version__, __release_date__))
    autocrop_group.addKnob(credits_knobs_c)

    credit_link = ('<font color = "#EF4E3D">Check for updates '
                   '<a href=\"https://www.cequinavfx.com">'
                   '<font color=#EF4E3D><b>here</a>')

    credits_knobs_d = nuke.Text_Knob('credit_d', '', credit_link)
    autocrop_group.addKnob(credits_knobs_d)


def super_auto_crop():
    """
        Main function to create a Group node with custom knobs to control the bounding box.
        Requires an alpha channel and a frame range.
    """

    print()
    print(' {}'.format('_' * 29))
    print('\n Starting AutoCrop function...')

    sel_node = get_selection()

    if sel_node:
        
        print(' > selected node: {}'.format(sel_node.name()))

        frame_range = get_frame_range()

        if not frame_range:
            return  # breaks function if None is returned from get_frame_range()

        node_after = nuke.dependentNodes(nuke.INPUTS, sel_node)

        # create a CurveTool
        print(' > frame-range: {}'.format(frame_range))
        print(' >> creating CurveTool node')

        curve_tool = create_curve_tool(sel_node, frame_range)

        # create a Group
        print(' >> creating Group Node...')

        autocrop_group, crop_node = create_group_node(sel_node, curve_tool, frame_range)

        # create knobs to control the bounding box
        print(' >> adding custom knobs')
        create_group_knobs(autocrop_group)

        group_name = autocrop_group.name()

        # set softness knob expression
        crop_node.knob('softness').setExpression('(%s.knob.softness)'
                                                 % group_name)

        # set box knob expressions
        crop_node.knob('box').setExpression('(curve) + ((%s.knob.left_size) + (%s.knob.proportional_size) *-1)'
                                            % (group_name, group_name), 0)

        crop_node.knob('box').setExpression('(curve) + ((%s.knob.bottom_size) + (%s.knob.proportional_size) *-1)'
                                            % (group_name, group_name), 1)

        crop_node.knob('box').setExpression('(curve) + (%s.knob.right_size) + (%s.knob.proportional_size)'
                                            % (group_name, group_name), 2)

        crop_node.knob('box').setExpression('(curve) + (%s.knob.top_size) + (%s.knob.proportional_size)'
                                            % (group_name, group_name), 3)

        # Delete CurveTool
        _del = nuke.delete(curve_tool)

        if len(node_after) > 0:
            node_after = nuke.toNode(node_after[0].name())
            node_after.setInput(0, autocrop_group)

        print('')
        print(' AutoCrop successfully created')
        print(' {}'.format('_'*29))

        return


def get_frame_range():
    """ 
        Prompts the user to input a frame range and returns it.

        :return: The frame range entered by the user, or None if the input is invalid.
    """

    _range = '%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame())

    get_range = nuke.getInput('Inform the Frame Range to bake.\nUse 1-100 or 1,100', _range)

    try:
        frame_range = nuke.FrameRange(get_range)

    except Exception as err:
        print(err)
        return None

    else:
        return frame_range


def get_selection():
    """ 
        Retrieves and validates the selected node.

        :return: The selected node, or None if no valid node is selected.
    """

    sel_nodes = nuke.selectedNodes()

    if len(sel_nodes) == 1:

        sel_node = nuke.selectedNode()

        if not sel_node.Class() == 'Viewer':
            return sel_node

        else:
            nuke.message('Selection cannot be an Viewer')

    else:
        nuke.message("Select something!")
        return


if __name__ == '__main__':
    """
        Run the script without installation.
    """

    super_auto_crop()
