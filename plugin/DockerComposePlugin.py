import logging

from icgparser.ModelResourcesUtilities import get_ir_key_name, ModelResources
from plugin import TemplateUtils


def search_containers_to_be_created(container_image_resource):
    logging.info("Searching for containers")
    containers = []
    if container_image_resource["generatedContainers"]:
        containers = list(container_image_resource["generatedContainers"])
    logging.info(f"Found containers {containers}")
    return containers

def create_template_file(resource_name, parameters, extra_parameters, language):
    inventory_template_path = TemplateUtils.find_template_path(iac_language=False, key=language,
                                                                 resource_name=resource_name)
    template = TemplateUtils.read_template(inventory_template_path)
    template_filled = TemplateUtils.edit_template(template, parameters)
    return template_filled

def create_metadata_files(resource_params, output_path, language):
    inventory_template_stored_path = output_path + "inventory.j2"
    ssh_template_stored_path = output_path + "ssh_key.j2"
    ansible_template_file_path = output_path + "main.yml"
    config_template_file_path = output_path + "config.yaml"

    inventory_template_filled = create_template_file("inventory", resource_params, None, language)
    config_template_filled = create_template_file("config", resource_params, None, language)
    ssh_key_template_filled = create_template_file("ssh_key", resource_params, None, language)
    ansible_template_filled = create_template_file("main", resource_params, None, language)

    TemplateUtils.write_template(inventory_template_filled, inventory_template_stored_path)
    TemplateUtils.write_template(ansible_template_filled, ansible_template_file_path)
    TemplateUtils.write_template(config_template_filled, config_template_file_path)
    TemplateUtils.write_template(ssh_key_template_filled, ssh_template_stored_path)


def create_files(step_data, output_path):
    logging.info(f"Using Docker Compose Plugin for step {step_data}")
    language = step_data[get_ir_key_name(ModelResources.LANGUAGE)]
    parameters = step_data["data"]
    for resource_name, resources in parameters.items():
        logging.info(f"Found resource type {resource_name}")
        for resource_params in resources:
            containers = search_containers_to_be_created(resource_params)
            for container in containers:
                logging.info(f"Creating templates for resource {resource_params}")
                container_name = container["name"]
                output_base_folder_path = output_path + f"{container_name}/"
                template_stored_path = output_base_folder_path + "docker-compose.yml"
                template_path = TemplateUtils.find_template_path(iac_language=False, key=language,
                                                                 resource_name=resource_name)
                template = TemplateUtils.read_template(template_path)
                template_filled = TemplateUtils.edit_template(template, container, resource_params)
                TemplateUtils.write_template(template_filled, template_stored_path)

                create_metadata_files(container, output_base_folder_path, language)
                logging.info(f"Docker compose files created for {container_name}")
    logging.info(f"Docker compose files created")
