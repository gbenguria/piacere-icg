import logging

from plugin import AnsiblePlugin, TerraformPlugin


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
