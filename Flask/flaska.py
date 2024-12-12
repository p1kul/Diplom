from flask import Flask, render_template, request
from models import session, User, Randomaizer
from random import choice
app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    sessions = session()
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if password != repeat_password:
            return render_template('registration.html',  error='Пароли не совпадают')
        user = sessions.query(User).filter_by(login=login).first()
        if user:
            return render_template('registration.html', error='Такой user уже существует')
        sessions.add(User(login=login, password=password))
        sessions.commit()
        return render_template('home.html')
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    sessions = session()
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = sessions.query(User).filter_by(login=login, password=password).first()
        if not user:
            return render_template('login.html',  error='Что-то пошло не так')

        return render_template('main.html')
    sessions.close()
    return render_template('login.html')


@app.route('/main', methods=['GET', 'POST'])
def main():
    sessions = session()
    if request.method == 'POST':
        something = request.form.get('something')
        sessions.add(Randomaizer(something=something))
        sessions.commit()
        return render_template('main.html')
    return render_template('main.html')


@app.route('/main/randoms', methods=['GET'])
def randoms():
    sessions = session()
    if request.method == 'GET':
        ran = sessions.query(Randomaizer.something).all()
        answer = choice(ran)
        slovo = ''.join(answer)
        return render_template('randoms.html', message=slovo)
    sessions.close()
    return render_template('randoms.html')


@app.route('/login/helper')
def helper():
    return render_template('helper.html')


@app.route('/login/helper/wait')
def wait():
    return render_template('wait.html')


if __name__ == '__main__':
    app.run(debug=True)


