from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.item_schema import UpdateTodoItem, NewTodoItem
from ..dependencies import get_db
from ..crud import item_crud

router = APIRouter(
    prefix="/lists",
    tags = ["Todo項目"]
)

@router.get("/{todo_list_id}/items/{todo_item_id}")
def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    db_item = item_crud.get_todo_item(db, todo_list_id, todo_item_id)
    return db_item

@router.post("/{todo_list_id}/items/")
def create_todo_item(todo_list_id: int, new_todo_item: NewTodoItem, db: Session = Depends(get_db)):
    db_item = item_crud.create_todo_item(db, todo_list_id, new_todo_item)
    return db_item

@router.put("/{todo_list_id}/items/{todo_item_id}")
def update_todo_item(todo_list_id: int, todo_item_id: int, update_todo_item:UpdateTodoItem, db: Session=Depends(get_db)):
    db_item = item_crud.get_todo_item(db, todo_list_id, todo_item_id)
    db_item = item_crud.update_todo_item(db, todo_list_id, todo_item_id, update_todo_item)
    return db_item

@router.delete("/{todo_list_id}/items/{todo_item_id}")
def delete_todo_item(todo_list_id: int, todo_item_id: int, db: Session=Depends(get_db)):
    db_item = item_crud.get_todo_item(db, todo_list_id, todo_item_id)
    db_item = item_crud.delete_todo_item(db, todo_list_id, todo_item_id)
    return db_item
