class TimeGrid:

    def __init__( self, total_time = 100.0, time_save_step = 10.0, time_step_size = 1.0 ):
        self.total_time = total_time
        self.time_save_step = time_save_step
        self.time_step_size = time_step_size


    def visualize( self, ax ):
        pass


    def export( self ):
        # todo: use representation of class as dict
        as_dict = {}
        as_dict["Time grid"] = {}
        as_dict["Time grid"]["total_time"] = self.total_time        
        as_dict["Time grid"]["time_save_step"] = self.time_save_step
        as_dict["Time grid"]["time_step_size"] = self.time_step_size
        return as_dict
