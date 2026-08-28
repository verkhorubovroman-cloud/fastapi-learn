from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, AfterValidator
from enum import Enum
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest
from auth import get_key, get_user, admin_only
from database import db, save_db
from typing import Annotated
from valid import check_valid_id
import random

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2"
}


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
    @app.get("/once_fixedquery/")
    async def once_fixdquery(q: Annotated[str | None, Query(pattern = "^fixedquery$")]):
        return q
    @app.get("/for_q/")
    async def once_q(q : Annotated[list[str], Query(min_ligth = 3, alias = "item_query", deprecated = True)] = ["foo", "bar"]):
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
    async def update_item(item_id: int, item: Item, q: Annotated[str | None, Query(title= "Query string", description="this is q", min_length= 3, max_length = 50)]=None):
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

    @app.get("/not_openapi/")
    async def nothing_openapi(hidden_query :  Annotated[str | None, Query(include_in_schema = False)] = None):
        if hidden_query:
            return {"hidden_query" : hidden_query}
        return {"hidden_query" : "Not found"}

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
    @app.get("/checking/")
    async def checking(id : Annotated[str | None,   AfterValidator(check_valid_id)] = None ):
        if id:
            item = data.get(id)
        else:
            id, item = random.choice(list(data.items()))
        return {"id" : id, "item" : item}
        
