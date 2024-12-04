from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder='templates')

connection = sqlite3.connect('Flask.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS User    
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
login TEXT UNIQUE,
password TEXT
)
""")

connection.commit()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if password != repeat_password:
            return render_template('registration.html',  error='Пароли не совпадают')
        cursor.execute('SELECT * FROM User WHERE login = ?', (login,))
        if cursor.fetchone():
            return render_template('registration.html', error='Такой user уже существует')
        cursor.execute('INSERT INTO User (login, password) VALUES (?, ?)', (login, password))
        connection.commit()
        return render_template('home.html')
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute('SELECT * FROM User WHERE login = ? AND password = ?', (login, password))
        if not cursor.fetchone():
            return render_template('login.html',  error='Что-то пошло не так')

        return render_template('main.html')
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/login/helper')
def helper():
    return render_template('helper.html')


@app.route('/login/helper/wait')
def wait():
    return render_template('wait.html')


if __name__ == '__main__':
    app.run(debug=True)