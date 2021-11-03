from jinja2 import Template, Environment, FileSystemLoader
import re

vm_output_file = "Output-code/outputvm.tf"
network_output_file = "Output-code/outputNetwork.tf"
db_output_file = "Output-code/outputdb.tf"

vm_template_path = "VM-templates/"
network_template_path = "Network-templates/"
db_template_path = "DB-templates/"

def vm(parametri):
    finalString = ""
    jinjaTemplate = Template(open(vm_template_path+"templatevm.txt", "r").read())
    for parametro in parametri:
        my_dict = {'vm':'aws_ami', 'os': 'ubuntu', 'executable_users':["self"], 'mostrecent': 'true', 'name_regex': "^myami-\\d{3}", 'owners': ["self"], 'sigla':None, 'cpu':'2', 'ram':'2', 'filter': [{'name': 'name', 'values':["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]}, {'name': 'virtualization-type', 'values': ["hvm"]}]}
        if 'vm' in parametro:
            my_dict['vm'] = parametro['vm']
        if 'os' in parametro:
            my_dict['os'] = parametro['os']
        if 'executable_users'in parametro:
            my_dict['executable_users'] = parametro['executable_users']
        if 'mostrecent' in parametro:
            my_dict['mostrecent'] = parametro['mostrecent']
        if 'name_regex' in parametro:
            my_dict['name_regex'] = parametro['name_regex']
        if 'owners' in parametro:
            my_dict['owners'] = parametro['owners']
        if 'filter' in parametro:
            my_dict['filter'] = parametri['filter']
        if 'cpu' in parametro:
            my_dict['cpu'] = parametro['cpu']
        if 'ram' in parametro:
            my_dict['ram'] = parametro['ram']
        if 'sigla' in parametro:
            my_dict['sigla'] = parametro['sigla']
            from amazon import amazon
            my_dict['instance_type'] = amazon(my_dict['cpu'], my_dict['ram'], my_dict['sigla'])
        if my_dict['sigla'] is None:
            from amazon import amz
            my_dict['instance_type'] = amz(my_dict['cpu'], my_dict['ram'])
        if 'instance_type' in parametro:
            my_dict['instance_type'] = parametro['instance_type']
        tm = Template("filter {\n   name   = \"{{ name }}\"\n   values = {{ values }}\n  }")
        string = ''
        for elem in my_dict['filter']:
            rend = tm.render(name=elem['name'], values=elem['values'])
            string = string+rend+'\n   '
        render = jinjaTemplate.render(my_dict, filters=string)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"

    salvataggio = open(vm_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def gcp(parametri):
    finalString = ""
    jinjaTemplate = Template(open(vm_template_path+"templategcp.txt", "r").read())
    for parametro in parametri:
        my_dict = {'default': 'default', 'name': 'test', 'machine_type': 'e2-medium', 'zone': 'us-central1-a'}
        if 'default' in parametro:
            my_dict['default'] = parametro['default']
        if 'name' in parametro:
            my_dict['name'] = parametro['name']
        if 'machine_type' in parametro:
            my_dict['machine_type'] = parametro['machine_type']
        if 'zone' in parametro:
           my_dict['zone'] = parametro['zone']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    salvataggio = open(vm_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def azurem(parametri):
    finalString = ""
    jinjaTemplate = Template(open(vm_template_path+"templateaz.txt", "r").read())
    for parametro in parametri:
        my_dict = {'source': "hashicorp/azurerm", 'version': "~>2.0", 'name': "<resource_group_name>", 'location': "<location>"}
        if 'source' in parametro:
            my_dict['source'] = parametro['source']
        if 'version' in parametro:
            my_dict['version'] = parametro['version']
        if 'name' in parametro:
            my_dict['name'] = parametro['name']
        if 'location' in parametro:
            my_dict['location'] = parametro['location']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    salvataggio = open(vm_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def networkaws(parametri):
    finalString = ""
    jinjaTemplate = Template(open(network_template_path+"templateNetworkaws.txt", "r").read())
    for parametro in parametri:
        my_dict = {'subname':'subname', 'vpcname': 'vpcname'}
        if 'subname' in parametro:
            my_dict['subname'] = parametro['subname']
        if 'vpcname' in parametro:
            my_dict['vpcname'] = parametro['vpcname']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"

    salvataggio = open(network_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def networkg(parametri):
    finalString = ""
    jinjaTemplate = Template(open(network_template_path+"templateNetworkg.txt", "r").read())
    for parametro in parametri:
        my_dict = {'network':'terraform-network', 'subnetwork': 'terraform-subnetwork'}
        if 'network' in parametro:
            my_dict['network'] = parametro['network']
        if 'subnetwork' in parametro:
            my_dict['subnetwork'] = parametro['subnetwork']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    salvataggio = open(network_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def networkaz(parametri):
    finalString = ""
    jinjaTemplate = Template(open(network_template_path+"templateNetworkaz.txt", "r").read())
    for parametro in parametri:
        my_dict = {'name':'my-resources', 'subnet_names': ["subnet1", "subnet2", "subnet3"]}
        if 'name' in parametro:
            my_dict['name'] = parametro['name']
        if 'subnet_names' in parametro:
            my_dict['subnet_names'] = parametro['subnet_names']
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

    salvataggio = open(network_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def awsdb(parametri):
    finalString = ""
    jinjaTemplate = Template(open(db_template_path+"templateawsdb.txt", "r").read())
    for parametro in parametri: 
        my_dict = {'identifier':'education', 'instance':'db.t3.micro', 'storage':'5', 'engine':'postgres', 'version':'13.1', 'username': 'edu', 'password':'var.db_password', 'subnet': 'aws_db_subnet_group.education.name', 'security': '[aws_security_group.rds.id]', 'parameter': 'aws_db_parameter_group.education.name', 'accessible': 'true', 'skip': 'true'}
        if 'identifier' in parametro:
            my_dict['identifier'] = parametro['identifier']
        if 'instance' in parametro:
            my_dict['instance'] = parametro['instance']
        if 'storage' in parametro:
            my_dict['storage'] = parametro['storage']
        if 'engine' in parametro:
            my_dict['engine'] = parametro['engine']
        if 'version' in parametro:
            my_dict['version'] = parametro['version']
        if 'username' in parametro:
            my_dict['username'] = parametro['username']
        if 'password' in parametro:
            my_dict['password'] = parametro['password']
        if 'subnet' in parametro:
            my_dict['subnet'] = parametro['subnet']
        if 'security' in parametro:
            my_dict['security'] = parametro['security']
        if 'parameter' in parametro:
            my_dict['parameter'] = parametro['parameter']
        if 'accessible' in parametro:
            my_dict['accessible'] = parametro['accessible']
        if 'skip' in parametro:
            my_dict['skip'] = parametro['skip']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    salvataggio = open(db_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def azuredb(parametri):
    finalString = ""
    jinjaTemplate = Template(open(db_template_path+"templateazuredb.txt", "r").read())
    for parametro in parametri:
        my_dict = {'name':'sqldbtf01', 'group_name':'${azurerm_resource_group.test2.name}', 'location':'North Central US', 'server_name':'${azurerm_sql_server.test2.name}', 'state':'Enabled', 'email':'["dbgrl93@gmail.com"]', 'days':'30', 'access_key':'${azurerm_storage_account.test2sa.primary_access_key}', 'endpoint':'${azurerm_storage_account.test2sa.primary_blob_endpoint}', 'default':'Enabled'}
        if 'name' in parametro:
            my_dict['name'] = parametro['name']
        if 'group_name' in parametro:
            my_dict['group_name'] = parametro['group_name']
        if 'location' in parametro:
            my_dict['location'] = parametro['location']
        if 'engine' in parametro:
            my_dict['server_name'] = parametro['server_name']
        if 'version' in parametro:
            my_dict['server_name'] = parametro['server_name']
        if 'state' in parametro:
            my_dict['state'] = parametro['state']
        if 'email' in parametro:
            my_dict['email'] = parametro['email']
        if 'days' in parametro:
            my_dict['days'] = parametro['days']
        if 'access_key' in parametro:
            my_dict['access_key'] = parametro['access_key']
        if 'endpoint' in parametro:
            my_dict['endpoint'] = parametro['endpoint']
        if 'default' in parametro:
            my_dict['default'] = parametro['v']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    salvataggio = open(db_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def googlesql(parametri):
    finalString = ""
    jinjaTemplate = Template(open(db_template_path+"templategoogledb.txt", "r").read())
    for parametro in parametri:
        my_dict = {'name':'my-database', 'instance':'google_sql_database_instance.instance.name', 'instance_name':'my-database-instance','region':'us-central1', 'tier':'db-f1-micro', 'deletion_protection':'true'}
        if 'name' in parametro:
            my_dict['name'] = parametro['name']
        if 'instance' in parametro:
            my_dict['instance'] = parametro['instance']
        if 'instance_name' in parametro:
            my_dict['instance_name'] = parametro['instance_name']
        if 'region' in parametro:
            my_dict['region'] = parametro['region']
        if 'tier' in parametro:
            my_dict['tier'] = parametro['tier']
        if 'deletion_protection' in parametro:
            my_dict['deletion_protection'] = parametro['deletion_protection']
        render = jinjaTemplate.render(my_dict)
        render = re.sub("'", "\"", render)
        finalString = finalString+render+"\n"
        
    salvataggio = open(db_output_file, "w")
    salvataggio.write(finalString)
    salvataggio.close()

def postgresql(parametri):
    jinjaTemplate = Template(open(db_template_path+"templateawsdb.txt", "r").read())
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
    salvataggio = open(db_output_file, "w")
    salvataggio.write(render)
    salvataggio.close()
