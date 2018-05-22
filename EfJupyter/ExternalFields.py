class ExternalFieldElectricOnRegularGridFromH5File():

    def __init__( self, name = "elec_file", filename = "field.h5" ):
        self.name = name
        self.filename = filename

    def visualize( self, ax ):
        pass

    def export( self ):
        as_dict = {}
        sec_name = "ExternalFieldElectricOnRegularGridFromH5File" + "." + self.name
        as_dict[sec_name] = {}
        as_dict[sec_name]["filename"] = self.filename
        return as_dict
