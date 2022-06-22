import psycopg2
from flask import Flask
from flask import render_template, request, redirect, abort

def connection(db_name, db_user, db_password, db_host, db_port):
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    return connection

conn = connection("phonebook", "postgres", "smthpass", "127.0.0.1", "5432")

cur = conn.cursor()

create = ('''CREATE TABLE IF NOT EXISTS phones(
    first_name CHAR(30) NOT NULL,
    last_name CHAR(30),
    phone_num CHAR(15))''')

def insert(first_name, last_name, phone_num):
    insert = (f"INSERT INTO phones (first_name, last_name, phone_num) "
              f"VALUES ('{first_name}', '{last_name}', '{phone_num}')")
    cur.execute(insert)
    conn.commit()

def list():
    cur.execute('SELECT * FROM phones')
    result = cur.fetchall()
    listing = []
    for user in result:
        listing.append(
            {'username': user[0] + user[1], 'first_name': user[0], 'last_name': user[1], 'phone_num': user[2]})
    return listing


cur.execute(create)
conn.commit()

app = Flask(__name__)

@app.route('/', methods=['get'])
def index():
    return redirect('http://127.0.0.1:5000/users')

@app.route('/users', methods=['get', 'post'])
def users():
    if request.method == 'POST':
        name = request.form.get('first_name')
        surname = request.form.get('last_name')
        phone_number = request.form.get('phone_num')
        insert(name, surname, phone_number)
    return render_template('site.html', users=list())

@app.route('/users/<username>')
def check(username):
    users = ''
    for i in list():
        if username == i['username']:
            users = i
        return f'<h2>UserName:{users["username"]} </h2> <br>'\
           f'<h2>Name:{users["first_name"]} </h2> <br>'\
           f'<h2>Surname:{users["last_name"]} </h2> <br>' \
           f'<h2>Phone_number:{users["phone_num"]} </h2> <br>'\

if __name__ == '__main__':
    app.run(debug=True)