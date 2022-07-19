import logging
from distutils.dir_util import copy_tree

from plugin import TemplateUtils, PluginUtility


def store_monitoring_agents_folder(output_path):
    logging.info(f"Adding monitoring agents folder in {output_path}")
    copy_tree("templates/terraform/open_stack/agents_playbook", output_path)


def create_files(parameters, output_path):
    language = "terraform"
    provider = parameters["provider"]

    config_file = PluginUtility.createExecutionFileInstructions(language, provider, parameters)

    resources = parameters.keys()
    terraform_main_file = create_init_file(language, provider)
    terraform_out_file = ""
    for resource_name in resources:
        logging.info("Creating output and main terraform template for resource '%s'", resource_name)

        template_for_main_path = TemplateUtils.find_template_path(language, provider, resource_name)
        template_for_output_path = TemplateUtils.find_template_path(language, provider,
                                                                    get_resource_out_path(resource_name))
        if template_for_main_path:
            for resource_params in parameters[resource_name]:
                template = TemplateUtils.read_template(template_for_main_path)
                # resource = parameters[resource_name]
                template_filled = TemplateUtils.edit_template(template, resource_params)
                terraform_main_file = terraform_main_file + template_filled + "\n"

        if template_for_output_path:
            for resource_params in parameters[resource_name]:
                template_out = TemplateUtils.read_template(template_for_output_path)
                # resource = parameters[resource_name]
                template_out_filled = TemplateUtils.edit_template(template_out, resource_params)
                terraform_out_file = terraform_out_file + template_out_filled + "\n"
    main_file_stored_path = output_path + "/main.tf"
    TemplateUtils.write_template(terraform_main_file, main_file_stored_path)
    output_file_stored_path = output_path + "/output.tf"
    TemplateUtils.write_template(terraform_out_file, output_file_stored_path)
    config_file_stored_path = output_path + "/config.yaml"
    TemplateUtils.write_template(config_file, config_file_stored_path)
    store_monitoring_agents_folder(output_path)
    logging.info("Terraform main file available at: {}".format(main_file_stored_path))
    logging.info(f"Terraform output file available at {output_file_stored_path}")


def create_init_file(language, provider):
    logging.info("Creating init %s file for provider %s", language, provider)
    template_path = TemplateUtils.find_template_path(language, provider, "init")
    template = TemplateUtils.read_template(template_path)
    return template.render() + "\n"

## TODO spostare i template di out in una cartella?? es. cartella vms&vms_out? altrimenti come prendo nome di out?
## non è nel doml
def get_resource_out_path(resource_name):
    return resource_name + "_out"
