from ansibleBuilder import *
from terraformBuilder import *
import json, sys, os

def ICG_call(parameters):
    os.system('rm -f /opt/Output-code/*')
    for step in parameters["steps"]:
        if step["programming_language"] == "ansible":
            input_data = InputData(app_type=step["type"], code_path=step["output_path"], template_type=step["info"]["name"], template_path=step["info"]["template_path"], template_data=step["data"])
            icg = AnsibleICG()
            icg.generate_code(input_data)
        elif step["programming_language"] == "terraform":
            input_data = step["data"]
            TerraformICG(input_data)

if __name__ == '__main__':
    arg_len = len(sys.argv)
    if arg_len > 1:
        file_name = sys.argv[1]
    else:
        print("Add parameters file name")
        sys.exit()

    input_file = open(file_name, "r")
    parameters = json.load(input_file)
    ICG_call(parameters)