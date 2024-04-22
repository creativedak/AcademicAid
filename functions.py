import sqlite3


#функции
def dobavit_user(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT id_tg FROM students')
    mas = cur.fetchall()
    mas = [int(x[0]) for x in mas]
    if id not in mas:
        cur.execute("INSERT INTO students (id_tg) VALUES ('%d')" % (id))
        conn.commit()

def delete_user(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f'DELETE FROM students WHERE id_tg = {id}')
    conn.commit()

def delete_teacher(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f'DELETE FROM teachers WHERE id_tg = {id}')
    conn.commit()
def dobavit_teacher(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT id_tg FROM teachers')
    mas = cur.fetchall()
    mas = [int(x[0]) for x in mas]
    if id not in mas:
        cur.execute("INSERT INTO teachers (id_tg) VALUES ('%d')" % (id))
        conn.commit()


def sobrat_info_users():
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    users = cur.fetchall()
    ans = ''
    cnt = 0
    for elem in users:
        elem = [str(x) for x in elem]
        for i in elem:
            ans += i+' '
        ans+='\n'
        cnt+=1
    ans = 'Всего пользователей: ' + str(cnt) + '\n' + ans+'\n'
    return ans

def sobrat_info_teachers():
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM teachers')
    users = cur.fetchall()
    ans = ''
    cnt = 0
    for elem in users:
        ans += str(elem[0])+' '+str(elem[1])+'\n'
        cnt+=1
    ans = 'Всего решал: ' + str(cnt) + '\n' + ans+'\n'
    return ans

def sobrat_info_orders():
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders')
    users = cur.fetchall()
    ans = ''
    cnt = 0
    for elem in users:
        for i in elem:
            ans+=str(i)+' '
        ans+='\n'
    ans = 'Всего пользователей: ' + str(cnt) + '\n' + ans+'\n'
    return ans

def proof_reshala(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT id_tg FROM teachers')
    teachers = cur.fetchall()
    teachers = [int(x[0]) for x in teachers]
    return id in teachers

def proof_student(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('SELECT id_tg FROM students')
    teachers = cur.fetchall()
    teachers = [int(x[0]) for x in teachers]
    return id in teachers

def add_order(id_student, description, budget, photo_id=None):
    # Установка соединения с базой данных
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Подготовка запроса на добавление заказа
    query = '''INSERT INTO orders (id_tg_student, description, id_tg_teacher, sost, budget, photo_zadaniya, answer, state_payment)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    # Значения для вставки в таблицу
    values = (id_student, description, None, 'новый', budget, photo_id, None, 'не оплачен')

    # Выполнение запроса
    cur.execute(query, values)
    # Подтверждение изменений
    conn.commit()

    cur.execute("SELECT id FROM orders WHERE id_tg_student = ? AND sost = 'новый'", (id_student,))
    a = cur.fetchone()[0]
    conn.commit()

    cur.execute('UPDATE students SET id_zakaza = ? WHERE id_tg = ?', (a, id_student))
    conn.commit()

    conn.close()

def cnt_orders():
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    ans = cur.fetchall()
    return len(ans)


def get_order_by_index(i):
    # Проверяем, что i является целым числом
    if i>=cnt_orders():
        return False

    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Используем безопасное форматирование для i, предварительно проверив его значение
    query = "SELECT * FROM orders WHERE sost = 'новый' LIMIT 1 OFFSET ?"

    # Выполнение запроса с безопасной подстановкой значения i-1
    cur.execute(query, (i,))
    order = cur.fetchone()

    conn.close()

    # Преобразовываем результат в строку, если запись была найдена
    if order:
        mas=[]
        for elem in order:
            mas.append(elem)
        return mas
    else:
        return False

def update_zakaz_status_student(student_id, sost):
    # Установка соединения с базой данных
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Подготовка SQL запроса на обновление статуса zakaz
    query = '''UPDATE students SET zakaz = ? WHERE id_tg = ?'''

    # Значения для обновления: True для zakaz, student_id - идентификатор студента
    values = (sost, student_id)

    try:
        # Выполнение запроса
        cur.execute(query, values)

        # Подтверждение изменений
        conn.commit()
    except sqlite3.Error as e:
        pass
    finally:
        # Закрытие соединения с базой данных
        conn.close()

def update_zakaz_status_teacher(student_id, sost):
    # Установка соединения с базой данных
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Подготовка SQL запроса на обновление статуса zakaz
    query = '''UPDATE teachers SET zakaz = ? WHERE id_tg = ?'''

    # Значения для обновления: True для zakaz, student_id - идентификатор студента
    values = (sost, student_id)

    try:
        # Выполнение запроса
        cur.execute(query, values)

        # Подтверждение изменений
        conn.commit()
    except sqlite3.Error as e:
        pass
    finally:
        # Закрытие соединения с базой данных
        conn.close()

def dostat_cnt_student(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f"SELECT cnt FROM students WHERE id_tg={id}")
    ans = cur.fetchone()
    print(ans)
    return int(ans[0])

def update_cnt_student(id, znach):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Подготовка SQL запроса на обновление статуса zakaz
    query = '''UPDATE students SET cnt = ? WHERE id_tg = ?'''
    values = (znach, id)
    try:
        # Выполнение запроса
        cur.execute(query, values)

        # Подтверждение изменений
        conn.commit()
    except sqlite3.Error as e:
        pass
    finally:
        # Закрытие соединения с базой данных
        conn.close()

def dostat_cnt_teacher(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f"SELECT cnt FROM teachers WHERE id_tg={id}")
    ans = cur.fetchone()
    return int(ans[0])

def update_cnt_teacher(id, znach):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()

    # Подготовка SQL запроса на обновление статуса zakaz
    query = '''UPDATE teachers SET cnt = ? WHERE id_tg = ?'''
    values = (znach, id)
    try:
        # Выполнение запроса
        cur.execute(query, values)

        # Подтверждение изменений
        conn.commit()
    except sqlite3.Error as e:
        pass
    finally:
        # Закрытие соединения с базой данных
        conn.close()

def status_teacher(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f"SELECT zakaz FROM teachers WHERE id_tg={id}")
    return cur.fetchone()[0]

def status_student(id):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f"SELECT zakaz FROM students WHERE id_tg={id}")
    return cur.fetchone()[0]

def update_order(id):
    pass

def dobavit_otklik(id_teacher, id_zakaz):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO otkliki (order_id, id_teacher, type) VALUES (?, ?, ?)', (id_zakaz, id_teacher, 'новый'))
    conn.commit()
    conn.close()

def dostat_id_zakaza(id_student):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute(f'SELECT id_zakaza FROM students WHERE id_tg = {id_student}')
    ans=cur.fetchone()
    if ans[0] != None:
        return int(ans[0])

def get_otkliki(id, a):
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    id = int(id)
    a = int(a)
    query = f'SELECT * FROM otkliki WHERE order_id = ? ORDER BY type ASC LIMIT 1 OFFSET ?'

    cur.execute(query, (id, a))
    order = [int(x) for x in cur.fetchone()]
    return order