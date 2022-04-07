import json
import logging
import tarfile
import uuid
from icgparser import ModelParser
from plugin import AnsiblePlugin, TerraformPlugin


class CompressFolder:
    def __init__(self, file_path, filename):
        self.file_path = file_path,
        self.filename = filename

def create_infrastructure_files(intermediate_representation: dict):
    template_generated_folder = intermediate_representation["output_path"]
    choose_plugin(intermediate_representation, template_generated_folder)
    logging.info("iac files available at %s", template_generated_folder)
    return template_generated_folder


def choose_plugin(parameters, template_generated_folder):
    # os.system('rm -f /opt/output_files_generated/*')
    logging.info("Choosing plugin")
    for step in parameters["steps"]:
        if step["programming_language"] == "ansible":
            logging.info("Ansible Plugin chosen")
            input_data = step["data"]
            AnsiblePlugin.create_files(input_data, template_generated_folder)
        elif step["programming_language"] == "terraform":
            logging.info("Terraform Plugin chosen")
            input_data = step["data"]
            TerraformPlugin.create_files(input_data, template_generated_folder)


def create_temp_file_for_model(model, output_folder):
    logging.info(f"Writing model file in temp folder at {output_folder} for parsing")


def save_file(data, file_path):
    logging.info(f"Saving data at: {file_path}")
    file = open(file_path, "w")
    if isinstance(data, dict):
        data = json.dumps(data, indent=2, sort_keys=True)
    print(data)
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
    temp_model_file_path = "icgparser/doml/nginx-openstack.domlx"
    save_file(model_xml, temp_model_file_path)
    logging.info(f"Successfully saved model in temp file at {temp_model_file_path}")
    return temp_model_file_path

def create_intermediate_representation(model_path, is_multiecore_metamodel, metamodel_directory):
    logging.info("Calling ICG Parser for creating intermediate representation")
    intermediate_representation = ModelParser.parse_model(model_path=model_path,
                                                          is_multiecore_metamodel=is_multiecore_metamodel,
                                                          metamodel_directory=metamodel_directory)
    intermediate_representation = reorganize_info(intermediate_representation)
    logging.info("Successfully created intermediate representation")
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
    logging.info(f"######################### {compress_folder_info.file_path}") ## TODO fix, is tuple instead of string
    return compress_folder_info

def create_iac_from_intermediate_representation(intermediate_representation):
    logging.info("Creating iac files")
    template_generated_folder = create_infrastructure_files(intermediate_representation)
    return template_generated_folder

def create_iac_from_doml(model, is_multiecore_metamodel, metamodel_directory):
    logging.info("Creating iac files: parse and plugins will be called")
    model_path = create_temp_model_file(model_xml=model)
    intermediate_representation = create_intermediate_representation(model_path, is_multiecore_metamodel,
                                                                     metamodel_directory)
    template_generated_folder = create_iac_from_intermediate_representation(intermediate_representation)
    compress_folder_info = compress_iac_folder(template_generated_folder)
    return compress_folder_info

def create_iac_from_doml_path(model_path, is_multiecore_metamodel, metamodel_directory):
    intermediate_representation = create_intermediate_representation(model_path, is_multiecore_metamodel,
                                                                     metamodel_directory)
    template_generated_folder = create_iac_from_intermediate_representation(intermediate_representation)
    compress_folder_info = compress_iac_folder(template_generated_folder)
    return compress_folder_info
