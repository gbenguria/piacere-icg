# Copyright 2022 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------

import logging

from pyecore.ecore import EOrderedSet, EEnumLiteral
from pyecore.resources import ResourceSet, URI, global_registry
import pyecore.ecore as Ecore  # This gets a reference to the Ecore metamodel implementation

TO_BE_PARSED_RESOURCES = {}
METAMODEL_SECTIONS = ["doml", "commons", "application", "infrastructure", "concrete", "optimization"]
METAMODEL_DIRECTORY = "icgparser/doml"


def extract_value_from(ecore_object_value):
    if isinstance(ecore_object_value, EOrderedSet):
        value = list(ecore_object_value)
    elif isinstance(ecore_object_value, EEnumLiteral):
        value = ecore_object_value.name
    else:
        value = ecore_object_value
    return value


def get_reference_list_if_exists(from_object, reference):
    reference_from_object = from_object.eGet(reference.name)
    if reference_from_object and isinstance(reference_from_object, EOrderedSet) and len(reference_from_object) > 0:
        return reference_from_object
    else:
        return None


def save_annotations(from_object, to_object):
    print(f'Saving annotation from {from_object.name}')
    if not to_object:
        to_object = {}
    for annotation in from_object.annotations:
        to_object[annotation.key] = annotation.value
    return to_object


def save_attributes(from_object, to_object, skip_component_name=False):
    print(f'Saving attributes from {from_object.name}')
    if not to_object:
        to_object = {}
    for attribute in from_object.eClass.eAllAttributes():
        if from_object.eGet(attribute.name):
            key = attribute.name
            if skip_component_name and attribute.name == "name":
                key = "infra_element_name"
                print(f'Renaming attributes {attribute.name} from {from_object.name} into {key}')
                ## TODO manage this (pay attention: error with sg!!)
            # elif attribute.name == "name":
            #     key = "concrete_element_name"
            #     print(f'Renaming attributes {attribute.name} from {from_object.name} into {key}')
            value = from_object.eGet(attribute.name)
            if isinstance(value, EOrderedSet):
                value = list(value)
            if isinstance(value, EEnumLiteral):
                value = value.name
            to_object[key] = value
    return to_object


def update_missing_parsed_resources(resource, reference, is_to_be_parsed):
    resource_name = resource.name
    if is_to_be_parsed and not (resource_name in TO_BE_PARSED_RESOURCES):
        print(f'Adding {resource_name} as missing parsed resource')
        TO_BE_PARSED_RESOURCES[resource_name] = {"resource": resource,
                                                 "reference": reference}  ## TODO introdurre interfaccia
    elif not is_to_be_parsed and (resource_name in TO_BE_PARSED_RESOURCES):
        print(f'Removing {resource_name} to the missing parsed resource')
        del TO_BE_PARSED_RESOURCES[resource_name]
    else:
        print(f'update_missing_parsed_resources: skipping {resource_name}')


def save_references_info(from_object, to_object):  ## TODO refactoring
    refs = from_object.eClass.eAllReferences()
    for ref in refs:
        if get_reference_list_if_exists(from_object, ref):
            logging.info(f'{ref.name} is a list, skipping it')
        ## TODO trattare la lista
        elif from_object.eGet(ref.name):
            logging.info(f'Adding reference "{ref.name}" location')
            reference_object = from_object.eGet(ref.name)
            to_object[ref.name] = reference_object.name
            update_missing_parsed_resources(reference_object, reference=ref, is_to_be_parsed=True)
    return to_object

def get_references(from_object):
    refs = from_object.eClass.eAllReferences()
    return list(refs)

def save_inner_components(from_object, to_object):
    inner_components = from_object.eAllContents()
    for obj in inner_components:
        if not isinstance(obj, EOrderedSet):  # TODO espandere info
            if obj.name is not None:
                object_name = obj.name
            else:
                logging.warning(f'Object name not available, changing it using class name: {obj.eClass.name}')
                object_name = obj.eClass.name
            print(f'Saving information from object {object_name}')
            inner_component = save_attributes(obj, {})
            save_references_info(obj, inner_component)
            to_object[object_name] = inner_component
    return to_object


def add_infrastructure_information(infrastructure_element, to_object):
    print(f'Saving infrastructure information from {infrastructure_element.name}')
    update_missing_parsed_resources(infrastructure_element, is_to_be_parsed=False, reference=None)
    save_attributes(infrastructure_element, to_object, skip_component_name=True)
    save_references_info(infrastructure_element, to_object)
    save_inner_components(infrastructure_element, to_object)
    return to_object


def retrieve_missing_parsed_resources():
    return TO_BE_PARSED_RESOURCES


def load_metamodel(metamodel_directory=METAMODEL_DIRECTORY, is_multiecore=False):
    global_registry[Ecore.nsURI] = Ecore
    rset = ResourceSet()
    if is_multiecore:
        logging.info(f"Loading multiecore metamodel from {metamodel_directory}")
        for mm_filename in METAMODEL_SECTIONS:
            resource = rset.get_resource(URI(f"{metamodel_directory}/{mm_filename}.ecore"))
            mm_root = resource.contents[0]  # Get the root of the MetaModel (EPackage)
            rset.metamodel_registry[mm_root.nsURI] = mm_root
    else:
        logging.info(f"Loading ecore metamodel from {metamodel_directory}/doml.ecore")
        resource = rset.get_resource(URI(f"{metamodel_directory}/doml.ecore"))
        mm_root = resource.contents[0]  # Get the root of the MetaModel (EPackage)
        rset.metamodel_registry[mm_root.nsURI] = mm_root
        for subp in mm_root.eSubpackages:
            rset.metamodel_registry[subp.nsURI] = subp
    return rset


def load_model(model_path, rset):
    doml_model_resource = rset.get_resource(URI(model_path))
    return doml_model_resource.contents[0]
