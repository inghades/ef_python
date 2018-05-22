import os
import shlex
import tempfile
import subprocess
import configparser

import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

from TimeGrid import TimeGrid
from SpatialMesh import SpatialMesh
from BoundaryConditions import BoundaryConditions
from OutputFile import OutputFile
from ParticleInteractionModel import ParticleInteractionModel
from ParticleSources import ParticleSourceBox, ParticleSourceCylinder
from InnerRegions import InnerRegionTubeAlongZSegment
from ExternalFields import ExternalFieldElectricOnRegularGridFromH5File


class EfConf:
    def __init__( self ):
        self.time_grid = TimeGrid()
        self.spatial_mesh = SpatialMesh()
        self.sources = []
        self.inner_regions = []
        self.output_file = OutputFile()
        self.boundary_conditions = BoundaryConditions()
        self.particle_interaction_model = ParticleInteractionModel()
        self.ex_fields = []

    def add_source( self, src ):
        self.sources.append( src )

    def add_inner_region( self, ir ):
        self.inner_regions.append( ir )

    def add_ex_field ( self, ef ):
        self.ex_fields.append( ef )
        
    def visualize( self, equal_aspect = True ):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        self.time_grid.visualize( ax )
        self.spatial_mesh.visualize( ax )
        for src in self.sources:
            src.visualize( ax )
        for ir in self.inner_regions:
            ir.visualize( ax )
        for ef in self.ex_fields:
            ef.visualize( ax )
        #
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        #
        if equal_aspect:
            self.axis_equal_3d( ax )
        plt.rcParams["figure.figsize"] = [ 9, 8 ]
        #
        plt.show()


    def axis_equal_3d( self, ax ):
        # https://stackoverflow.com/questions/8130823/set-matplotlib-3d-plot-aspect-ratio
        extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
        sz = extents[:,1] - extents[:,0]
        centers = np.mean(extents, axis=1)
        maxsize = max(abs(sz))
        r = maxsize/2
        for ctr, dim in zip(centers, 'xyz'):
            getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

        
    def export( self, filename ):
        as_dict = {}
        as_dict.update( self.time_grid.export()  )
        as_dict.update( self.spatial_mesh.export() )        
        for src in self.sources:
            as_dict.update( src.export() )
        for ir in self.inner_regions:
            as_dict.update( ir.export() )
        as_dict.update( self.output_file.export() )
        as_dict.update( self.boundary_conditions.export() )
        as_dict.update( self.particle_interaction_model.export() )
        for ef in self.ex_fields:
            as_dict.update( ef.export() )
        # can't construct config from dictionary; have to do it manually
        # config = configparser.ConfigParser( as_dict )
        config = configparser.ConfigParser()
        for sec_name, sec in as_dict.items():
            config[sec_name] = {}
            for k, v in sec.items():
                config[sec_name][k] = str(v)
        with open( filename, 'w') as f:
            config.write( f )


    def print_config( self ):
        as_dict = {}
        as_dict.update( self.time_grid.export()  )
        as_dict.update( self.spatial_mesh.export() )        
        for src in self.sources:
            as_dict.update( src.export() )
        for ir in self.inner_regions:
            as_dict.update( ir.export() )
        as_dict.update( self.output_file.export() )
        as_dict.update( self.boundary_conditions.export() )
        as_dict.update( self.particle_interaction_model.export() )
        for ef in self.ex_fields:
            as_dict.update( ef.export() )
        for sec_name, sec in as_dict.items():
            print( "[" + sec_name + "]" )
            for k, v in sec.items():
                print( k, " = ", v )
            print()

            
    def run( self, ef_command = "python3 ../../main.py", workdir = "./",
             save_config_as = None ):
        current_dir = os.getcwd()
        os.chdir( workdir )
        if save_config_as:
            self.export( save_config_as )
            command = ef_command + " " + save_config_as
        else:
            tmpfile, tmpfilename = tempfile.mkstemp( suffix = ".ini", text = True )
            self.export( tmpfilename )
            command = ef_command + " " + tmpfilename
        print( "command:", command )
        self.run_command( command )
        #stdout = subprocess.Popen( command, shell = True,
        #                           stdout = subprocess.PIPE ).stdout.read()
        # Jupyter magick
        # !{command}
        #print( stdout )
        if tmpfile:
            os.remove( tmpfilename )
        os.chdir( current_dir )


    @classmethod
    def run_from_file( cls, startfile,
                       ef_command = "python3 ../../main.py",
                       workdir = "./" ):
        current_dir = os.getcwd()
        os.chdir( workdir )
        command = ef_command + " " + startfile
        print( "command:", command )
        stdout = subprocess.Popen( command, shell = True,
                                   stdout = subprocess.PIPE ).stdout.read()
        print( stdout )
        os.chdir( current_dir )


    def run_command( self, command ):
        #https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print( output.strip() )
        rc = process.poll()
        return rc
    # try instead
    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
