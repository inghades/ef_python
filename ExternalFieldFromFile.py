from Vec3d import Vec3d
import physical_constants
import h5py

class ElectricFieldFromFile:

    def __init__(self):
        pass

    @classmethod
    def init_from_config(cls, conf):
        new_obj = cls()
        new_obj.allocate_grid_values( conf )
        new_obj.calculate_cell_size()
        return new_obj

    @classmethod
    def init_from_h5(cls, h5_field_group):
        new_obj = cls()
        new_obj.filename = h5_field_group.attrs["filename"][0]
        h5group = h5_field_group.attrs["filename"][0]+"/ElectricFieldFromFile"
        new_obj.allocate_grid_valuesh5( )
        return new_obj

    def allocate_grid_values ( self, conf ):
        conf_part = conf["ElectricFieldFromFile"]
        self.filename = conf_part["filename"]
        self.node_coordinates_ffile =
        h5file = h5py.File(self.filename, 'r')
        tmp_x = h5file["./Spatial_mesh/node_coordinates_x"]
        tmp_y = h5file["./Spatial_mesh/node_coordinates_y"]
        tmp_z = h5file["./Spatial_mesh/node_coordinates_z"]
        for i, (vx, vy, vz) in enumerate( zip( tmp_x, tmp_y, tmp_z ) ):
            self.node_coordinates_ffile[i] = Vec3d( vx, vy, vz )
        #
        tmp_x = h5group["./electric_field_x"][:]
        tmp_y = h5group["./electric_field_y"][:]
        tmp_z = h5group["./electric_field_z"][:]
        for i, (vx, vy, vz) in enumerate( zip( tmp_x, tmp_y, tmp_y ) ):
            self.electric_field_ffile[i] = Vec3d( vx, vy, vz )

    def calculate_cell_size(self):
        self.x_cell_size = abs(self.node_coordinates_ffile[1].x - self.node_coordinates[0].x)
        self.y_cell_size = abs(self.node_coordinates_ffile[1].y - self.node_coordinates[0].y)
        self.z_cell_size = abs(self.node_coordinates_ffile[1].z - self.node_coordinates[0].z)

    def field_at_particle_position(self, p):
        total_field = Vec3d.zero()
        dx = self.x_cell_size
        dy = self.y_cell_size
        dz = self.z_cell_size
        # 'tlf' = 'top_left_far'
        tlf_i, tlf_x_weight = next_node_num_and_weight( p.position.x, dx )
        tlf_j, tlf_y_weight = next_node_num_and_weight( p.position.y, dy )
        tlf_k, tlf_z_weight = next_node_num_and_weight( p.position.z, dz )
        # tlf
        total_field = Vec3d.zero()
        field_from_node = spat_mesh.electric_field[tlf_i][tlf_j][tlf_k].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # trf
        field_from_node = spat_mesh.electric_field[tlf_i-1][tlf_j][tlf_k].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # blf
        field_from_node = spat_mesh.electric_field[tlf_i][tlf_j - 1][tlf_k].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # brf
        field_from_node = spat_mesh.electric_field[tlf_i-1][tlf_j-1][tlf_k].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # tln
        field_from_node = spat_mesh.electric_field[tlf_i][tlf_j][tlf_k-1].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # trn
        field_from_node = spat_mesh.electric_field[tlf_i-1][tlf_j][tlf_k-1].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # bln
        field_from_node = spat_mesh.electric_field[tlf_i][tlf_j - 1][tlf_k-1].times_scalar(
            tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )
        # brn
        field_from_node = spat_mesh.electric_field[tlf_i-1][tlf_j-1][tlf_k-1].times_scalar(
            1.0 - tlf_x_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_y_weight )
        field_from_node = field_from_node.times_scalar( 1.0 - tlf_z_weight )
        total_field = total_field.add( field_from_node )

        return total_field

    def next_node_num_and_weight(x, grid_step):
        x_in_grid_units = x / grid_step
        next_node = ceil(x_in_grid_units)
        weight = 1.0 - (next_node - x_in_grid_units)
        return (next_node, weight)

    def write_to_file( self, h5file ):
        groupname = "/ElectricFieldFromFile"
        h5group = h5file.create_group( groupname )
        h5group.attrs["filename"] = self.filename
