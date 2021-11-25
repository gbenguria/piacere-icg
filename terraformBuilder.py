import json
import yaml
from terraforUtils import *
import sys
 

def TerraformICG(parameters):
    if 'vm' in parameters:
        if (parameters['provider']=='aws'):
            if 'vm' in parameters:
                awsvm(parameters['vm'])
            if 'network' in parameters:
                networkaws(parameters['network'])
            if 'db' in parameters:
                awsdb(parameters['db'])
        elif (parameters['provider']=='gcp'):
            gcpvm(parameters['vm'])
            if 'network' in parameters:
                networkg(parameters['network'])
            if 'db' in parameters:
                googlesql(parameters['db'])
        elif (parameters['provider']=='azure'):
            azurevm(parameters['vm'])
            if 'network' in parameters:
                networkaz(parameters['network'])
            if 'db' in parameters:
                azuredb(parameters['db'])