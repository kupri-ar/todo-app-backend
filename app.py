from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from user_routes import user_bp, jwt_redis_blocklist
from exceptions import NotFoundException, MissingParam
from todo_items_routes import todo_items_bp

from models import db, ma

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object('config.Config')
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

jwt = JWTManager(app)

app.register_blueprint(todo_items_bp, url_prefix='/todo')
app.register_blueprint(user_bp)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    rv = dict({'message': 'Validation Error', 'data': error.messages})
    return rv, 422


@app.errorhandler(NotFoundException)
@app.errorhandler(MissingParam)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True)
