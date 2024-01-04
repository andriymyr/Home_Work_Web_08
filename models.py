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
domain = config.get("DB", "domain")


uri = f"mongodb+srv://{username}:{password}@{db_name}.{domain}/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


connect(db="web17",host=uri)

print ("_"*60)



class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))
    meta = {"allow_inheritance": True}


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()


if __name__ == "__main__":
    ross = User(email="ross@example.com", first_name="Ross", last_name="Lawley").save()

    john = User(email="john@example.com")
    john.first_name = "John"
    john.last_name = "Lawley"
    john.save()

    post1 = TextPost(title="Fun with MongoEngine", author=john)
    post1.content = "Took a look at MongoEngine today, looks pretty cool."
    post1.tags = ["mongodb", "mongoengine"]
    post1.save()

    post2 = LinkPost(title="MongoEngine Documentation", author=ross)
    post2.link_url = "http://docs.mongoengine.com/"
    post2.tags = ["mongoengine"]
    post2.save()