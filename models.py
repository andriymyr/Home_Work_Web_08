from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import *
import configparser
import pathlib
import sys


file_config = pathlib.Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "user")
password = config.get("DB", "password")
db_name = config.get("DB", "db_name")
db = config.get("DB", "db")
domain = config.get("DB", "domain")
authors = config.get("json", "authors")
qoutes = config.get("json", "qoutes")


uri = f"mongodb+srv://{username}:{password}@{db_name}.{domain}/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))
try:
    client.admin.command("ping")
except Exception as e:
    print(e)
    sys.exit(1)

connect(db=db, host=uri)


class Author(Document):
    fullname = StringField(max_length=150)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()


class Qoute(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    meta = {"allow_inheritance": True}


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()
