import logging
import tarfile

from fastapi import APIRouter, Body
from fastapi.responses import FileResponse

from plugin import TerraformPlugin
from plugin import AnsiblePlugin


api_router = APIRouter()

@api_router.post("/infrastructure/files")
def create_infrastructure_files(intermediate_representation: dict = Body(...)):
    logging.info("Received intermediate representation create_infrastructure_files request")
    choose_plugin(intermediate_representation)
    logging.info("Creating compress folder with iac files")
    output_template_folder = intermediate_representation["output_path"]
    compress_file_name = "outputIaC.tar.gz"
    compress_file_path = compress_file(output_template_folder, compress_file_name)
    return FileResponse(compress_file_path, media_type='application/octet-stream', filename=compress_file_name)

def choose_plugin(parameters):
    # os.system('rm -f /opt/output_files_generated/*')
    for step in parameters["steps"]:
        if step["programming_language"] == "ansible":
            input_data = step["data"]
            AnsiblePlugin.create_files(input_data, parameters["output_path"])
        elif step["programming_language"] == "terraform":
            input_data = step["data"]
            TerraformPlugin.create_files(input_data, parameters["output_path"])

def compress_file(source_folder, dest_file_name):
    # prefix_path = "/opt/"
    prefix_path = ""
    logging.info("Compressing folder %s into destination %s", prefix_path + source_folder,
                 prefix_path + dest_file_name)
    with tarfile.open(prefix_path + dest_file_name, "w:gz") as tar:
        tar.add(source_folder, arcname='.')
    return prefix_path + dest_file_name
