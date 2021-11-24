import json
import yaml
#import toscaparser
import sys
 

def TerraformICG(parameters):
    if 'vm' in parameters:
        if (parameters['provider']=='aws'):
            if 'vm' in parameters:
                from functions import awsvm
                awsvm(parameters['vm'])
            if 'network' in parameters:
                from functions import networkaws
                networkaws(parameters['network'])
            if 'db' in parameters:
                from functions import awsdb
                awsdb(parameters['db'])
        elif (parameters['provider']=='gcp'):
            from functions import gcpvm
            gcpvm(parameters['vm'])
            if 'network' in parameters:
                from functions import networkg
                networkg(parameters['network'])
            if 'db' in parameters:
                from functions import googlesql
                googlesql(parameters['db'])
        elif (parameters['provider']=='azure'):
            from functions import azurevm
            azurevm(parameters['vm'])
            if 'network' in parameters:
                from functions import networkaz
                networkaz(parameters['network'])
            if 'db' in parameters:
                from functions import azuredb
                azuredb(parameters['db'])