from flask import Flask, Blueprint, current_app, render_template, make_response, request, redirect, url_for
import requests
import json

app = Blueprint('app', __name__, url_prefix='/')

@app.route('/')
def index():
    data = { "page": 1, "per_page": 3}
    if 'page' in request.args:
        data["page"] = request.args.get('page', '')
    api_url = f'{current_app.config["API_URL"]}/poems'
    headers = { "Content-Type": "application/json" }
    response = requests.get(api_url, json=data, headers=headers)
    poems = json.loads(response.text)
    pagination = {}
    pagination["pages"] = json.loads(response.text)["pages"]
    pagination["current_page"] = json.loads(response.text)["page"]
    return render_template('main.html', poems=poems["poems"], pagination=pagination)

@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        if email != None and password != None: 
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            data = {"email" : email, "password" : password}
            headers = {"Content-Type" : "application/json"}
            response = requests.post(api_url, json = data, headers = headers)
            print(response, "Error")
            if (response.ok): 
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                response = make_response(redirect(url_for('users.user_main')))
                response.set_cookie("access_token", token)
                response.set_cookie("id", user_id)
                return response
        return(render_template('login.html', error = "Usuario o contraseña incorrectos"))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    req = make_response(redirect(url_for('app.index')))
    req.delete_cookie("access_token")
    req.delete_cookie("id")
    return req

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = 'poet'
        if name != "" and email != "" and password != "":
            api_url = f'{current_app.config["API_URL"]}/auth/register'
            data = {"name": name, "email": email, "password": password, "role": role}
            headers = { "Content-Type": "application/json" }
            response = requests.post(api_url, json = data, headers = headers)
            print(response, "response del register")
            if response.ok:
                return redirect(url_for("app.login"))
            else:
                return redirect(url_for("app.login"))
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")