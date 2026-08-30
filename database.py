import json

def load_db():
    try:
        with open("db.json", "r") as f:
            return json.load(f) # Читаем JSON как список
    except FileNotFoundError:
        return []

#сохранаем в json
def save_db(data):
    with open ("db.json", "w") as f:
        json.dump(data, f)

# Загружаем базу данных при старте
db = load_db()
