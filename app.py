from flasgger import Swagger
from flask import Flask

from src.api import routes
from src.api.routes import init_api_routes
from src.config import db
import src.api.routes

app = Flask(__name__)
  # Create Swagger object for API documentation
db.Base.metadata.create_all(db.engine)
init_api_routes(app)
swagger = routes.swagger(app)
if __name__ == '__main__':
    app.run(port=5000)
