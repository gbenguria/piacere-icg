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
#		© Copyright 2022 Hewlett Packard Enterprise Development LP
# -------------------------------------------------------------------------
import logging
from icgparser import DomlParserUtilities
from icgparser.DomlParserUtilities import get_reference_list_if_exists

OUTPUT_BASE_DIR_PATH = "output_files_generated/"
doml_layers = {
    "active_infrastructure_layer": "activeInfrastructure",
}

def to_camel_case(content):
    return content[0].lower() + content[1:]


def include_missing_objects_from_infrastructure_layer(to_step):
    for obj_name in DomlParserUtilities.retrieve_missing_parsed_resources():
        obj = DomlParserUtilities.retrieve_missing_parsed_resources()[obj_name]
        infra_object_representation = {}
        infra_object_representation = DomlParserUtilities.save_attributes(obj["resource"], infra_object_representation)
        infra_object_representation = DomlParserUtilities.save_inner_components(obj["resource"],
                                                                                infra_object_representation)
        ## TODO fix attenzione che sovrascrive
        ir_key_name = to_camel_case(obj["reference"].eType.name)
        to_step["data"][ir_key_name] = [infra_object_representation]
        return to_step


def include_infra_object_from_concrete_layer(provider, infra_object_step):
    logging.info(f'Adding objects from concrete layer for provider {provider.name}')
    for ref in provider.eClass.eReferences:
        provider_object_list = get_reference_list_if_exists(provider, ref)
        if provider_object_list:
            logging.info(
                f'Found list of object {len(provider_object_list)} "{provider_object_list}" in "{provider.name}"')
            object_list_representation = []
            for object in provider_object_list:
                object_representation = {}
                object_representation = DomlParserUtilities.save_annotations(object, object_representation)
                object_representation = DomlParserUtilities.save_attributes(object, object_representation)
                object_representation = DomlParserUtilities.add_infrastructure_information(object.maps,
                                                                                           object_representation)
                object_list_representation.append(object_representation)
            infra_object_step["data"][ref.name] = object_list_representation
    return infra_object_step


def parse_infrastructural_objects(doml_model):
    infra_object_step = {"programming_language": "terraform"}  ## TODO refactoring: generalize
    concretization_layer = doml_model.eGet(doml_layers["active_infrastructure_layer"])
    providers = concretization_layer.providers
    for provider in providers:
        logging.info(f'Searching objects to be generates for provider "{provider.name}"')
        infra_object_step["data"] = {}  ## TODO refactoring, fix (maybe list?): generalize
        infra_object_step["data"]["provider"] = provider.name  ## TODO refactoring: generalize
        infra_object_step = include_infra_object_from_concrete_layer(provider, infra_object_step)
        infra_object_step = include_missing_objects_from_infrastructure_layer(infra_object_step)
    return infra_object_step


def create_intermediate_representation(model_loaded):
    model_name = model_loaded.name
    output_path = OUTPUT_BASE_DIR_PATH + model_name + "/"
    intermediate_representation_steps = []
    infra_object_step = parse_infrastructural_objects(model_loaded)
    intermediate_representation_steps.append(infra_object_step)
    intermediate_representation = {
        "output_path": output_path,
        "steps": intermediate_representation_steps
    }
    return intermediate_representation


def parse_model(model_path, is_multiecore_metamodel, metamodel_directory):
    rset = DomlParserUtilities.load_metamodel(metamodel_directory=metamodel_directory,
                                              is_multiecore=is_multiecore_metamodel)
    doml_model = DomlParserUtilities.load_model(model_path, rset)
    create_intermediate_representation(doml_model)
