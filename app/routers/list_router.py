from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.list_schema import UpdateTodoList, NewTodoList
from ..dependencies import get_db
from ..crud import list_crud

router = APIRouter(
    prefix="/lists",
    tags = ["Todoリスト"]
)

@router.get("/{todo_list_id}")
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = list_crud.get_todo_list(db, todo_list_id)
    return db_item

@router.post("/")
def create_todo_list(new_todo_list: NewTodoList, db: Session = Depends(get_db)):
    db_item = list_crud.create_todo_list(db, new_todo_list)
    return db_item

@router.put("/{todo_list_id}")
def update_todo_list(todo_list_id: int, update_todo_list: UpdateTodoList, db: Session = Depends(get_db)):
    db_item = db_item = list_crud.get_todo_list(db, todo_list_id)
    db_item = list_crud.update_todo_list(db, todo_list_id, update_todo_list.title, update_todo_list.description)
    return db_item

@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = list_crud.get_todo_list(db, todo_list_id)
    db_item = list_crud.delete_todo_list(db, todo_list_id)
    return db_item