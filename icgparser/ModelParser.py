# -------------------------------------------------------------------------
#		PIACERE ICG Parser
#
#       This module has been tested with Python v3.7.4
#       To use it you must first install PyEcore
#           $ pip install pyecore
#
#       Usage: python icgparser.py [-h] [-d dir] [-v] [--single] model
#           -h          prints usage
#           -d dir      loads metamodel from <dir>
#           --single / --single_mmodel   use the single (non-split) metamodel
#           model       the input model to be translated into the ICG intermediate representation
#
#		Author: Lorenzo Blasi
#		23/2/2022 - created
#		© Copyright 2022 Hewlett Packard Enterprise Development LP
# -------------------------------------------------------------------------
import logging
import sys
from pyecore.resources import ResourceSet, URI, global_registry
import pyecore.ecore as Ecore  # This gets a reference to the Ecore metamodel implementation

# -------------------------------------------------------------------------
# Utility functions to printout the loaded model
# -------------------------------------------------------------------------
newline = "\n"
spaces = "    "
comment = "#"


def write_to(outchannel, line):
    # for now we just print on the console
    if outchannel == "console":
        print(line)
    # if the channel is different we don't print at all


def print_obj(obj, level=0):
    #    for x in range(level):
    #        print("    ", end='')
    class_name = obj.eClass.name
    if class_name == 'Property':
        #        print('Class: {0}\t\t{1} = {2}'.format(class_name, obj.key, obj.value))
        print(f'{comment}{level * spaces}Class: {class_name}\t\t{obj.key} = {obj.value}')
        return False
    if class_name == 'Deployment':
        print(
            f'{comment}{level * spaces}Class: {class_name}\t\tcomponent = {obj.component.eClass.name}/{obj.component.name} node = {obj.node.eClass.name}/{obj.node.name}')
        return False
    try:
        obj_name = obj.name
        print(f'{comment}{level * spaces}Class: {class_name}\t\tObject: {obj_name}')
        return True
    except Exception:
        print(f'{comment}{level * spaces}Class: {class_name}\t\tObject: no name')
        return False


def print_contents_recursive(obj, level=0):
    if print_obj(obj, level):
        for x in obj.eContents:
            print_contents_recursive(x, level + 1)


# -------------------------------------------------------------------------
# Utility functions to produce the output Intermediate Language
# -------------------------------------------------------------------------
# --- Helpers
def extract_image_name(concretevm_obj):
    # To find the VM image name you could search into the inverse relations of the abstract image generating its related abstract VM, looking for a concrete image object (whose class is VMImage) and extract the value from its contents
    #   concretevm_obj is a VirtualMachine (nginx-openstack_v2.doml:81, it should have been a OpenStackVM),
    #   concretevm_obj.maps is a VirtualMachine (the abstract one)
    #   concretevm_obj.maps.generatedFrom is a VMImage (the abstract one)
    for x in concretevm_obj.maps.generatedFrom._inverse_rels:
        if x[0].eClass.name == 'VMImage':
            return x[0].eContents[0].value


def extract_concrete_network_name(abstractnet_obj):
    for x in abstractnet_obj._inverse_rels:
        if x[0].eClass.name == 'Network':
            return x[0].eContents[0].value


# --- Handlers
def model_handler(obj, model_root, level, intermediate_repr):
    # output prefix
    append_in_file(intermediate_repr,
                   f'{level * spaces}{{{newline}{level * spaces}{spaces}"output_path": "output_files_generated/{obj.name}/",')
    append_in_file(intermediate_repr, f'{level * spaces}{spaces}"steps": [')
    # handle contents
    for x in obj.eContents:
        handle_obj(x, model_root, level + 2, intermediate_repr)
    # output suffix
    append_in_file(intermediate_repr, f'{level * spaces}{spaces}]')
    append_in_file(intermediate_repr, f'{level * spaces}}}')


def concrete_infra_handler(obj, model_root, level, intermediate_repr):
    # output prefix
    append_in_file(intermediate_repr, f'{level * spaces}{{{newline}{level * spaces}{spaces}"programming_language": "terraform",')
    # handle contents
    for x in obj.eContents:
        handle_obj(x, model_root, level + 1, intermediate_repr)
    # output suffix
    append_in_file(intermediate_repr, f'{level * spaces}}}')


def network_handler(obj, model_root, level, intermediate_repr):
    # ignore the concrete network, since its name has been extracted separately and included in the concrete VM
    logging.warning('Ignoring Network')


def property_handler(obj, model_root, level, intermediate_repr):
    key = obj.key
    append_in_file(intermediate_repr, f'{level * spaces}"{key}" :     "{obj.value}",')


def provider_handler(obj, model_root, level, intermediate_repr):
    # output prefix
    append_in_file(intermediate_repr, f'{level * spaces}"data": {{{newline}{level * spaces}{spaces}"provider": "{obj.name}",')
    # handle contents
    for x in obj.eContents:
        handle_obj(x, model_root, level + 1, intermediate_repr)
    # output suffix
    append_in_file(intermediate_repr, f'{level * spaces}}}')


def concrete_vm_handler(obj, model_root, level, intermediate_repr):
    # output prefix
    append_in_file(intermediate_repr, f'{level * spaces}"vm": [{{')  # VMs can be more than one: I need an example...
    level = level + 1
    # print(f'{level * spaces}# maps {obj.maps.name}')
    logging.warning(f"Ignoring map {obj.maps.name}")
    # handle contents
    for x in obj.eContents:
        handle_obj(x, model_root, level, intermediate_repr)
    # add other attributes defined elsewhere: image name, address, ...
    append_in_file(intermediate_repr, f'{level * spaces}"image" :     "{extract_image_name(obj)}",')
    for iface in obj.maps.ifaces:
        append_in_file(intermediate_repr, f'{level * spaces}"address" :     "{iface.endPoint}",')
        append_in_file(intermediate_repr, f'{level * spaces}"network_name" :     "{extract_concrete_network_name(iface.belongsTo)}"')
    # output suffix
    level = level - 1
    append_in_file(intermediate_repr, f'{level * spaces}}}]')


def vm_image_handler(obj, model_root, level, intermediate_repr):
    # ignore the concrete image, since its image name has been extracted separately and included in the concrete VM
    logging.warning(f'Ignoring VMImage')


class_handler = {

    "DOMLModel": model_handler,
    "ConcreteInfrastructure": concrete_infra_handler,
    "Network": network_handler,
    "Property": property_handler,
    "RuntimeProvider": provider_handler,
    "VirtualMachine": concrete_vm_handler,  # Warning: the class here might change to some concrete VM class
    "VMImage": vm_image_handler
}


def handle_obj(obj, model_root, level, intermediate_repr):
    if obj.eClass.name in class_handler:
        class_handler[obj.eClass.name](obj, model_root, level, intermediate_repr)
    else:
        logging.warning(f'Class {obj.eClass.name} has no handler')


# -------------------------------------------------------------------------
# Parse parameters
# -------------------------------------------------------------------------
skip_next = False
doml_directory = "icgparser/doml"


# -------------------------------------------------------------------------
# Load each part of the DOML metamodel and register them
# -------------------------------------------------------------------------
def load_metamodel(load_split_model):
    global_registry[Ecore.nsURI] = Ecore  # Load the Ecore metamodel first
    rset = ResourceSet()
    if load_split_model:
        mm_parts = ["doml", "commons", "application", "infrastructure", "concrete", "optimization"]
        for mm_filename in mm_parts:
            resource = rset.get_resource(URI(f"{doml_directory}/{mm_filename}.ecore"))
            mm_root = resource.contents[0]  # Get the root of the MetaModel (EPackage)
            rset.metamodel_registry[mm_root.nsURI] = mm_root
    else:
        resource = rset.get_resource(URI(f"{doml_directory}/doml.ecore"))
        mm_root = resource.contents[0]  # Get the root of the MetaModel (EPackage)
        rset.metamodel_registry[mm_root.nsURI] = mm_root
        for subp in mm_root.eSubpackages:
            rset.metamodel_registry[subp.nsURI] = subp
    return rset


# -------------------------------------------------------------------------
# Finally load the model and print it out
# -------------------------------------------------------------------------

def parse_model(model):
    load_split_model = None
    rset = load_metamodel(load_split_model)
    doml_model_resource = rset.get_resource(URI(model))
    doml_model = doml_model_resource.contents[0]
    single = "single-file (doml.ecore)"
    split = "split"
    dash = "-"
    logging.info(f'{comment}{80 * dash}')
    logging.info(f'{comment} Using {split if load_split_model else single} metamodel from directory {doml_directory}')
    print(f'{comment} Model loaded from file {model}:')
    print(f'{comment}{80 * dash}')
    print_contents_recursive(doml_model)
    print(f'{comment}{80 * dash}{newline}{comment} Generated Intermediate Representation follows:{newline}{comment}')
    intermediate_repr_file_path = "input_file_generated/ir.json"
    create_file("input_file_generated/ir.json")
    handle_obj(doml_model, doml_model, 0, intermediate_repr_file_path)

def create_file(file_name):
    f = open(file_name, "w")
    f.write("")
    f.close()

def append_in_file(file_name, data):
    f = open(file_name, "a")
    f.write(data)
    f.write("\n")
    f.close()
