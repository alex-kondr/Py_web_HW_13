from pathlib import Path

from mongoengine import connect

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")



mongo_user = env("MONGO_USER")
mongo_pass = env("MONGO_PASS")
db_name = env("MONGO_DB_NAME")
domain = env("MONGO_DOMAIN")

connect(host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}", ssl=True)
