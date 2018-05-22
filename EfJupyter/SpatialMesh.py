class SpatialMesh:

    def __init__( self,
                  grid_x_size = 10, grid_x_step = 1,
                  grid_y_size = 10, grid_y_step = 1,
                  grid_z_size = 10, grid_z_step = 1 ):
        self.grid_x_size = grid_x_size
        self.grid_x_step = grid_x_step        
        self.grid_y_size = grid_y_size
        self.grid_y_step = grid_y_step
        self.grid_z_size = grid_z_size
        self.grid_z_step = grid_z_step


    def visualize( self, ax ):
        self.draw_cube( ax )


    def draw_cube( self, ax ):
        vertices = []
        vertices.append( [0, 0, 0] )
        vertices.append( [self.grid_x_size, 0, 0] )
        vertices.append( [self.grid_x_size, self.grid_y_size, 0] )
        vertices.append( [0, self.grid_y_size, 0] )
        vertices.append( [0, 0, 0] )
        vertices.append( [0, 0, self.grid_z_size] )
        vertices.append( [self.grid_x_size, 0, self.grid_z_size] )
        vertices.append( [self.grid_x_size, 0, 0] )
        vertices.append( [self.grid_x_size, 0, self.grid_z_size] )
        vertices.append( [self.grid_x_size, self.grid_y_size, self.grid_z_size] )
        vertices.append( [self.grid_x_size, self.grid_y_size, 0] )
        vertices.append( [self.grid_x_size, self.grid_y_size, self.grid_z_size] )
        vertices.append( [0, self.grid_y_size, self.grid_z_size] )
        vertices.append( [0, self.grid_y_size, 0] )
        vertices.append( [0, self.grid_y_size, self.grid_z_size] )
        vertices.append( [0, 0, self.grid_z_size] )
        x = [ v[0] for v in vertices ]
        y = [ v[1] for v in vertices ]
        z = [ v[2] for v in vertices ]
        ax.plot( x, y, z, label='volume' )


    def export( self ):
        as_dict = {}
        as_dict["Spatial mesh"] = {}
        as_dict["Spatial mesh"]["grid_x_size"] = self.grid_x_size
        as_dict["Spatial mesh"]["grid_x_step"] = self.grid_x_step
        as_dict["Spatial mesh"]["grid_y_size"] = self.grid_y_size
        as_dict["Spatial mesh"]["grid_y_step"] = self.grid_y_step
        as_dict["Spatial mesh"]["grid_z_size"] = self.grid_z_size
        as_dict["Spatial mesh"]["grid_z_step"] = self.grid_z_step
        return as_dict        
