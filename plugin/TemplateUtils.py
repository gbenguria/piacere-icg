import configparser
import logging
import os

import jinja2
from jinja2 import Template


@jinja2.pass_context
def get_context(c):
    return c

def find_template_path(iac_language, key, resource_name):
    try:
        properties_reader = configparser.ConfigParser()
        properties_reader.read("template-location.properties")
        template_path = properties_reader.get(iac_language + "." + key, resource_name)
        logging.info("Chosen template at: '%s'", template_path)
        return template_path
    except configparser.NoOptionError as error:
        logging.warning("%s. Please check properties file", error)
        pass


def edit_template(template, parameters: dict):
    logging.info("Starting editing template")
    template.globals['context'] = get_context
    template.globals['callable'] = callable
    render = template.render(parameters)
    template_with_custom_params = ""+render+"\n"
    return template_with_custom_params


def read_template(template_path):
    logging.info("Reading template at: '%s'", template_path)
    try:
        template = Template(open(template_path, "r").read())
        return template
    except jinja2.exceptions.TemplateSyntaxError as exc:
        # TODO or error?
        logging.warning('Syntax error on template %s, %s', template_path, exc)
        pass


def write_template(template, output_path_file):
    os.makedirs(os.path.dirname(output_path_file), exist_ok=True)
    file = open(output_path_file, "w+")
    file.write(template)
    logging.info("Writing file at: '%s'", output_path_file)
    file.close()
