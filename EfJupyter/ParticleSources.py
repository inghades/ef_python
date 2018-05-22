class ParticleSourceBox():
    def __init__( self, name = 'box_source',
                  initial_number_of_particles = 500,
                  particles_to_generate_each_step = 500, 
                  box_x_left = 6, box_x_right = 5,
                  box_y_bottom = 2, box_y_top = 5,
                  box_z_near = 1, box_z_far = 3,
                  mean_momentum_x = 0,
                  mean_momentum_y = 0,
                  mean_momentum_z = 6.641e-15,
                  temperature = 0.0,
                  charge = -1.799e-6,
                  mass = 3.672e-24 ):
        self.name = name
        self.box_x_left = box_x_left
        self.box_x_right = box_x_right
        self.box_y_bottom = box_y_bottom
        self.box_y_top = box_y_top
        self.box_z_near = box_z_near
        self.box_z_far = box_z_far
        self.initial_number_of_particles = initial_number_of_particles
        self.particles_to_generate_each_step = particles_to_generate_each_step
        self.mean_momentum_x = mean_momentum_x
        self.mean_momentum_y = mean_momentum_y
        self.mean_momentum_z = mean_momentum_z
        self.temperature = temperature
        self.charge = charge
        self.mass = mass


    def visualize( self, ax ):
        self.draw_cube( ax )


    def draw_cube( self, ax ):
        vertices = []
        vertices.append( [self.box_x_left, self.box_y_bottom, self.box_z_near] )
        vertices.append( [self.box_x_right, self.box_y_bottom, self.box_z_near] )
        vertices.append( [self.box_x_right, self.box_y_top, self.box_z_near] )
        vertices.append( [self.box_x_left, self.box_y_top, self.box_z_near] )
        vertices.append( [self.box_x_left, self.box_y_bottom, self.box_z_near] )
        vertices.append( [self.box_x_left, self.box_y_bottom, self.box_z_far] )
        vertices.append( [self.box_x_left, self.box_y_top, self.box_z_far] )
        vertices.append( [self.box_x_left, self.box_y_top, self.box_z_near] )
        vertices.append( [self.box_x_left, self.box_y_top, self.box_z_far] )
        vertices.append( [self.box_x_right, self.box_y_top, self.box_z_far] )
        vertices.append( [self.box_x_right, self.box_y_top, self.box_z_near] )
        vertices.append( [self.box_x_right, self.box_y_top, self.box_z_far] )
        vertices.append( [self.box_x_right, self.box_y_bottom, self.box_z_far] )
        vertices.append( [self.box_x_right, self.box_y_bottom, self.box_z_near] )
        vertices.append( [self.box_x_right, self.box_y_bottom, self.box_z_far] )
        vertices.append( [self.box_x_left, self.box_y_bottom, self.box_z_far] )
        x = [ v[0] for v in vertices ]
        y = [ v[1] for v in vertices ]
        z = [ v[2] for v in vertices ]
        ax.plot( x, y, z, label=self.name )


    def export( self ):
        as_dict = {}
        sec_name = "Particle_source_box" + "." + self.name
        as_dict[sec_name] = {}
        as_dict[sec_name]["box_x_left"] = self.box_x_left
        as_dict[sec_name]["box_x_right"] = self.box_x_right
        as_dict[sec_name]["box_y_bottom"] = self.box_y_bottom
        as_dict[sec_name]["box_y_top"] = self.box_y_top
        as_dict[sec_name]["box_z_near"] = self.box_z_near
        as_dict[sec_name]["box_z_far"] = self.box_z_far
        as_dict[sec_name]["initial_number_of_particles"] = \
                                                self.initial_number_of_particles
        as_dict[sec_name]["particles_to_generate_each_step"] = \
                                                self.particles_to_generate_each_step
        as_dict[sec_name]["mean_momentum_x"] = self.mean_momentum_x
        as_dict[sec_name]["mean_momentum_y"] = self.mean_momentum_y
        as_dict[sec_name]["mean_momentum_z"] = self.mean_momentum_z
        as_dict[sec_name]["temperature"] = self.temperature
        as_dict[sec_name]["charge"] = self.charge
        as_dict[sec_name]["mass"] = self.mass
        return as_dict        





    
class ParticleSourceCylinder():
    def __init__( self, name = 'cyl_source',
                  initial_number_of_particles = 500,
                  particles_to_generate_each_step = 500,
                  cylinder_axis_start_x = 2.5, cylinder_axis_start_y = 2.5,
                  cylinder_axis_start_z = 4, cylinder_axis_end_x = 2.5,
                  cylinder_axis_end_y = 2.5, cylinder_axis_end_z = 7,
                  cylinder_radius = 1,
                  mean_momentum_x = 0,
                  mean_momentum_y = 0,
                  mean_momentum_z = 6.641e-15,
                  temperature = 0.0,
                  charge = -1.799e-6,
                  mass = 3.672e-24 ):
        self.name = name
        self.cylinder_axis_start_x = cylinder_axis_start_x
        self.cylinder_axis_start_y = cylinder_axis_start_y
        self.cylinder_axis_start_z = cylinder_axis_start_z
        self.cylinder_axis_end_x = cylinder_axis_end_x
        self.cylinder_axis_end_y = cylinder_axis_end_y
        self.cylinder_axis_end_z = cylinder_axis_end_z
        self.cylinder_radius = cylinder_radius
        self.initial_number_of_particles = initial_number_of_particles
        self.particles_to_generate_each_step = particles_to_generate_each_step
        self.mean_momentum_x = mean_momentum_x
        self.mean_momentum_y = mean_momentum_y
        self.mean_momentum_z = mean_momentum_z
        self.temperature = temperature
        self.charge = charge
        self.mass = mass


    def visualize( self, ax ):
        self.draw_cyl( ax )


    def draw_cyl( self, ax ):
        vertices = []
        shift_x = self.cylinder_axis_start_x
        shift_y = self.cylinder_axis_start_y
        arc_step = 5.0 / 180.0 * np.pi
        r = self.cylinder_radius
        z1 = self.cylinder_axis_start_z
        z2 = self.cylinder_axis_end_z
        vertices.append([shift_x + r, shift_y, z1])
        for phi in np.arange(0, 360, arc_step):
            vertices.append([shift_x + r * np.cos(phi), shift_y + r * np.sin(phi), z1])
        vertices.append([shift_x + r, shift_y, z1])
        vertices.append([shift_x + r, shift_y, z2])
        for phi in np.arange(0, 360, arc_step):
            vertices.append([shift_x + r * np.cos(phi), shift_y + r * np.sin(phi), z2])
        x = [ v[0] for v in vertices ]
        y = [ v[1] for v in vertices ]
        z = [ v[2] for v in vertices ]
        ax.plot( x, y, z, label=self.name )


    def export( self ):
        as_dict = {}
        sec_name = "Particle_source_cylinder" + "." + self.name
        as_dict[sec_name] = {}
        as_dict[sec_name]["cylinder_axis_start_x"] = self.cylinder_axis_start_x
        as_dict[sec_name]["cylinder_axis_start_y"] = self.cylinder_axis_start_y
        as_dict[sec_name]["cylinder_axis_start_z"] = self.cylinder_axis_start_z
        as_dict[sec_name]["cylinder_axis_end_x"] = self.cylinder_axis_end_x
        as_dict[sec_name]["cylinder_axis_end_y"] = self.cylinder_axis_end_y
        as_dict[sec_name]["cylinder_axis_end_z"] = self.cylinder_axis_end_z
        as_dict[sec_name]["cylinder_radius"] = self.cylinder_radius
        as_dict[sec_name]["initial_number_of_particles"] = \
                                                self.initial_number_of_particles
        as_dict[sec_name]["particles_to_generate_each_step"] = \
                                                self.particles_to_generate_each_step
        as_dict[sec_name]["mean_momentum_x"] = self.mean_momentum_x
        as_dict[sec_name]["mean_momentum_y"] = self.mean_momentum_y
        as_dict[sec_name]["mean_momentum_z"] = self.mean_momentum_z
        as_dict[sec_name]["temperature"] = self.temperature
        as_dict[sec_name]["charge"] = self.charge
        as_dict[sec_name]["mass"] = self.mass
        return as_dict
