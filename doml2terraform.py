import json
import yaml
#import toscaparser
import sys
 

def TerraformICG(parametri):
    if 'vm' in parametri:
        if (parametri['provider']=='aws'):
            from functions import vm
            vm(parametri['vm'])
            if 'network' in parametri:
                from functions import networkaws
                networkaws(parametri['network'])
            if 'db' in parametri:
                from functions import awsdb
                awsdb(parametri['db'])
        elif (parametri['provider']=='gcp'):
            from functions import gcp
            gcp(parametri['vm'])
            if 'network' in parametri:
                from functions import networkg
                networkg(parametri['network'])
            if 'db' in parametri:
                from functions import googlesql
                googlesql(parametri['db'])
        elif (parametri['provider']=='azurerm'):
            from functions import azurem
            azurem(parametri['vm'])
            if 'network' in parametri:
                from functions import networkaz
                networkaz(parametri['network'])
            if 'db' in parametri:
                from functions import azuredb
                azuredb(parametri['db'])