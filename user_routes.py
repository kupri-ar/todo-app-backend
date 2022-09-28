import redis
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt, get_jwt_identity

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "123":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)

    response_headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Access-Control-Expose-Headers': 'Authorization'
    }

    return jsonify(username=username), 200, response_headers


@user_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    return jsonify(msg="Access token revoked")


@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    user = get_jwt_identity()

    return jsonify(username=user), 200
