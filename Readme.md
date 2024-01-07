1.  Перевірка наявності правильності файлів qoutes.json та authors.json
    py main.py --action read
2.  Внесення даних з qoutes.json та authors.json в базу даних
    py main.py --action update
3.  Пошук по полях/значеннях - Author.fullname, Qoute.tags
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

4.  Пошук по полях/значеннях/частина - Author.fullname, Qoute.tags, Author.description
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

5.  Створення користувачів та повідомдень
    py main.py --action create_messege
6.  Розміщення повідомлень в черзі
    py main.py --action post_messege
7.  Отримання повідомлень з черги та їх обробка
    py main.py --action send_messege
