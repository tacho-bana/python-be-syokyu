from sqlalchemy.orm import Session
from ..models.list_model import ListModel
from ..models.item_model import ItemModel
from ..schemas.item_schema import UpdateTodoItem, NewTodoItem, ResponseTodoItem
from app.const import TodoItemStatusCode
from fastapi import HTTPException, status

def get_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    db_item = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    return db_item

def create_todo_item(db: Session, todo_list_id: int, new_todo_item: NewTodoItem):
    db_item = db.query(ListModel).filter(ListModel.id==todo_list_id).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
        
    db_item = ItemModel(
        todo_list_id=todo_list_id,
        title=new_todo_item.title,
        description=new_todo_item.description,
        due_at=new_todo_item.due_at,
        status_code=TodoItemStatusCode.NOT_COMPLETED.value
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_item(db: Session, todo_list_id: int, todo_item_id: int, update_todo_item: UpdateTodoItem):
    db_item = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="data not found")
    db_item.title = update_todo_item.title
    db_item.description = update_todo_item.description
    db_item.due_at = update_todo_item.due_at

    if update_todo_item.complete is True:
        db_item.status_code = TodoItemStatusCode.COMPLETED.value
    elif update_todo_item.complete is False:
        db_item.status_code = TodoItemStatusCode.NOT_COMPLETED.value

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_todo_item(db: Session, todo_list_id: int, todo_item_id: int):
    db_item = db.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="data not found")
    db.delete(db_item)
    db.commit()
    return {"OK"}

def get_todo_items(db:Session, page: int, per_page: int):
    return db.query(ItemModel).offset((page - 1) * per_page).limit(per_page).all()