import sqlite3

def connection():
    # подключение бд
    conn = sqlite3.connect('base.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS students (id int auto_increment primary key, id_tg int, zakaz BOOLEAN, cnt INT, id_zakaza INT)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS teachers (id int auto_increment primary key, id_tg int, zakaz BOOLEAN, cnt INT, name VARCHAR(50), grade INT, last_zakaz INT)')
    conn.commit()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, id_tg_student INT, description VARCHAR(50), id_tg_teacher INT, sost VARCHAR(50), vremya TIMESTAMP DEFAULT CURRENT_TIMESTAMP, budget INT, photo_zadaniya INT, answer VARCHAR(500), photo_answer INT, state_payment VARCHAR(500))')
    conn.commit()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS otkliki (id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, id_teacher INT, type VARCHAR(50))')
    conn.commit()