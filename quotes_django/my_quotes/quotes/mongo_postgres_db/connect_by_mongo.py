import configparser
from pathlib import Path

from mongoengine import connect


path = Path(__file__).parent

config = configparser.ConfigParser()
config.read(path.joinpath("config.ini"))

mongo_user = config.get("DB", "user")
mongo_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

connect(host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{domain}/{db_name}", ssl=True)
