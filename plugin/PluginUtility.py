from plugin import TemplateUtils


def createExecutionFileInstructions(iac_language, key, data):
    template_for_config_path = TemplateUtils.find_template_path(iac_language, key, "config")
    template_for_config = TemplateUtils.read_template(template_for_config_path)
    template_for_config_path_edited = TemplateUtils.edit_template(template_for_config, data)
    return template_for_config_path_edited
