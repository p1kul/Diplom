from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from models import session, User, Randomaizer
from random import choice
app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/registration')
async def registration_get(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@app.post('/registration')
async def registration_post(request: Request):
    sessions = session()
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    repeat_password = form.get('repeat_password')
    if password != repeat_password:
        return templates.TemplateResponse('registration.html', {'request': request, 'error': 'Пароли не совпадают'})
    user = sessions.query(User).filter_by(login=login).first()
    if user:
        return templates.TemplateResponse('registration.html', {'request': request, 'error': 'Такой user уже существует'})
    sessions.add(User(login=login, password=password))
    sessions.commit()
    return templates.TemplateResponse('home.html', {'request': request})


@app.get('/login')
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/login')
async def login_post(request: Request):
    sessions = session()
    form = await request.form()
    login = form.get('login')
    password = form.get('password')
    user = sessions.query(User).filter_by(login=login, password=password).first()
    if not user:
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Что-то пошло не так'})
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/main')
async def main(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.post('/main')
async def main_post(request: Request):
    sessions = session()
    form = await request.form()
    something = form.get('something')
    sessions.add(Randomaizer(something=something))
    sessions.commit()
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/main/randoms')
async def randoms(request: Request):
    sessions = session()
    ran = sessions.query(Randomaizer.something).all()
    answer = choice(ran)
    slovo = ''.join(answer)
    sessions.close()
    return templates.TemplateResponse('randoms.html', {'request': request, 'message': slovo})


@app.get('/login/helper')
async def login_get(request: Request):
    return templates.TemplateResponse('helper.html', {'request': request})


@app.get('/login/helper/wait')
async def wait(request: Request):
    return templates.TemplateResponse('wait.html', {'request': request})


