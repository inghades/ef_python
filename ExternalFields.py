from Vec3d import Vec3d
import physical_constants
import h5py
import numpy as np

class ExternalField:

    def __init__( self ):
        pass

    @classmethod
    def init_from_config( cls, field_conf, field_conf_name ):
        new_obj = cls()        
        new_obj.name = field_conf_name[ field_conf_name.rfind(".") + 1 : ]
        return new_obj

    @classmethod
    def init_from_h5( cls, h5group ):
        new_obj = cls() 
        new_obj.name = os.path.basename( h5group.name )
        return new_obj


    def write_to_file( self, h5_fields_group ):
        current_field_group = h5_fields_group.create_group( "./" + self.name )
        self.write_hdf5_field_parameters( current_field_group )

    

# Uniform magnetic

class ExternalFieldMagneticUniform( ExternalField ):

    def __init__( self ):
        super().__init__()

    @classmethod
    def init_from_config( cls, field_conf, field_conf_name ):
        new_obj = super().init_from_config( field_conf, field_conf_name )
        new_obj.field_type = "magnetic_uniform"
        new_obj.check_correctness_of_related_config_fields( field_conf )
        new_obj.get_values_from_config( field_conf )
        return new_obj


    def check_correctness_of_related_config_fields( self, field_conf ):
        pass
        # nothing to check here
        

    def get_values_from_config( self, field_conf ):
        self.magnetic_field = Vec3d( field_conf.getfloat("magnetic_field_x"),
                                     field_conf.getfloat("magnetic_field_y"),
                                     field_conf.getfloat("magnetic_field_z") )

    @classmethod 
    def init_from_h5( cls, h5_field_group ):
        new_obj = super().init_from_h5( h5_field_group )        
        new_obj.field_type = "magnetic_uniform"
        Hx = h5_field_group.attrs["magnetic_uniform_field_x"]
        Hy = h5_field_group.attrs["magnetic_uniform_field_y"]
        Hz = h5_field_group.attrs["magnetic_uniform_field_z"]        
        new_obj.magnetic_field = Vec3d( Hx, Hy, Hz )
        return new_obj


    def field_at_particle_position( self, particle, current_time ):
        return self.magnetic_field


    def write_hdf5_field_parameters( self, current_field_group_id ):
        current_field_group_id.attrs["field_type"] = self.field_type
        current_field_group_id.attrs.create( "magnetic_uniform_field_x",
                                             self.magnetic_field.x )
        current_field_group_id.attrs.create( "magnetic_uniform_field_y",
                                             self.magnetic_field.y )
        current_field_group_id.attrs.create( "magnetic_uniform_field_z",
                                             self.magnetic_field.z )
        current_field_group_id.attrs.create( "speed_of_light",
                                             physical_constants.speed_of_light )


    @classmethod
    def is_magnetic_uniform_config_part( cls, field_name ):
        return "ExternalFieldMagneticUniform" in field_name
        
# Uniform electric


class ExternalFieldElectricUniform( ExternalField ):

    def __init__( self ):
        pass

    @classmethod
    def init_from_config( cls, field_conf, field_conf_name ):
        new_obj = super().init_from_config( field_conf, field_conf_name )
        new_obj.field_type = "electric_uniform"
        new_obj.check_correctness_of_related_config_fields( field_conf )
        new_obj.get_values_from_config( field_conf )
        return new_obj


    def check_correctness_of_related_config_fields( self, field_conf ):
        pass
        # nothing to check here

    def get_values_from_config( self, field_conf ):
        self.electric_field = Vec3d( field_conf.getfloat("electric_field_x"),
                                     field_conf.getfloat("electric_field_y"),
                                     field_conf.getfloat("electric_field_z") )

    @classmethod 
    def init_from_h5( cls, h5_field_group ):
        new_obj = super().init_from_h5( h5_field_group )        
        new_obj.field_type = "electric_uniform"
        Ex = h5_field_group.attrs["electric_uniform_field_x"]
        Ey = h5_field_group.attrs["electric_uniform_field_y"]
        Ez = h5_field_group.attrs["electric_uniform_field_z"]        
        new_obj.electric_field = Vec3d( Ex, Ey, Ez )
        return new_obj
        

    def field_at_particle_position( self, particle, current_time ):
        return self.electric_field
    

    def write_hdf5_field_parameters( self, current_field_group_id ):
        current_field_group_id.attrs["field_type"] = self.field_type
        current_field_group_id.attrs.create( "electric_uniform_field_x",
                                             self.electric_field.x )
        current_field_group_id.attrs.create( "electric_uniform_field_y",
                                             self.electric_field.y )
        current_field_group_id.attrs.create( "electric_uniform_field_z",
                                             self.electric_field.z )


    @classmethod
    def is_electric_uniform_config_part( cls, field_name ):
        return "ExternalFieldElectricUniform" in field_name

# Eletric from file

class ExternalFieldElectricFile(ExternalField):

    def __init__(self):
        pass

    @classmethod
    def init_from_config(cls, field_conf, field_conf_name):
        new_obj = super().init_from_config(field_conf, field_conf_name)
        new_obj.field_type = "electric_file"
        new_obj.check_correctness_of_related_config_fields(field_conf)
        filename = field_conf["filename"]
        h5file = h5py.File(filename, 'r')
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
            new_obj.electric_field_file[i][j][k] = Vec3d( vx, vy, vz )

        return new_obj

    def check_correctness_of_related_config_fields(self, field_conf):
        pass
        # nothing to check here

    def allocate_ongrid_values( self ):
        nx = self.x_n_nodes
        ny = self.y_n_nodes
        nz = self.z_n_nodes
        self.electric_field_file = np.full( (nx,ny,nz) , Vec3d.zero(), dtype=object )


    @classmethod
    def init_from_h5(cls, h5_field_group):
        new_obj = super().init_from_h5(h5_field_group)
        new_obj.field_type = "electric_uniform"
        Ex = h5_field_group.attrs["electric_uniform_field_x"]
        Ey = h5_field_group.attrs["electric_uniform_field_y"]
        Ez = h5_field_group.attrs["electric_uniform_field_z"]
        new_obj.electric_field = Vec3d(Ex, Ey, Ez)
        return new_obj

    def field_at_particle_position(self, particle, current_time):
        return self.electric_field

    def write_hdf5_field_parameters(self, current_field_group_id):
        current_field_group_id.attrs["field_type"] = self.field_type
        current_field_group_id.attrs.create("electric_uniform_field_x",
                                            self.electric_field.x)
        current_field_group_id.attrs.create("electric_uniform_field_y",
                                            self.electric_field.y)
        current_field_group_id.attrs.create("electric_uniform_field_z",
                                            self.electric_field.z)

    @classmethod
    def is_electric_file_config_part(cls, field_name):
        return "ExternalFieldElectricFile" in field_name

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