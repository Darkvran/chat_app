from flask import Flask, render_template, request
import sqlite3, hashlib

app = Flask(__name__)
database_path = 'users.db'
db = sqlite3.connect(database_path, check_same_thread=False)
sql = db.cursor()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        if '' in request.form.values():
            return render_template('register.html', message='Пожалуйста, заполните все поля')
        elif request.form['password'] != request.form['password_repeat']:
            return render_template('register.html', message='Неверный повтор пароля')

        sql.execute('SELECT email, username FROM Users WHERE email = ? OR username = ?',
                    (request.form['email'], request.form['username']))
        existing_user = sql.fetchall()

        if existing_user:
            if existing_user[0][0] == request.form['email']:
                return render_template('register.html', message='Этот адрес занят')

            if existing_user[0][1] == request.form['username']:
                return render_template('register.html', message='Этот ник занят')

        data = (request.form['email'], request.form['username'], '/static/avatars/no_avatar.jpg', '',
                hashlib.sha256(request.form['password'].encode()).hexdigest())

        sql.execute('INSERT INTO Users (email, username, avatar, about, password) VALUES (?, ?, ?, ?, ?)', data)
        db.commit()

        return render_template('register.html', message='Регистрация завершена')

        #print(result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if '' in request.form.values():
            return render_template('login.html', message='Пожалуйста, заполните все поля')
        sql.execute('SELECT email FROM Users WHERE email = ?',
                    (request.form['email'],))
        existing_user = sql.fetchall()
        if existing_user:
            sql.execute('SELECT email, password FROM Users WHERE email = ? AND password = ?',
                    (request.form['email'], hashlib.sha256(request.form['password'].encode()).hexdigest()))
            result = sql.fetchall()
            if len(result) == 0:
                print(result)
                return render_template('login.html', message='Неверный пароль')

            else:
                print(result)
                return render_template('login.html', message='Успешная авторизация!')
        else:
            return render_template('login.html', message='Данного пользователя не существует')




if __name__ == '__main__':
    app.run()
