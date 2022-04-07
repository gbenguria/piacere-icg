import logging
from fastapi import APIRouter, Body
from fastapi.responses import FileResponse
from controller import Orchestrator

api_router = APIRouter()

base_compress_file_name = "iac_files_"


@api_router.post("/infrastructure/files")
def create_iac_from_intermediate_representation(intermediate_representation: dict = Body(...)):
    logging.info("Received intermediate representation create_iac_from_intermediate_representation request")
    compress_folder_info = Orchestrator.create_iac_from_intermediate_representation(intermediate_representation)
    return FileResponse(compress_folder_info.file_path, media_type='application/octet-stream',
                        filename=compress_folder_info.filename)


@api_router.post("/iac/files")
def create_iac_from_doml(data: str = Body(..., media_type="application/xml")):
    logging.info("Received create_iac_from_doml request")
    compress_folder_info = Orchestrator.create_iac_from_doml(model=data, metamodel_directory="icgparser/doml",
                                                             is_multiecore_metamodel=False)
    logging.info(f"file_path: {compress_folder_info.file_path}, filename: {compress_folder_info.filename}")
    return FileResponse(path=compress_folder_info.filename, media_type='application/octet-stream', ## TODO change path into compress_folder_info.file_path
                        filename=compress_folder_info.filename)
