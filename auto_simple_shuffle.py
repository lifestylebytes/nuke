# 2023 Aug
# Gabrielle You

import nuke

def create_parallel_dots(num_dots, spacing, reference_node, starting_x_pos, starting_y_pos):
    # Create a list to store the Dot nodes
    dots = []

    # Loop to create and position the dots
    for i in range(num_dots):
        dot = nuke.createNode("Dot")
        dot.setXpos(starting_x_pos + i * spacing)
        dot.setYpos(starting_y_pos)
        dots.append(dot)

    # Connect the dots together
    for i in range(num_dots - 1):
        dots[i + 1].setInput(0, dots[i])

    return dots

def aov_layers(read_node):
    # Get a list of available layers from the Read node
    layers = nuke.layers(read_node)

    # Calculate the total number of layers (excluding 'rgb')
    num_layers = len([layer for layer in layers if layer.lower() != 'rgb'])

    # Calculate the starting x and y positions for the new nodes
    starting_x_pos = int(read_node['xpos'].value()) + 34
    starting_y_pos = int(read_node['ypos'].value()) + 150

    # Create a list to store all the Dot nodes
    dot_nodes = create_parallel_dots(num_layers, 200, read_node, starting_x_pos, starting_y_pos)

    # Create Shuffle2 nodes for each layer and set the layer name as 'postage' (excluding 'rgb')
    for layer in layers:
        if layer.lower() != 'rgb':  # Skip 'rgb' layer
            # Create a unique Shuffle node name
            shuffle_name = 'Shuffle_' + layer
            suffix = 1
            while nuke.exists(shuffle_name):
                shuffle_name = 'Shuffle_' + layer + str(suffix)
                suffix += 1

            # Create a Shuffle2 node
            if dot_nodes:
                shuffle_node = nuke.createNode('Shuffle2', 'in1 ' + layer)
                shuffle_node.setInput(0, dot_nodes.pop(0))  # Connect to the first Dot node in the list

                # Set the position of the Shuffle2 node
                shuffle_node['xpos'].setValue(int(shuffle_node['xpos'].value()))
                shuffle_node['ypos'].setValue(int(shuffle_node['ypos'].value() + 100))

                # Rename the Shuffle2 node with the unique name
                shuffle_node['name'].setValue(shuffle_name)

# Assuming you already have a Read node for your file
read_node = nuke.selectedNode()

# Call the function to create the auto-distributor and generate Shuffle2 nodes
aov_layers(read_node)