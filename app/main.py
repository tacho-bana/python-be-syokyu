import os
from datetime import datetime

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

from .dependencies import get_db
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from .models.item_model import ItemModel
from .models.list_model import ListModel

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: int
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

class Item(BaseModel):
    id: int
    todo_list_id: int
    description: str
    status_code: int
    due_at: datetime
    updated_at: datetime


@app.get("/echo")
def get_echo(message: str, name: str):
    return {'Message': message+" "+name+"!"}

@app.get("/health", tags=["System"])
def get_health():
    return {"status": "ok"}

@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, session: Session = Depends(get_db)):
    db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    return db_item

@app.post("/lists", tags = ["Todoリスト"])
def post_todo_list(new_todo_list: NewTodoList, session: Session = Depends(get_db)):
    db_item = ListModel(
        title=new_todo_list.title,
        description=new_todo_list.description
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@app.put("/lists/{todo_list_id}", tags=["Todoリスト"])
def put_todo_list(todo_list_id: int, update_todo_list: UpdateTodoList, session: Session = Depends(get_db)):
    db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    
    db_item.title = update_todo_list.title
    db_item.description = update_todo_list.description

    session.commit()
    session.refresh(db_item)
    return db_item

@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int, session: Session = Depends(get_db)):
    db_item = session.query(ListModel).filter(ListModel.id == todo_list_id).first()
    session.delete(db_item)
    session.commit()
    return {}

@app.post("/lists/{todo_list_id}/items", response_model=Item, tags=["Todo項目"])
def create_todo_item(new_todo_item: NewTodoItem, session: Session = Depends(get_db)):


    db_item = ItemModel(
        todo_list_id= 9,
        title=new_todo_item.title,
        description=new_todo_item.description,
        status_code = new_todo_item.status_code,
        due_at=new_todo_item.due_at
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)

    return db_item

    

@app.get("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todo項目"])
def get_todo_item(todo_list_id: int, todo_item_id: int, session: Session = Depends(get_db)):
    
    db_item = (session.query(ItemModel).filter(ItemModel.todo_list_id == todo_list_id, ItemModel.id == todo_item_id).first())
    
    return db_item