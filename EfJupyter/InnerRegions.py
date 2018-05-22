class InnerRegionTubeAlongZSegment():
    def __init__( self, name = 'segment',
                  potential = 0,
                  tube_segment_axis_x = 6, tube_segment_axis_y = 5,
                  tube_segment_axis_start_z = 2, tube_segment_axis_end_z = 5,
                  tube_segment_inner_radius = 1, tube_segment_outer_radius = 3,
                  tube_segment_start_angle_deg = 0, tube_segment_end_angle_deg = 45 ):
        self.name = name
        self.potential = potential
        self.tube_segment_axis_x = tube_segment_axis_x
        self.tube_segment_axis_y = tube_segment_axis_y
        self.tube_segment_axis_start_z = tube_segment_axis_start_z
        self.tube_segment_axis_end_z = tube_segment_axis_end_z
        self.tube_segment_inner_radius = tube_segment_inner_radius
        self.tube_segment_outer_radius = tube_segment_outer_radius
        self.tube_segment_start_angle_deg = tube_segment_start_angle_deg
        self.tube_segment_end_angle_deg = tube_segment_end_angle_deg


    def visualize( self, ax ):
        self.draw_segment( ax )


    def draw_segment( self, ax ):
        vertices = []
        shift_x = self.tube_segment_axis_x
        shift_y = self.tube_segment_axis_y
        phi1 = self.tube_segment_start_angle_deg / 180.0 * np.pi
        phi2 = self.tube_segment_end_angle_deg / 180.0 * np.pi
        arc_step = 5.0 / 180.0 * np.pi
        r1 = self.tube_segment_inner_radius
        r2 = self.tube_segment_outer_radius
        z1 = self.tube_segment_axis_start_z
        z2 = self.tube_segment_axis_end_z
        vertices.append( [shift_x + r1 * np.cos(phi1), shift_y + r1 * np.sin(phi1), z1] )
        for phi in np.arange( phi1, phi2, arc_step ):
            vertices.append( [shift_x + r1 * np.cos(phi), shift_y + r1 * np.sin(phi), z1] )
        vertices.append( [shift_x + r1 * np.cos(phi2), shift_y + r1 * np.sin(phi2), z1] )
        vertices.append( [shift_x + r2 * np.cos(phi2), shift_y + r2 * np.sin(phi2), z1] )
        for phi in np.arange( phi2, phi1, -arc_step ):
            vertices.append( [shift_x + r2 * np.cos(phi), shift_y + r2 * np.sin(phi), z1] )
        vertices.append( [shift_x + r2 * np.cos(phi1), shift_y + r2 * np.sin(phi1), z1] )
        vertices.append( [shift_x + r1 * np.cos(phi1), shift_y + r1 * np.sin(phi1), z1] )
        vertices.append( [shift_x + r1 * np.cos(phi1), shift_y + r1 * np.sin(phi1), z2] )
        for phi in np.arange( phi1, phi2, arc_step ):
            vertices.append( [shift_x + r1 * np.cos(phi), shift_y + r1 * np.sin(phi), z2] )
        vertices.append( [shift_x + r1 * np.cos(phi2), shift_y + r1 * np.sin(phi2), z2] )
        vertices.append( [shift_x + r1 * np.cos(phi2), shift_y + r1 * np.sin(phi2), z1] )
        vertices.append( [shift_x + r1 * np.cos(phi2), shift_y + r1 * np.sin(phi2), z2] )
        vertices.append( [shift_x + r2 * np.cos(phi2), shift_y + r2 * np.sin(phi2), z2] )
        vertices.append( [shift_x + r2 * np.cos(phi2), shift_y + r2 * np.sin(phi2), z1] )
        vertices.append( [shift_x + r2 * np.cos(phi2), shift_y + r2 * np.sin(phi2), z2] )
        for phi in np.arange( phi2, phi1, -arc_step ):
            vertices.append( [shift_x + r2 * np.cos(phi), shift_y + r2 * np.sin(phi), z2] )
        vertices.append( [shift_x + r2 * np.cos(phi1), shift_y + r2 * np.sin(phi1), z2] )
        vertices.append( [shift_x + r2 * np.cos(phi1), shift_y + r2 * np.sin(phi1), z1] )
        vertices.append( [shift_x + r2 * np.cos(phi1), shift_y + r2 * np.sin(phi1), z2] )
        vertices.append( [shift_x + r1 * np.cos(phi1), shift_y + r1 * np.sin(phi1), z2] )
        x = [ v[0] for v in vertices ]
        y = [ v[1] for v in vertices ]
        z = [ v[2] for v in vertices ]
        ax.plot( x, y, z, label=self.name )


    def export( self ):
        as_dict = {}
        sec_name = "Inner_region_tube_along_z_segment" + "." + self.name
        as_dict[sec_name] = {}
        as_dict[sec_name]["potential"] = self.potential
        as_dict[sec_name]["tube_segment_axis_x"] = self.tube_segment_axis_x
        as_dict[sec_name]["tube_segment_axis_y"] = self.tube_segment_axis_y
        as_dict[sec_name]["tube_segment_axis_start_z"] = self.tube_segment_axis_start_z
        as_dict[sec_name]["tube_segment_axis_end_z"] = self.tube_segment_axis_end_z
        as_dict[sec_name]["tube_segment_inner_radius"] = self.tube_segment_inner_radius
        as_dict[sec_name]["tube_segment_outer_radius"] = self.tube_segment_outer_radius
        as_dict[sec_name]["tube_segment_start_angle_deg"] = \
                            self.tube_segment_start_angle_deg
        as_dict[sec_name]["tube_segment_end_angle_deg"] = \
                            self.tube_segment_end_angle_deg
        return as_dict        
