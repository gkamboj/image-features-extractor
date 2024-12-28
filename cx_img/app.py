import os
import connexion

from cx_img.config.configuration import configs

swagger_path = os.path.join(os.path.dirname(__file__), 'api', 'swagger.yml')
app = connexion.App("__name__")
app.add_api(swagger_path)


@app.route("/")
def home():
    return "This is Flask application for image operations like object detections and attributes extraction!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=configs['app.port'])
