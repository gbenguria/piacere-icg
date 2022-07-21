# Copyright 2022 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------

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
    compress_folder_info = Orchestrator.create_iac_from_doml(model=data, metamodel_directory="icgparser/doml/v1",
                                                             is_multiecore_metamodel=False)
    return FileResponse(path=compress_folder_info.file_path, media_type='application/octet-stream',
                        filename=compress_folder_info.filename)
