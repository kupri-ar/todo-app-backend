from flask import Blueprint, request
from flask_jwt_extended import jwt_required

import crud

todo_items_bp = Blueprint('todo_items_bp', __name__)


@todo_items_bp.route('/', methods=['POST'])
def create_item():
    """Add new Item"""

    body = request.get_json()
    result = crud.create_todo_item(body)

    return result, 201


@todo_items_bp.route('/', methods=['GET'])
def get_items():
    """Get Items with pagination"""

    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 3)
    order_by = request.args.get('order_by', None)
    desc_order = request.args.get('desc_order', False)

    return crud.get_todo_items_with_paginate(page, per_page, order_by, desc_order)


@todo_items_bp.route('/', methods=['PUT'])
@jwt_required()
def update_todo_item():
    """Update Item"""

    body = request.get_json()
    result = crud.update_todo_item(body)

    return result, 200
