class OutputFile:
    def __init__( self, output_filename_prefix = "out_", output_filename_suffix = ".h5" ):
        self.output_filename_prefix = output_filename_prefix
        self.output_filename_suffix = output_filename_suffix

    def visualize( self, ax ):
        pass


    def export( self ):
        # todo: use representation of class as dict
        as_dict = {}
        as_dict["Output filename"] = {}
        as_dict["Output filename"]["output_filename_prefix"] = self.output_filename_prefix
        as_dict["Output filename"]["output_filename_suffix"] = self.output_filename_suffix
        return as_dict
