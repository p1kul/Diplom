from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory='templates')

connection = sqlite3.connect('FastAPI.db', check_same_thread=False)
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


@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/registration')
async def registration_get(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@app.post('/registration')
async def registration_post(request: Request):
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    repeat_password = form.get('repeat_password')
    if password != repeat_password:
        return templates.TemplateResponse('registration.html', {'request': request, 'error': 'Пароли не совпадают'})
    cursor.execute('SELECT * FROM User WHERE login = ?', (login,))
    if cursor.fetchone():
        return templates.TemplateResponse('registration.html', {'request': request, 'error': 'Такой user уже существует'})
    cursor.execute('INSERT INTO User (login, password) VALUES (?, ?)', (login, password))
    connection.commit()
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/login')
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/login')
async def login_post(request: Request):
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    cursor.execute('SELECT * FROM User WHERE login = ? AND password = ?', (login, password))
    if not cursor.fetchone():
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Что-то пошло не так'})
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/main')
async def main(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/login/helper')
async def login_get(request: Request):
    return templates.TemplateResponse('helper.html', {'request': request})


@app.get('/login/helper/wait')
async def wait(request: Request):
    return templates.TemplateResponse('wait.html', {'request': request})