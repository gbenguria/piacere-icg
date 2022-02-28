import json
import logging
from fastapi import FastAPI

import api.InfrastructureTemplateController
from api import InfrastructureTemplateController

fast_api = FastAPI()

fast_api.include_router(api.InfrastructureTemplateController.api_router)
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    parameters_file = open("input_file_example/nginx/parameter.json")
    parameters_file = json.load(parameters_file)
    InfrastructureTemplateController.choose_plugin(parameters_file)
