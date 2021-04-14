from ctypes import *
from list_bodies import *
from error_codes import *

import sys
import os

class spyce_core:
    
      
    SPYCE_LIB = "../../"
    CSPICE_LIB =" ../../lib/cspice.so"
    model_file_location="model.dat"
    CSPICE=None;
    
    
    list_bodies_array=[]
    list_kernels=[]
    
    
    # Core variables, do not alter, or assign directly
    
    IMAX=180 # The max number of bodies in JPL's ephemerides. 
    
    MU_LENGTH_2=113
    
    ISPC=False
      
    # This constructor initialises all of SPYCE global variables.
    #
    
    IBC=0 #IBC is the system's barycentre. Default value is 0, which is the solary system barycentre.
    
    
    

    REF_FRAME='J2000'
    ABCORR = 'NONE'
    
    def __init__(self, i_spyce_lib_location, i_cspice_lib_location, i_model_file_location):
        """
        Starts the SPYCE Core system.

        Parameters
        ----------
        i_spyce_lib_location : str
            Path to SPYCE's root directory.
        i_cspice_lib_location : str
            Path to cspice.so
        i_model_file_location : str
            Path to model.dat.

        Returns
        -------
        None.

        """
        
        
        self.SPYCE_LIB=i_spyce_lib_location
        self.CSPICE_LIB=i_cspice_lib_location
        self.CSPICE=CDLL(i_cspice_lib_location);
        model_file_location=i_model_file_location
        
        self.read_model_spyce(model_file_location)
        return
    
    def read_model_spyce(self, model_file):
        """
        
    
        Parameters
        ----------
        model_file : str
            DESCRIPTION.
    
        Returns
        -------
        None.
    
        """
        with open(model_file) as f:
            content = f.readlines()
        # Now that we know the length of model.dat file, we can define the variable MMAX, and use it to initialise other important variables.
        
        #MMAX = len(content)
       

        for line in content:
           new_body=spyce_list_bodies()
           if(self.check_list_array_forID(line.strip())==False):
               
               new_body.set_ID(line.strip())
               eph_temp=new_body.get_ibc_eph_ref_by_id(line,self)
               new_body.set_ibc_eph(eph_temp[1])
               self.add_kernelNametoList(eph_temp[0])
               self.list_bodies_array.append(new_body)
        
        self.load_kernels_all()        
        return
    

    def check_list_array_forID(self, b_id):
        """
        

        Parameters
        ----------
        spyce_core_obj : obj
            spyce_core class Object.
        b_id : str
            ID of the body read from the model.dat file.

        Returns
        -------
        True if bodyid is already in array. False if the bodyid is unique.

        """
        
        if(len(self.list_bodies_array)>0):
            found=False
            for body in self.list_bodies_array:
                if(body.get_ID().strip()==b_id.strip()):
                    found=True
            
            return found
        else:
            return False
        
        
        
        return
    
    
    def add_kernelNametoList(self, kernel_name_toadd):
            
        found=False
            
        for kernel in self.list_kernels:
            if(kernel_name_toadd.strip()==kernel):
                found=True
                        
        if(found==False):
            self.list_kernels.append(kernel_name_toadd)
             
        return
        

        
    def load_kernels_all(self):
        cDLL=self.return_SPICE_Object()
        for kernel in self.list_kernels:
            kernel_path=self.SPYCE_LIB+"eph/"+kernel
            cDLL.furnsh_c(kernel_path.encode('utf-8'))
        
        # Now that the required ephemerides have been loaded, we load the leapsecond kernel

        if(self.ISPC):
            kernel_path=self.SPYCE_LIB+"gkernels/naif0012.tls.pc"
        else:
            kernel_path=self.SPYCE_LIB+"gkernels/naif0012.tls"
        
        cDLL.furnsh_c(kernel_path.encode('utf-8'))
        
        kernel_path=self.SPYCE_LIB+"gkernels/gm_de431.tpc"
        cDLL.furnsh_c(kernel_path.encode('utf-8'))
        kernel_path=self.SPYCE_LIB+"gkernels/latest_leapseconds.tls"
        cDLL.furnsh_c(kernel_path.encode('utf-8'))
        
        return
    
    
    def return_SPICE_Object(self): 
        path=self.CSPICE_LIB
        return CDLL(path);
    

    def set_IBC(self, ibc):
        self.IBC=ibc
        return
    
    def get_IBC(self):
        return self.IBC;
    