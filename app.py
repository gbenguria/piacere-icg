from ICG import *
from flask import Flask, request, send_file
import tarfile
import os.path

def create_app(test_config=None):
    app = Flask(__name__)

    app.config["CLIENT_IMAGES"] = "/opt"

    @app.post("/")
    def ICG():
        if request.is_json:
            parameters = request.get_json()
            ICG_call(parameters)
            with tarfile.open("/opt/outputIaC.tar.gz", "w:gz") as tar:
                tar.add("/opt/Output-code", arcname=os.path.basename("/opt/Output-code"))
            file_name = "/opt/outputIaC.tar.gz"
            return send_file(file_name, attachment_filename='outputIaC.tar.gz'), 201
        return {"error": "Request must be JSON"}, 415
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)