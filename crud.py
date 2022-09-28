from sqlalchemy import desc

from exceptions import MissingParam, NotFoundException
from models import TodoItem, db
from schemas import TodoItemSchema


def create_todo_item(payload):
    new_todo_item = TodoItemSchema().load(payload, session=db.session)
    db.session.add(new_todo_item)
    db.session.commit()

    return TodoItemSchema().dump(new_todo_item)


def get_todo_items_with_paginate(page, per_page, order_by, desc_order):
    q = db.session.query(TodoItem)

    if order_by == 'name':
        if desc_order:
            q = q.order_by(desc(TodoItem.name))
        else:
            q = q.order_by(TodoItem.name)
    elif order_by == 'email':
        if desc_order:
            q = q.order_by(desc(TodoItem.email))
        else:
            q = q.order_by(TodoItem.email)
    elif order_by == 'is_checked':
        if desc_order:
            q = q.order_by(desc(TodoItem.is_checked))
        else:
            q = q.order_by(TodoItem.is_checked)
    else:
        q = q.order_by(desc(TodoItem.id))

    result = q.paginate(page=int(page), per_page=int(per_page))

    response_data = TodoItemSchema(many=True).dump(result.items)
    response_headers = {
        "X-Pagination-Current-Page": page,
        "X-Pagination-Per-Page": per_page,
        "X-Pagination-Total-Count": result.total,
        'X-Pagination-Page-Count': result.pages,
        'Access-Control-Expose-Headers': 'X-Pagination-Current-Page, X-Pagination-Per-Page, '
                                         'X-Pagination-Total-Count, X-Pagination-Page-Count'
    }

    return response_data, response_headers


def update_todo_item(payload):
    if 'id' not in payload.keys():
        raise MissingParam(param='id')

    todo_item_id = payload['id']

    existing = db.session.query(TodoItem).where(TodoItem.id == todo_item_id).first()

    old_content = existing.content

    if not existing:
        raise NotFoundException()

    todo_item = TodoItemSchema().load(payload, session=db.session, partial=True, instance=existing)

    if old_content != todo_item.content:
        todo_item.edited_by_admin = True

    db.session.commit()

    return TodoItemSchema().dump(todo_item)
