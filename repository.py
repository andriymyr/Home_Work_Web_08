import json
import sys
import signal
import faker
import random
import producer
import consumer

import threading

from models import Author, Qoute, User, Post, connect, authors, qoutes, count_user
from mongoengine.queryset.visitor import Q

exit_event = threading.Event()


def signal_handler(signum, frame):
    print("Received CTRL+C, stopping the worker...")
    exit_event.set()


def read_json():
    e = ""
    try:
        with open(authors, "r", encoding="utf-8") as fh:
            authors_data = json.load(fh)
        with open(qoutes, "r", encoding="utf-8") as fh:
            qoutes_data = json.load(fh)
    except Exception as e:
        print(e)
        # sys.exit(1)
    return authors_data, qoutes_data, e


def update_mongo(authors_data, qoutes_data):
    for data in authors_data:
        mongo_author = Author(fullname=data["fullname"])
        mongo_author.born_date = data["born_date"]
        mongo_author.born_location = data["born_location"]
        mongo_author.description = data["description"]
        mongo_author.save()

    for data in qoutes_data:
        mongo_qoute = Qoute(tags=data["tags"])
        mongo_qoute.author = Author.objects(fullname=data["author"]).first()
        mongo_qoute.quote = data["quote"]
        mongo_qoute.save()


def find_data(fild, args):
    if not fild:
        print("no find")
    for search_data in args:
        if fild == "fullname":
            author = Author.objects(fullname=search_data).first().id
            if author:
                res = Qoute.objects(author=author)
                print(f"search <{search_data}> in field <{fild}> :\n")
                for qout in res:
                    print(qout.quote)
        elif fild == "tags":
            for tag_ in Qoute.objects(tags=search_data):
                print(
                    f"search {search_data} in field {fild} :\n Author {tag_.author.fullname} - {tag_.quote}"
                )


def finds_data(fild, args):
    if not fild:
        print("no find")
    for search_data in args:
        if fild == "fullname":
            print(f"search <{search_data}> in field <{fild}> :\n")
            authors = Author.objects(fullname__icontains=search_data)  # .first().id
            for author in authors:
                res = Qoute.objects(author__icontains=author.id)
                for qout in res:
                    print(qout.author.fullname, "--", qout.quote)
        elif fild == "description":
            res = Author.objects(description__icontains=search_data)
            print(f"search <{search_data}> in field <{fild}> :\n")
            for desc in res:
                print(
                    desc.fullname,
                    "_",
                    desc.born_date,
                    "_",
                    desc.born_location,
                    desc.description,
                )
        elif fild == "tags":
            print(f"search {search_data} in field {fild} :")
            for tag_ in Qoute.objects(tags__icontains=search_data):
                print(f"Author {tag_.author.fullname} - {tag_.quote}")


def create_messege():
    fake = faker.Faker()
    count = 0
    while count < float(count_user):
        count += 1
        user_ = User(fullname=fake.name())
        user_.email = fake.email()
        user_.phone = fake.phone_number()
        user_.channel = random.choice(["email", "phone"])

        user_.save()
        post_ = Post(author=user_.id)
        post_.title = fake.text(max_nb_chars=100)
        post_.save()
        # post_.tags
        # post_.meta


def post_messege():
    producer.producer()


def send_messege():
    my_thread = threading.Thread(target=consumer.consumer)

    my_thread.start()
    signal.signal(signal.SIGINT, signal_handler)
    my_thread.join()
