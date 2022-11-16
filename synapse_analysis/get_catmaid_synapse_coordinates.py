import pymaid
import numpy as np
from FANC_auto_recon.transforms import realignment

def get_catmaid_synapse_coordinates(neuron, voxel_resolution=np.array([4.3, 4.3, 45]), transform=True):
    
    skeleton_id = neuron.skeleton_id
    connector_details = pymaid.get_connector_details(neuron)
    # connector_details.presynaptic_to_node: node presynaptic to connector
    # connector_details.postsynaptic_to_node: node(s) postsynaptic to connector
    # connector_details.presynaptic_to: skeleton ID associated with node presynaptic to connector
    # connector_details.postsynaptic_to: skeleton ID(s) associated with node(s) postsynaptic to connector
    
    # Output synapses (node presynaptic to connector belongs to neuron of interest)
    output_connectors = connector_details.loc[connector_details.presynaptic_to==int(skeleton_id), :] 
    if len(output_connectors) > 0:
        output_nodes = np.concatenate(output_connectors.postsynaptic_to_node.values)
        output_nodes = [i for i in output_nodes if i]
        output_coordinates = pymaid.get_node_location(output_nodes).loc[:, ['x', 'y', 'z']]

        if transform is False:
            output_coordinates = output_coordinates.values / voxel_resolution
        else:
            # Transform coordinates from CATMAID to Neuroglancer space
            output_coordinates = realignment.fanc3_to_4(output_coordinates.values / voxel_resolution)
    else:
        output_coordinates = None

    # Input synapses (node presynaptic to connector does not belong to neuron of interest)
    input_connectors = connector_details.loc[connector_details.presynaptic_to!=int(skeleton_id), :]
    if len(input_connectors) > 0:
        input_nodes = input_connectors.presynaptic_to_node.values
        input_nodes = [i for i in input_nodes if i!=None]
        input_coordinates = pymaid.get_node_location(input_nodes).loc[:, ['x', 'y', 'z']]

        if transform is False:
            input_coordinates = input_coordinates.values / voxel_resolution
        else:
            # Transform coordinates from CATMAID to Neuroglancer space
            input_coordinates = realignment.fanc3_to_4(input_coordinates.values / voxel_resolution)
    else:
        input_coordinates = None

    return input_coordinates, output_coordinates
