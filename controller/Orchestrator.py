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

import json
import logging
import os
import tarfile
import time
import uuid
import yaml

from icgparser import ModelParser, PiacereInternalToolsIntegrator, IntermediateRepresentationUtility
from icgparser.IntermediateRepresentationUtility import IntermediateRepresentationResources
from plugin import AnsiblePlugin, TerraformPlugin
from utility.FileParsingUtility import replace_none_with_empty_str


class CompressFolder:
    def __init__(self, file_path, filename):
        self.file_path = file_path
        self.filename = filename


def create_infrastructure_files(intermediate_representation: dict):
    template_generated_folder = intermediate_representation["output_path"]
    choose_plugin(intermediate_representation, template_generated_folder)
    logging.info("iac files available at %s", template_generated_folder)
    return template_generated_folder


def choose_plugin(parameters, template_generated_folder):
    # os.system('rm -f /opt/output_files_generated/*')
    logging.info("Choosing plugin")
    metadata_root_folder = {"iac": []}
    for step in parameters["steps"]:
        if step["programming_language"] == "ansible":
            logging.info("Ansible Plugin chosen")
            step_name = step[IntermediateRepresentationResources.STEP_NAME.value]
            metadata_root_folder["iac"].append(step_name)
            # input_data = step["data"]
            AnsiblePlugin.create_files(step, template_generated_folder)
        elif step["programming_language"] == "terraform":
            logging.info("Terraform Plugin chosen")
            metadata_root_folder["iac"].append("terraform")
            input_data = step["data"]
            iac_output_folder = template_generated_folder + "terraform"
            # plugin_metadata = {"input": ["openstack_username", "openstack_password", "openstack_auth_url"],
            plugin_metadata = {"input": [], "output": [], "engine": "terraform"}
            save_file(plugin_metadata, iac_output_folder + "/config.yaml", output_extensions="YAML")
            TerraformPlugin.create_files(input_data, iac_output_folder)
    save_file(metadata_root_folder, template_generated_folder + "/config.yaml", output_extensions="YAML")


def save_file(data, file_path, output_extensions="json"):
    logging.debug(f"Saving data: {data} at {file_path}")
    logging.info(f"Saving data at: {file_path}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file = open(file_path, "w")
    if isinstance(data, dict) and output_extensions == "YAML":
        logging.info("Converting python dict into yaml data")
        data = yaml.dump(data)
        data = "---\n" + data + "..."
    if isinstance(data, dict):
        data_without_none_value = replace_none_with_empty_str(data)
        logging.info("Converting python dict into json data")
        data = json.dumps(data_without_none_value, indent=2, sort_keys=True)
    file.write(data)
    file.close()


def reorganize_info(intermediate_repr):
    logging.info("Reorganizing intermediate representation")
    computing_group_list = []
    if "computingGroup" in intermediate_repr["steps"][0]["data"].keys():
        groups = intermediate_repr["steps"][0]["data"]["computingGroup"][0]
        for key in groups:
            if not key == "name":
                computing_group_list.append(groups[key])
        intermediate_repr["steps"][0]["data"]["computingGroup"] = computing_group_list
    return intermediate_repr


def random_file_name_generation(base_name):
    return base_name + str(uuid.uuid4().hex) + ".tar.gz"


def compress_file(source_folder, dest_file_name):
    # prefix_path = "/opt/"
    prefix_path = ""
    folder_path = prefix_path + dest_file_name + ""
    logging.info(f"Compressing folder {source_folder} into destination {folder_path}")
    with tarfile.open(folder_path, "w:gz") as tar:
        tar.add(source_folder, arcname='.')
    return folder_path


def create_temp_model_file(model_xml):
    logging.info("Saving model in temp file")
    temp_model_file_path = "icgparser/doml/v1/nginx-openstack_v1.domlx"
    save_file(model_xml, temp_model_file_path)
    logging.info(f"Successfully saved model in temp file at {temp_model_file_path}")
    return temp_model_file_path


def create_intermediate_representation(model_path, is_multiecore_metamodel, metamodel_directory):
    logging.info("Calling ICG Parser for creating intermediate representation")
    intermediate_representation = ModelParser.parse_model(model_path=model_path,
                                                          is_multiecore_metamodel=is_multiecore_metamodel,
                                                          metamodel_directory=metamodel_directory)
    # intermediate_representation = reorganize_info(intermediate_representation)
    logging.info(f"Successfully created intermediate representation {intermediate_representation}")
    logging.info("Calling ICG PiacereInternalToolsIntegrator to add info for PIACERE internal tools")
    intermediate_representation = PiacereInternalToolsIntegrator.add_internal_tool_information(intermediate_representation)
    logging.warning("Force adding sg information in network") ## TODO fix from doml
    intermediate_representation = IntermediateRepresentationUtility.force_add_resources_name(
        IntermediateRepresentationResources.NETWORKS,
        IntermediateRepresentationResources.SECURITY_GROUPS,
        intermediate_representation)
    intermediate_representation_path = "input_file_generated/ir.json"
    save_file(intermediate_representation, intermediate_representation_path)
    logging.info(f"Saved intermediate representation at {intermediate_representation_path}")
    return intermediate_representation


def compress_iac_folder(template_generated_folder):
    base_compress_file_name = "iac_files_"
    compress_file_name = random_file_name_generation(base_compress_file_name)
    compress_file_folder_path = compress_file(template_generated_folder, compress_file_name)
    logging.info(f"Successfully created iac files, available at {compress_file_folder_path}")
    compress_folder_info = CompressFolder(file_path=compress_file_folder_path, filename=compress_file_name)
    return compress_folder_info


def create_iac_from_intermediate_representation(intermediate_representation):
    logging.info("Creating iac files")
    template_generated_folder = create_infrastructure_files(intermediate_representation)
    return template_generated_folder


def create_iac_from_doml(model, is_multiecore_metamodel, metamodel_directory):
    """ Create IaC files storing the model domlx in a temp file and then parsing it

    :param model: the model xml file
    :type model: xml
    :param is_multiecore_metamodel: true if the metamodel is composed by multiecore files, false is it is a single ecore file
    :type is_multiecore_metamodel: bool
    :param metamodel_directory: the path of the metamodel directory
    :type metamodel_directory: str

    :returns: path to the zip folder containing the IaC files
    :type: str
    """
    logging.info("Creating iac files: parse and plugins will be called")
    model_path = create_temp_model_file(model_xml=model)
    ## TODO: same as def create_iac_from_doml_path a part from the model storage in xml
    intermediate_representation = create_intermediate_representation(model_path, is_multiecore_metamodel,
                                                                     metamodel_directory)
    template_generated_folder = create_iac_from_intermediate_representation(intermediate_representation)
    PiacereInternalToolsIntegrator.add_files_for_piacere_internal_tools(template_generated_folder)
    compress_folder_info = compress_iac_folder(template_generated_folder)
    return compress_folder_info


def create_iac_from_doml_path(model_path, is_multiecore_metamodel, metamodel_directory):
    """ Create IaC files from existing file model domlx

    :param model_path: the model xml file location
    :type model_path: str
    :param is_multiecore_metamodel: true if the metamodel is composed by multiecore files, false is it is a single ecore file
    :type is_multiecore_metamodel: bool
    :param metamodel_directory: the path of the metamodel directory
    :type metamodel_directory: str

    :returns: path to the zip folder containing the IaC files
    :type: str
    """
    intermediate_representation = create_intermediate_representation(model_path, is_multiecore_metamodel,
                                                                     metamodel_directory)
    template_generated_folder = create_iac_from_intermediate_representation(intermediate_representation)
    PiacereInternalToolsIntegrator.add_files_for_piacere_internal_tools(template_generated_folder)
    compress_folder_info = compress_iac_folder(template_generated_folder)
    return compress_folder_info
