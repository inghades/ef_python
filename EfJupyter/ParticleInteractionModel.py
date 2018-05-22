class ParticleInteractionModel:

    def __init__( self, particle_interaction_model = "PIC" ):
        self.particle_interaction_model = particle_interaction_model

    def visualize( self, ax ):
        pass

    def export( self ):
        # todo: use representation of class as dict
        as_dict = {}
        as_dict["Particle interaction model"] = {}
        as_dict["Particle interaction model"]["particle_interaction_model"] = \
                                                    self.particle_interaction_model
        return as_dict
