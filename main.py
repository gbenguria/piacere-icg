import logging
from fastapi import FastAPI
import api.InfrastructureTemplateController

fast_api = FastAPI()

fast_api.include_router(api.InfrastructureTemplateController.api_router)
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    logging.info("Starting ICG application")
