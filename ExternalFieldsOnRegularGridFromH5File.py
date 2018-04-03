import h5py
import numpy as np
from math import ceil

from ExternalField import ExternalField
from Vec3d import Vec3d
import physical_constants


# Electric on regular grid from h5 file

class ExternalFieldElectricOnRegularGridFromH5File( ExternalField ):

    def __init__(self):
        pass

    @classmethod
    def init_from_config( cls, field_conf, field_conf_name ):
        new_obj = super().init_from_config( field_conf, field_conf_name )
        new_obj.field_type = "electric_on_regular_grid_from_h5file"
        new_obj.check_correctness_of_related_config_fields( field_conf )
        new_obj.h5filename = field_conf["filename"]
        h5file = h5py.File( new_obj.h5filename, 'r' )
        new_obj.x_volume_size = h5file["./Spatial_mesh"].attrs["x_volume_size"]
        new_obj.y_volume_size = h5file["./Spatial_mesh"].attrs["y_volume_size"]
        new_obj.z_volume_size = h5file["./Spatial_mesh"].attrs["z_volume_size"]
        new_obj.x_cell_size = h5file["./Spatial_mesh"].attrs["x_cell_size"]
        new_obj.y_cell_size = h5file["./Spatial_mesh"].attrs["y_cell_size"]
        new_obj.z_cell_size = h5file["./Spatial_mesh"].attrs["z_cell_size"]
        new_obj.x_n_nodes = h5file["./Spatial_mesh"].attrs["x_n_nodes"]
        new_obj.y_n_nodes = h5file["./Spatial_mesh"].attrs["y_n_nodes"]
        new_obj.z_n_nodes = h5file["./Spatial_mesh"].attrs["z_n_nodes"]
        new_obj.allocate_ongrid_values()
        tmp_x = h5file["./Spatial_mesh/electric_field_x"]
        tmp_y = h5file["./Spatial_mesh/electric_field_y"]
        tmp_z = h5file["./Spatial_mesh/electric_field_z"]
        for global_idx, (vx, vy, vz) in enumerate( zip( tmp_x, tmp_y, tmp_z ) ):
            i, j, k = new_obj.global_idx_to_node_ijk( global_idx )
            new_obj.electric_field[i][j][k] = Vec3d( vx, vy, vz )
        return new_obj

    def check_correctness_of_related_config_fields(self, field_conf):
        pass
        # nothing to check here

    def allocate_ongrid_values( self ):
        nx = self.x_n_nodes
        ny = self.y_n_nodes
        nz = self.z_n_nodes
        self.electric_field = np.full( (nx, ny, nz) , Vec3d.zero(), dtype=object )


    @classmethod
    def init_from_h5( cls, h5_field_group ):
        new_obj = super().init_from_h5( h5_field_group )
        new_obj.field_type = "electric_on_regular_grid_from_h5file"
        print( "ExternalFieldElectricOnRegularGridFromH5File: "
               "continue from h5 is not supported" )
        self.electric_field = None               
        # Ex = h5_field_group.attrs["electric_uniform_field_x"]
        # Ey = h5_field_group.attrs["electric_uniform_field_y"]
        # Ez = h5_field_group.attrs["electric_uniform_field_z"]
        # new_obj.electric_field = Vec3d(Ex, Ey, Ez)
        return new_obj

    
    def field_at_particle_position( self, particle, current_time ):
        # todo: this is copied from ParticleToMeshMap class.
        # Create RegularMesh class instead?
        dx = self.x_cell_size
        dy = self.y_cell_size
        dz = self.z_cell_size
        p = particle
        # 'tlf' = 'top_left_far'
        tlf_i, tlf_x_weight = next_node_num_and_weight( p.position.x, dx )
        tlf_j, tlf_y_weight = next_node_num_and_weight( p.position.y, dy )
        tlf_k, tlf_z_weight = next_node_num_and_weight( p.position.z, dz )
        # tlf
        total_field = Vec3d.zero()
        field_from_node = self.electric_field[tlf_i][tlf_j][tlf_k].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # trf
        field_from_node = self.electric_field[tlf_i-1][tlf_j][tlf_k].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # blf
        field_from_node = self.electric_field[tlf_i][tlf_j - 1][tlf_k].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # brf
        field_from_node = self.electric_field[tlf_i-1][tlf_j-1][tlf_k].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # tln
        field_from_node = self.electric_field[tlf_i][tlf_j][tlf_k-1].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # trn
        field_from_node = self.electric_field[tlf_i-1][tlf_j][tlf_k-1].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # bln
        field_from_node = self.electric_field[tlf_i][tlf_j - 1][tlf_k-1].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # brn
        field_from_node = self.electric_field[tlf_i-1][tlf_j-1][tlf_k-1].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        return total_field

    
    def write_hdf5_field_parameters(self, current_field_group_id):
        current_field_group_id.attrs["field_type"] = self.field_type
        current_field_group_id.attrs["filename"] = self.h5filename

        
    @classmethod
    def is_electric_on_regular_grid_from_h5file_config_part( cls, field_name ):
        return "ExternalFieldElectricOnRegularGridFromH5File" in field_name


    
    def global_idx_to_node_ijk( self, global_idx ):
        # In row-major order: (used to save on disk)
        # global_index = i * nz * ny +
        #                j * nz +
        #                k
        #
        nx = self.x_n_nodes
        ny = self.y_n_nodes
        nz = self.z_n_nodes
        i = global_idx // ( nz * ny )
        j_and_k_part = global_idx % ( nz * ny )
        j = j_and_k_part // nz
        k = j_and_k_part % nz
        return (i, j, k)


def next_node_num_and_weight( x, grid_step ):
    x_in_grid_units = x / grid_step
    next_node = ceil( x_in_grid_units )
    weight = 1.0 - ( next_node - x_in_grid_units )
    return ( next_node, weight )
