import logging
import json
import tarfile
import uuid

from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from controller.PluginOrchestrator import create_infrastructure_files
from icgparser import ModelParser

api_router = APIRouter()

base_compress_file_name = "iac_files_"


@api_router.post("/infrastructure/files")
def create_iac_from_intermediate_representation(intermediate_representation: dict = Body(...)):
    logging.info("Received intermediate representation create_iac_from_intermediate_representation request")
    template_generated_folder = create_infrastructure_files(intermediate_representation)
    compress_file_name = random_file_name_generation(base_compress_file_name)
    compress_file_path = compress_file(template_generated_folder, compress_file_name)
    return FileResponse(compress_file_path, media_type='application/octet-stream', filename=compress_file_name)


@api_router.post("/iac/files")
def create_iac_from_doml(data: str = Body(..., media_type="application/xml")):
    logging.info("Received create_iac_from_doml request")
    temp_model_file_path = "icgparser/doml/nginx-openstack.domlx"
    logging.info("Writing model file in temp folder '%s' for parsing", temp_model_file_path)
    f = open(temp_model_file_path, "w")
    f.write(data)
    f.close()
    intermediate_representation = ModelParser.parse_model(model_path=temp_model_file_path)
    intermediate_representation = reorganize_info(intermediate_representation)
    save(intermediate_representation, "input_file_generated/ir.json")
    template_generated_folder = create_infrastructure_files(intermediate_representation)
    compress_file_name = random_file_name_generation(base_compress_file_name)
    compress_file_folder = compress_file(template_generated_folder, compress_file_name)
    return FileResponse(compress_file_folder,
                        media_type='application/octet-stream',
                        filename=compress_file_name)


def random_file_name_generation(base_name):
    return base_name + str(uuid.uuid4().hex) + ".tar.gz"


def compress_file(source_folder, dest_file_name):
    # prefix_path = "/opt/"
    prefix_path = ""
    logging.info("Compressing folder %s into destination %s", prefix_path + source_folder,
                 prefix_path + dest_file_name)
    with tarfile.open(prefix_path + dest_file_name, "w:gz") as tar:
        tar.add(source_folder, arcname='.')
    return prefix_path + dest_file_name


def save(data, file_path):
    file = open(file_path, "w")
    if isinstance(data, dict):
        data = json.dumps(data, indent=2, sort_keys=True)
    print(data)
    file.write(data)
    file.close()

def reorganize_info(intermediate_repr):
    computing_group_list = []
    groups = intermediate_repr["steps"][0]["data"]["computingGroup"][0]
    for key in groups:
        if not key == "name":
            computing_group_list.append(groups[key])
    intermediate_repr["steps"][0]["data"]["computingGroup"] = computing_group_list
    return intermediate_repr
