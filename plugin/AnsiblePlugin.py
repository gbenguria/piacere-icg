import logging
from plugin import TemplateUtils
from plugin.PluginException import PluginResourceNotFoundError


def clean_operating_system_name(operating_system):
    if "ubuntu" in operating_system:
        return "ubuntu"
    else:
        raise PluginResourceNotFoundError(plugin_name="AnsiblePlugin", resource_name="operating system")


def find_operating_system(parameters):
    try:
        operating_system = parameters.get("node").get("os")
        operating_system_name = clean_operating_system_name(operating_system)
        return operating_system_name
    except Exception:
        raise PluginResourceNotFoundError(plugin_name="AnsiblePlugin", resource_name="operating system")


def create_inventory_file(parameters, language, operating_system, template_name):
    inventory_template_path = TemplateUtils.find_template_path(language, operating_system, template_name)
    template = TemplateUtils.read_template(inventory_template_path)
    template_filled = TemplateUtils.edit_template(template, parameters)
    return template_filled


def create_files(parameters, output_path):
    language = "ansible"
    for resource_name, resource in parameters.items():
        logging.info("Creating template for resource '%s'", resource_name)
        operating_system = find_operating_system(resource)
        ansible_template_path = TemplateUtils.find_template_path(language, operating_system, resource_name)
        if ansible_template_path:
            # for resource_params in parameters[resource_name]:
            resource_params = parameters[resource_name]

            ansible_output_file_path = output_path + "/".join([language, resource_name]) + ".yaml"
            inventory_output_file_path = output_path + "/".join([language, "inventory"]) + ".j2"
            config_output_file_path = output_path + "/".join([language, "config"]) + ".yaml"

            template = TemplateUtils.read_template(ansible_template_path)
            template_filled = TemplateUtils.edit_template(template, resource_params)

            inventory_template_filled = create_inventory_file(resource_params, language, operating_system, "inventory")
            config_template_filled = create_inventory_file(resource_params, language, operating_system, "config")

            TemplateUtils.write_template(inventory_template_filled, inventory_output_file_path)
            TemplateUtils.write_template(template_filled, ansible_output_file_path)
            TemplateUtils.write_template(config_template_filled, config_output_file_path)

    logging.info("File available at: {}".format(output_path))
