import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE employees_number;
                DROP TABLE employees;
                DROP TABLE number;
                CREATE TABLE IF NOT EXISTS employees(
                id_employee SERIAL PRIMARY KEY,
                last_name VARCHAR(40) NOT NULL,
                first_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL);
            
                CREATE TABLE IF NOT EXISTS number(
                id_number SERIAL PRIMARY KEY,
                number VARCHAR(40) NOT NULL);
            
                CREATE TABLE IF NOT EXISTS employees_number(
                id_employee int NOT NULL,
                id_number int NOT NULL,
                FOREIGN KEY (id_number) REFERENCES number(id_number), 
                FOREIGN KEY (id_employee) REFERENCES employees(id_employee),
                PRIMARY KEY (id_employee,id_number));          
                   """
        )

def add_client(conn):
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    email = input("Введите почту: ")
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO employees (first_name, last_name, email) VALUES(%s, %s, %s)
                ;
                """, (first_name, last_name , email))
        conn.commit()



def add_phone(conn):
    id_employee = int(input("Введите ID клиента: "))
    phone = input("Введите номер телефона клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
                    INSERT INTO number(number) VALUES(%s) RETURNING id_number;
                    """, (phone,))
        id_number = cur.fetchone()
        conn.commit()
        cur.execute("""
                    INSERT INTO employees_number (id_number, id_employee) VALUES(%s,%s)  
                    """, (id_number, id_employee))
        conn.commit()


def change_client(conn):
    id_employee = input ("Введите ID клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT   first_name FROM employees 
                    WHERE id_employee = %s ;
                    """, (id_employee,))
        print("Изменение данных клиента:", cur.fetchone())
        first_name = input("Измените имя: ")
        last_name = input("Измените фамилию: ")
        email = input("Измените почту: ")
        cur.execute("""
                UPDATE employees SET first_name=%s, last_name=%s, email=%s
                WHERE email=%s;
                """, (first_name, last_name, email, id_employee ))
        conn.commit()

def delete_phone(conn):
    id_employee = input("Введите ID клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE  FROM employees_number 
                    WHERE id_employee=%s;
                    """, (id_employee,))
        conn.commit()

def delete_client(conn):
    id_employee = input("Введите ID клиента: ")
    with conn.cursor() as cur:
        cur.execute("""
                        SELECT id_number FROM employees_number 
                        WHERE id_employee=%s;
                        """, (id_employee,))
        id_number = cur.fetchone()
        cur.execute("""
                        DELETE  FROM employees_number 
                        WHERE id_employee=%s;
                        """, (id_employee,))
        conn.commit()
        cur.execute("""
                        DELETE  FROM number 
                        WHERE id_number=%s;
                        """, (id_number,))
        conn.commit()
        cur.execute("""
                                DELETE  FROM employees 
                                WHERE id_employee=%s;
                                """, (id_employee,))
        conn.commit()

def find_client(conn):
    with conn.cursor() as cur:
        id_ops = int (input ("По какому признаку производиться поиск (1-Имя, 2-Фамилия, 3- Номер телефона, 4-почта --> "))
        if id_ops == 1 :
            check = input("Введите имя: ")
            cur.execute("""
                        SELECT first_name, last_name FROM employees 
                        WHERE first_name=%s;
                         """, (check,))
            print(cur.fetchall())
        elif id_ops == 2:
            check = input("Введите фамилию: ")
            cur.execute("""
                        SELECT first_name, last_name FROM employees 
                        WHERE last_name=%s;
                        """, (check,))
            print(cur.fetchall())
        elif id_ops == 3:
            check = input("Введите номер телефона: ")
            cur.execute("""
            SELECT  first_name, last_name FROM employees e
            JOIN employees_number en ON e.id_employee=en.id_employee
            JOIN number n ON en.id_number=n.id_number
            WHERE number=%s
            GROUP BY first_name, last_name 
            """, (check,))
            print(cur.fetchall())
        elif id_ops == 4:
            check = input("Введите почту: ")
            cur.execute("""
                        SELECT first_name, last_name FROM employees 
                        WHERE email=%s;
                        """, (check,))
            print(cur.fetchall())
with psycopg2.connect(database="employed", user="postgres", password="64082") as conn:
    create_db(conn)
    add_client(conn)
    add_phone(conn)
    change_client(conn)
    delete_phone(conn)
    delete_client(conn)
    find_client(conn)
conn.close()