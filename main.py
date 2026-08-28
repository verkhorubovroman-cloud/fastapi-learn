from fastapi import FastAPI
from endpoints import register_endpoints

# Создаём приложение FastAPI
app = FastAPI()
register_endpoints(app)
# Регистрируем эндпойнты
#register_endpoints(app)
