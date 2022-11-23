from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for
import requests
import json

poems = Blueprint('poems', __name__, url_prefix='/')

@poems.route('/profile/user/poemas')
def my_poems():
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/poems'
        data = {"page":1,"per_page":10}
        headers = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
        response = requests.get(api_url, json=data, headers=headers)
        poems = json.loads(response.text)
        return render_template('user_poems.html', poems=poems["poems"])
    else:
        return redirect(url_for('app.login'))

@poems.route('/view/poem/<int:id>', methods=['GET'])
def view_poem(id):
    jwt = request.cookies.get('access_token')
    user_id = request.cookies.get("id")
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    headers = {"Content-Type" : "application/json"}
    response = requests.get(api_url, headers=headers)
    poem = json.loads(response.text)
    api_url_quali = f'{current_app.config["API_URL"]}/qualifications'
    data_quali = {"poem_id" : id}
    headers_quali = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
    response = requests.get(api_url_quali, json=data_quali, headers=headers_quali)
    qualifications = json.loads(response.text)
    print("Poema",poem)
    print("Calificaciones",qualifications)
    return render_template('poem_view.html', poem=poem, user_id=int(user_id), qualifications=qualifications)

@poems.route('/poem/create', methods=['GET','POST'])
def create_poem():
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            user_id = request.cookies.get("id")
            data = {"title": title, "body": body, "user_id": user_id  }
            headers = {"Content-Type" : "application/json", "Authorization" : f"Bearer {jwt}"}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                if response.ok:
                    response = json.loads(response.text)
                    print(response, 'AJAJAJAJAJ')
                    return redirect(url_for('poems.view_poem', id=response["id"], jwt=jwt))
                else:
                    return redirect(url_for('poems.create_poem'))
            else:
                return redirect(url_for('poems.create_poem'))
        else:
            return render_template('poem_create.html', jwt=jwt)
    else:
        return redirect(url_for('app.login'))

@poems.route('/poem/modify/<int:id>', methods=['GET', 'POST'])
def modify_poem(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/poem/{id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            poem = json.loads(response.text)
            return render_template('poem_modify.html', poem=poem)
        if request.method == 'POST':
            api_url = f'{current_app.config["API_URL"]}/poem/{id}'
            data = {"title": request.form['title'], "body": request.form['body']}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            response = requests.put(api_url, json=data, headers=headers)
            return redirect(url_for('users.user_main', id=id))
    return redirect(url_for('app.login'))

@poems.route('/poem/<int:id>/delete')
def delete_poem(id):
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/poem/{id}'
        headers = {"Content-Type" : "application/json","Authorization":f"Bearer {jwt}"}
        response = requests.delete(api_url, headers=headers)
        return redirect(url_for('users.user_main'))
    else:
        return redirect(url_for('main.login'))