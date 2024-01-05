from models import Author, Qoute, connect, authors_data, qoutes_data

for data in authors_data:
    mongo_author = Author(fullname=data["fullname"])
    mongo_author.born_date = data["born_date"]
    mongo_author.born_location= data["born_location"]
    mongo_author.description= data["description"]
    mongo_author.save()

for data in qoutes_data:
    mongo_qoute= Qoute(tags=data["tags"])
    mongo_qoute.author= Author.objects(fullname=data["author"]).first()
    mongo_qoute.quote= data["quote"]
    mongo_qoute.save()



"""
    fullname = StringField(max_length=150)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()


class Qoute(Document):
    tags = StringField()
    author = ReferenceField(Author)
    quote = StringField()

"""