from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from enum import Enum
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest
from auth import get_key, get_user, admin_only
from database import db, save_db
from typing import Annotated

class Item(BaseModel):
    name: str
    price : float
    description : str | None = None # Описание — строка или ничего
# Определяем Enum — список разрешённых значений

class Model(str, Enum):
    a = "a"  # Разрешённое значение "a"
    b = "e"  # Разрешённое значение "b"


# Функция для регистрации эндпойнтов
def register_endpoints(app: FastAPI):
    @app.get("/for_q/")
    async def once_q(q : Annotadet[list[str], Query(min_ligth = 3)]):
        register = {"q" : q}
        return register
    @app.get("/models/{model}")
    async def get_model(model: Model):
        # model: Model -- проверяет, что значение из Enum
        if model == Model.a:
                return ["haaaallo a"]
        return ["hello e"]
    # Эндпойнт для главной страницы
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    # Эндпойнт с path-параметром item_id (часть URL)
    # Например, /items/5 вернёт {"item_id": 5}
    @app.get("/items/{item_id}")
    async def read_item(item_id: int, q : str = None, key=Depends(get_key)):
        # item_id: int -- параметр должен быть числом
        return {"item_id": item_id, "q":q}

    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item, q: Annotated[str | None, Query(min_length= 3, max_length = 50, pattern = "^fixedquery$")]=None):
        result = {"item_id" : item_id, **item.model_dump()}
        if q:
            result.update({"q":q})
        return result

    @app.get("/users/me")
    async def read_user_me(user: str = Depends(get_user)):
        return {"user_id" : user}

# Эндпойнт только для админа
    @app.get("/admin/")
    async def admin_only_point(user: str = Depends(admin_only)):
        return {"message" : "Welcome, admin"}

    @app.get("/users/{user_id}")
    async def read_user(user_id: str):
        return {"user_id" : user_id}
    
    @app.post("/items/")
    async def create_item(item: Item):
        #проверяем цену
        if item.price > 100:
            raise HTTPException(status_code=400, detail="слишком дорогой")
        db.append(item.dict())
        save_db(db)
        return item

    @app.get("/items/")
    async def read_item():
        return db
