from wsgiref import headers
from flask import Blueprint, redirect, request, url_for, render_template, request, Response, make_response
import requests
import json

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    api_url = "http://127.0.0.1:5000/poems"
    data = {"page": 1, "per_page": 10}
    jwt = requests.cookies.get("access_token")
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(jwt)}
    print(jwt)
    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)
    print(response.text)
    poems = json.loads(response.text)
    print(poems)
    return render_template('index.html')

@app.route('/main_page')
def main_page():
    return render_template('main_page.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        api_url = "http://127.0.0.1:5000/auth/login"
        email = request.form['email']
        password = request.form['password']
        print(email)
        print(password)
        print(request)

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/new_password')
def new_password():
    return render_template('new_password.html')

@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/my_profile')
def my_profile():
    return render_template('my_profile.html')

@app.route('/my_poem_list')
def poem_list():
    api_url = "http://127.0.0.1:6000/poems"
    data = {"page": 1, "per_page": 5}
    jwt = request.cookies.get("access_token")
    print(jwt)
    headers = {"Content-Type": "application/json", "Authorization": "Bearer {}".format(jwt)}
    response = requests.get(api_url, json=data, headers=headers)
    print(response.status_code)
    poems = json.loads(response.text)
    list_poems = poems["poems"]
    for poem in list_poems:
        print(poem)  
    print(type(list_poems))
    return render_template('my_poem_list.html', poems=list_poems)

@app.route('/view_poems')
def view_poem():
    return render_template('view_poems.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/mark_poem')
def mark():
    return render_template('mark_poem.html')