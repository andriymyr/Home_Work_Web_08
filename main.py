import argparse
import repository

# import producer

from bson.objectid import ObjectId
from mongoengine import (
    connect,
    Document,
    StringField,
    IntField,
    ListField,
    DoesNotExist,
)

parser = argparse.ArgumentParser(description="Server Cats Enterprise")
parser.add_argument(
    "--action",
    help="update, read, find, finds, create_messege, post_messege, send_messege",
)
parser.add_argument("--name")
parser.add_argument("--tag")

arg = vars(parser.parse_args())

action = arg.get("action")
name = arg.get("name")
age = arg.get("tag")
e = ""
authors_data = ""
qoutes_data = ""


def main():
    match action:
        case "read":
            authors_data, qoutes_data, error_ = repository.read_json()
            if error_:
                print([e.to_mongo().to_dict() for e in error_])
            else:
                print(authors_data, f"\n", qoutes_data)
        case "update":
            authors_data, qoutes_data, error_ = repository.read_json()
            repository.update_mongo(authors_data, qoutes_data)
        case "find":
            find_ = True
            while find_:
                text = input(
                    "Введить данні для пошуку у форматі 'поле пошуку,значення(може бути декілька через кому)\n"
                )
                text = text.split(",")
                fild = text[0]
                args = text[1:]
                repository.find_data(fild, args)
                if fild.lower() == "exit":
                    find_ = False
        case "finds":
            find_ = True
            while find_:
                text = input(
                    "Введить данні для пошуку у форматі 'поле пошуку,значення/неповне(може бути декілька через кому)\n"
                )
                text = text.split(",")
                fild = text[0]
                args = text[1:]
                repository.finds_data(fild, args)
                if fild.lower() == "exit":
                    find_ = False
        case "create_messege":
            repository.create_messege()
        case "post_messege":
            repository.post_messege()
        case "send_messege":
            repository.send_messege()
        case _:
            print("Unknown command")


if __name__ == "__main__":
    main()

"""
1. Перевірка наявності правильності файлів qoutes.json та authors.json
    py main.py --action read
2. Внесення даних з qoutes.json та authors.json в базу даних
    py main.py --action update
3. Пошук по полях/значеннях - Author.fullname, Qoute.tags
    py main.py --action find

        Введить данні для пошуку у форматі 'поле пошуку,значення(може бути декілька через кому)
        fullname,Albert Einstein
        search <Albert Einstein> in field <fullname> :

        “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
        “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”
        “Try not to become a man of success. Rather become a man of value.”

        Введить данні для пошуку у форматі 'поле пошуку,значення(може бути декілька через кому)
        tags,humor,life
        search humor in field tags :
        Author Steve Martin - “A day without sunshine is like, you know, night.”
        search life in field tags :
        Author Albert Einstein - “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”
4. Пошук по полях/значеннях/частина - Author.fullname, Qoute.tags, Author.description
    py main.py --action finds

        Введить данні для пошуку у форматі 'поле пошуку,значення/неповне(може бути декілька через кому)
        fullname,Albert Einstei,St
        search <Albert Einstei> in field <fullname> :

        “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
        “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”
        “Try not to become a man of success. Rather become a man of value.”
        search <St> in field <fullname> :

        “The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”
        “There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”
        “Try not to become a man of success. Rather become a man of value.”    
5. Створення користувачів та повідомдень
    py main.py --action create_messege
6. Розміщення повідомлень в черзі
    py main.py --action post_messege 
7. Отримання повідомлень з черги та їх обробка
    py main.py --action send_messege
"""
