import ansibleUtils 

class InputData:
    app_type: str
    code_path: str
    template_type: str
    template_path: str
    template_data: map

    def __init__(self, app_type, code_path, template_type, template_path, template_data):
        self.app_type = app_type
        self.code_path = code_path
        self.template_type = template_type
        self.template_path = template_path
        self.template_data = template_data

class TemplateInfo:
    path: str
    type: str
    data: map

    def __init__(self, input_data: InputData):
        self.path = input_data.template_path
        self.type = input_data.template_type
        self.data = input_data.template_data

class AnsibleModule:
    
    def get_template(self, template_complete_path):
        template = open(template_complete_path, "r")
        return template.readlines()

    def edit_template(self, template_type, template_list, template_data, kind):
        if template_type == "postgres":
            new_file = ansibleUtils.databases_postgres(template_list, template_data, kind)
        if template_type == "mysql":
            new_file = ansibleUtils.databases_mysql(template_list, template_data, kind)
        if template_type == "wordpress":
            new_file = ansibleUtils.service_wordpress(template_list, template_data, kind)  
        return new_file

    def write_file(self, edited_content, code_path: str):
        file = open(code_path, "w+")
        file.write(edited_content)
        file.close()

class AnsibleICG:

    def generate_code(self, input_data: InputData):

        templateFile = TemplateInfo(input_data)
        ansibleModule = AnsibleModule()

        kinds = ["play", "vars"]
        for kind in kinds:
            template_complete_path = templateFile.path + templateFile.type + "-" + kind + ".tpl"
            template_list = ansibleModule.get_template(template_complete_path)
            edited_content = ansibleModule.edit_template(templateFile.type, template_list, templateFile.data, kind)
            code_path = input_data.code_path + templateFile.type + "-" + kind + ".yml"
            ansibleModule.write_file(edited_content, code_path)
