from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest

# Настраиваем API-ключ в заголовке X-Key
api_key = APIKeyHeader(name="X-Key")
fake_keys = ["secret"]

# Функция проверки API-ключа
def get_key(key: str = Depends(api_key)):
    if key not in fake_keys:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return key

# HTTP Basic
basic = HTTPBasic()

# Функция проверки имени и пароля
def get_user(credentials: HTTPBasicCredentials = Depends(basic)):
    if not compare_digest(credentials.password, "pass"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username.strip()

# Проверка админа
def admin_only(user: str = Depends(get_user)):
    if user.strip() != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user
