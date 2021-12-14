from jinja2 import Template, Environment, FileSystemLoader
import re
from aws import *

def awsvm(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/VM-templates/AWStemplateVM.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'vm':'aws_ami',
                    'id': '1', 
                    'id': 'vm1', 
                    'os': 'ubuntu', 
                    'executable_users':["self"], 
                    'mostrecent': 'true', 
                    'name_regex': "^myami-\\d{3}", 
                    'owners': ["self"], 
                    'type':None, 
                    'cpu':'2', 
                    'ram':'2', 
                    'filter': [{'name': 'name', 'values':["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]}, 
                                {'name': 'virtualization-type', 'values': ["hvm"]}]
                }
        if 'vm' in parameter:
            my_dict['vm'] = parameter['vm']
        if 'id' in parameter:
            my_dict['id'] = parameter['id']
        if 'name' in parameter:
            my_dict['name'] = parameter['name']
        if 'os' in parameter:
            my_dict['name_regex'] = parameter['os']+"*"
        if 'executable_users'in parameter:
            my_dict['executable_users'] = parameter['executable_users']
        if 'mostrecent' in parameter:
            my_dict['mostrecent'] = parameter['mostrecent']
        if 'name_regex' in parameter:
            my_dict['name_regex'] = parameter['name_regex']
        if 'owners' in parameter:
            my_dict['owners'] = parameter['owners']
        if 'filter' in parameter:
            my_dict['filter'] = parametri['filter']
        if 'cpu' in parameter:
            my_dict['cpu'] = parameter['cpu']
        if 'ram' in parameter:
            my_dict['ram'] = parameter['ram']
        if 'type' in parameter:
            my_dict['type'] = parameter['type']
            my_dict['instance_type'] = vmcatalog1(my_dict['cpu'], my_dict['ram'], my_dict['sigla'])
        if my_dict['type'] is None:
            my_dict['instance_type'] = vmcatalog(my_dict['cpu'], my_dict['ram'])
        if 'instance_type' in parameter:
            my_dict['instance_type'] = parameter['instance_type']
        tm = Template("filter {\n   name   = \"{{ name }}\"\n   values = {{ values }}\n  }")
        string = ''
        render = jinjaTemplate.render(my_dict, filters=string)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"

    create_file = open("Output-code/outputvm.tf", "w")
    create_file.write(finalString)
    create_file.close()

def gcpvm(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/VM-templates/GCPtemplateVM.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'default': 'default', 'name': 'test', 'machine_type': 'e2-medium', 'zone': 'us-central1-a'}
        if 'default' in parameter:
            my_dict['default'] = parameter['default']
        if 'name' in parameter:
            my_dict['name'] = parameter['name']
        if 'machine_type' in parameter:
            my_dict['machine_type'] = parameter['machine_type']
        if 'zone' in parameter:
           my_dict['zone'] = parameter['zone']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    create_file = open("Output-code/outputvm.tf", "w")
    create_file.write(finalString)
    create_file.close()

def azurevm(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/VM-templates/AZUREtemplateVM.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'source': "hashicorp/azurerm", 'version': "~>2.0", 'name': "<resource_group_name>", 'location': "<location>"}
        if 'source' in parameter:
            my_dict['source'] = parameter['source']
        if 'version' in parameter:
            my_dict['version'] = parameter['version']
        if 'name' in parameter:
            my_dict['name'] = parameter['name']
        if 'location' in parameter:
            my_dict['location'] = parameter['location']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    create_file = open("Output-code/outputvm.tf", "w")
    create_file.write(finalString)
    create_file.close()

def networkaws(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/Network-templates/AWStemplateNetwork.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'subname':'subname', 'vpcname': 'vpcname', 'subnet_cidrblock':'subnet_cidrblock', 'vpc_cidr': 'vpc_cidr'}
        if 'subnet_cidrblock' in parameter:
            my_dict['subnet_cidrblock'] = parameter['subnet_cidrblock']
        if 'vpc_cidr' in parameter:
            my_dict['vpc_cidr'] = parameter['vpc_cidr']
        if 'subnetname' in parameter:
            my_dict['subnetname'] = parameter['subnetname']
        if 'vpcname' in parameter:
            my_dict['vpcname'] = parameter['vpcname']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"

    create_file = open("Output-code/outputNetwork.tf", "w")
    create_file.write(finalString)
    create_file.close()

def networkg(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/Network-templates/GCPtemplateNetwork.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'network':'terraform-network', 'subnetwork': 'terraform-subnetwork'}
        if 'network' in parameter:
            my_dict['network'] = parameter['network']
        if 'subnetwork' in parameter:
            my_dict['subnetwork'] = parameter['subnetwork']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    create_file = open("Output-code/outputNetwork.tf", "w")
    create_file.write(finalString)
    create_file.close()

def networkaz(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/Network-templates/AZUREtemplateNetwork.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'name':'my-resources', 'subnet_names': ["subnet1", "subnet2", "subnet3"]}
        if 'name' in parameter:
            my_dict['name'] = parameter['name']
        if 'subnet_names' in parameter:
            my_dict['subnet_names'] = parameter['subnet_names']
        tm = Template("\"{{ name }}\" : [\"Microsoft.Sql\"]")
        string = ''
        i = len(my_dict['subnet_names'])
        for elem in my_dict['subnet_names']:
            rend = tm.render(name = elem)
            string = string+rend
            i = i-1
            if i>0:
                string = string+",\n    "
        render = jinjaTemplate.render(my_dict, endpoints=string)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"

    create_file = open("Output-code/outputNetwork.tf", "w")
    create_file.write(finalString)
    create_file.close()

def awsdb(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/DB-templates/AWStemplateDB.tpl", "r").read())
    for parameter in parametri: 
        my_dict = {'identifier':'education', 'instance':'db.t3.micro', 'storage':'5', 'engine':'postgres', 'version':'13.1', 'username': 'edu', 'password':'var.db_password', 'subnet': 'aws_db_subnet_group.education.name', 'security': '[aws_security_group.rds.id]', 'parameter': 'aws_db_parameter_group.education.name', 'accessible': 'true', 'skip': 'true'}
        if 'identifier' in parameter:
            my_dict['identifier'] = parameter['identifier']
        if 'instance' in parameter:
            my_dict['instance'] = parameter['instance']
        if 'storage' in parameter:
            my_dict['storage'] = parameter['storage']
        if 'engine' in parameter:
            my_dict['engine'] = parameter['engine']
        if 'version' in parameter:
            my_dict['version'] = parameter['version']
        if 'username' in parameter:
            my_dict['username'] = parameter['username']
        if 'password' in parameter:
            my_dict['password'] = parameter['password']
        if 'subnet' in parameter:
            my_dict['subnet'] = parameter['subnet']
        if 'security' in parameter:
            my_dict['security'] = parameter['security']
        if 'parameter' in parameter:
            my_dict['parameter'] = parameter['parameter']
        if 'accessible' in parameter:
            my_dict['accessible'] = parameter['accessible']
        if 'skip' in parameter:
            my_dict['skip'] = parameter['skip']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    create_file = open("Output-code/outputdb.tf", "w")
    create_file.write(finalString)
    create_file.close()

def azuredb(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/DB-templates/AZUREtemplateDB.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'name':'sqldbtf01', 'group_name':'${azurerm_resource_group.test2.name}', 'location':'North Central US', 'server_name':'${azurerm_sql_server.test2.name}', 'state':'Enabled', 'email':'["dbgrl93@gmail.com"]', 'days':'30', 'access_key':'${azurerm_storage_account.test2sa.primary_access_key}', 'endpoint':'${azurerm_storage_account.test2sa.primary_blob_endpoint}', 'default':'Enabled'}
        if 'name' in parameter:
            my_dict['name'] = parameter['name']
        if 'group_name' in parameter:
            my_dict['group_name'] = parameter['group_name']
        if 'location' in parameter:
            my_dict['location'] = parameter['location']
        if 'engine' in parameter:
            my_dict['server_name'] = parameter['server_name']
        if 'version' in parameter:
            my_dict['server_name'] = parameter['server_name']
        if 'state' in parameter:
            my_dict['state'] = parameter['state']
        if 'email' in parameter:
            my_dict['email'] = parameter['email']
        if 'days' in parameter:
            my_dict['days'] = parameter['days']
        if 'access_key' in parameter:
            my_dict['access_key'] = parameter['access_key']
        if 'endpoint' in parameter:
            my_dict['endpoint'] = parameter['endpoint']
        if 'default' in parameter:
            my_dict['default'] = parameter['v']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    create_file = open("Output-code/outputdb.tf", "w")
    create_file.write(finalString)
    create_file.close()

def googlesql(parametri):
    finalString = ""
    jinjaTemplate = Template(open("/opt/DB-templates/GCPtemplateDB.tpl", "r").read())
    for parameter in parametri:
        my_dict = {'name':'my-database', 'instance':'google_sql_database_instance.instance.name', 'instance_name':'my-database-instance','region':'us-central1', 'tier':'db-f1-micro', 'deletion_protection':'true'}
        if 'name' in parameter:
            my_dict['name'] = parameter['name']
        if 'instance' in parameter:
            my_dict['instance'] = parameter['instance']
        if 'instance_name' in parameter:
            my_dict['instance_name'] = parameter['instance_name']
        if 'region' in parameter:
            my_dict['region'] = parameter['region']
        if 'tier' in parameter:
            my_dict['tier'] = parameter['tier']
        if 'deletion_protection' in parameter:
            my_dict['deletion_protection'] = parameter['deletion_protection']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    create_file = open("Output-code/outputdb.tf", "w")
    create_file.write(finalString)
    create_file.close()

def postgresql(parametri):
    jinjaTemplate = Template(open("/opt/DB-templates/AWStemplateDB.tpl", "r").read())
    my_dict = {'name': 'my_db', 'owner': 'my_role', 'template': 'template0', 'lc_collate':'C', 'connection_limit':-1, 'allow_connections': 'true'}
    if 'name' in parametri:
        my_dict['name'] = parametri['name']
    if 'owner' in parametri:
        my_dict['owner'] = parametri['owner']
    if 'template' in parametri:
        my_dict['template'] = parametri['template']
    if 'lc_collate' in parametri:
        my_dict['lc_collate'] = parametri['lc_collate']
    if 'connection_limit' in parametri:
        my_dict['connection_limit'] = parametri['connection_limit']
    if 'allow_connections' in parametri:
        my_dict['allow_connections'] = parametri['allow_connections']
    render = jinjaTemplate.render(my_dict)
    render = re.sub("'", "\"", render)
    create_file = open("Output-code/outputdb.tf", "w")
    create_file.write(render)
    create_file.close()
