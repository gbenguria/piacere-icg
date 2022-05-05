import logging
from plugin import TemplateUtils


def create_files(parameters, output_path):
    language = "terraform"
    provider = parameters["provider"]
    resources = parameters.keys()
    terraform_file = create_init_file(language, provider)
    for resource_name in resources:
        logging.info("Creating template for resource '%s'", resource_name)
        template_path = TemplateUtils.find_template_path(language, provider, resource_name)
        if template_path:
            for resource_params in parameters[resource_name]:
                template = TemplateUtils.read_template(template_path)
                # resource = parameters[resource_name]
                template_filled = TemplateUtils.edit_template(template, resource_params)
                terraform_file = terraform_file + template_filled + "\n"
    output_file_path = output_path + "/main.tf"
    TemplateUtils.write_template(terraform_file, output_file_path)
    logging.info("File available at: {}".format(output_path))


def create_init_file(language, provider):
    logging.info("Creating init %s file for provider %s", language, provider)
    template_path = TemplateUtils.find_template_path(language, provider, "init")
    template = TemplateUtils.read_template(template_path)
    return template.render() + "\n"
