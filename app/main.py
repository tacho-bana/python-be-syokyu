from fastapi import FastAPI
from .routers import list_router, item_router

app = FastAPI()

app.include_router(list_router.router)  
app.include_router(item_router.router)  

