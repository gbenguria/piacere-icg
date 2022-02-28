import logging
from plugin import TemplateUtils


def create_files(parameters, output_path):
    language = "ansible"
    operating_system = parameters["operating_system"]
    resources = parameters.keys()
    for resource_name in resources:
        logging.info("Creating template for resource '%s'", resource_name)
        template_path = TemplateUtils.find_template_path(language, operating_system, resource_name)
        if template_path:
            #for resource_params in parameters[resource_name]:
            resource_params = parameters[resource_name]
            output_file_path = output_path + "/".join([language, resource_name]) + ".play"
            template = TemplateUtils.read_template(template_path)
            template_filled = TemplateUtils.edit_template(template, resource_params)
            TemplateUtils.write_template(template_filled, output_file_path)
    logging.info("File available at: {}".format(output_path))

