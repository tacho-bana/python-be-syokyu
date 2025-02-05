from sqlalchemy.orm import Session
from ..models.list_model import ListModel
from ..schemas.list_schema import UpdateTodoList, NewTodoList

def get_todo_list(db: Session, todo_list_id: int):
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()

def create_todo_list(db:Session, new_todo_list: NewTodoList):
    db_item = ListModel(
        title=new_todo_list.title,
        description=new_todo_list.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_todo_list(db: Session, todo_list_id: int, update_todo_list: UpdateTodoList):
    db_item = Session.query(ListModel).filter(ListModel.id==todo_list_id).first()
    db_item.title = update_todo_list.title
    db_item.description = update_todo_list.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_todo_list(db: Session, todo_list_id: int):
    db_item = Session.query(ListModel).filter(ListModel.id==todo_list_id).first()
    if not db_item:
        return {"Error"}
    db.delete(db_item)
    db.commit()
    return {"OK"}

