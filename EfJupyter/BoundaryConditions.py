class BoundaryConditions:

    def __init__( self,
                  boundary_phi_right = 0, boundary_phi_left = 0,
                  boundary_phi_bottom = 0, boundary_phi_top = 0,
                  boundary_phi_near = 0, boundary_phi_far = 0 ):
        self.boundary_phi_right = boundary_phi_right
        self.boundary_phi_left = boundary_phi_left
        self.boundary_phi_bottom = boundary_phi_bottom
        self.boundary_phi_top = boundary_phi_top
        self.boundary_phi_near = boundary_phi_near
        self.boundary_phi_far = boundary_phi_far


    def visualize( self, ax ):
        pass

    
    def export( self ):
        as_dict = {}        
        as_dict["Boundary conditions"] = {}
        as_dict["Boundary conditions"]["boundary_phi_right"] = self.boundary_phi_right
        as_dict["Boundary conditions"]["boundary_phi_left"] = self.boundary_phi_left
        as_dict["Boundary conditions"]["boundary_phi_bottom"] = self.boundary_phi_bottom
        as_dict["Boundary conditions"]["boundary_phi_top"] = self.boundary_phi_top
        as_dict["Boundary conditions"]["boundary_phi_near"] = self.boundary_phi_near
        as_dict["Boundary conditions"]["boundary_phi_far"] = self.boundary_phi_far
        return as_dict        
