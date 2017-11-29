#! /usr/bin/python                                                                       
                                                                                         
import os                                                                                
                                                                                         
filepath = (os.path.dirname(os.path.abspath(__file__)) + '/env.conf')                                                           
variables = dict(line.strip().split('=') for line in open(filepath))                 
for k, v in variables.items():                                                       
    if not v:                                                                        
       exit(1)
