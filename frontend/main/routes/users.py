from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for
import requests
import json

users = Blueprint('users', __name__, url_prefix='/')

@users.route('/home')
def user_main():
    if request.cookies.get('access_token'):
        data = { "page": 1, "per_page": 3 }
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
    else:
        return redirect(url_for('app.login'))

@users.route('/profile/user')
def user_profile():
    jwt = request.cookies.get('access_token')
    if jwt:
        usuario = request.cookies.get('id')
        api_url_user = f'{current_app.config["API_URL"]}/user/{usuario}'
        headers = {"Content-Type":"application/json", "Authorization" : f"Bearer {jwt}"}
        response = requests.get(api_url_user, headers=headers)
        user = json.loads(response.text)
        print("aaaa", user)
        return render_template('user_profile.html', jwt=jwt, user=user)
    else:
        return redirect(url_for('app.login'))

@users.route('/profile/user/modify', methods=['GET', 'POST'])
def modify_user():
    jwt = request.cookies.get('access_token')
    if jwt:
        user_id = request.cookies.get('id')
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            user = json.loads(response.text)
            return render_template('user_modify.html', user=user) 
        if request.method == 'POST':
            name = request.form['newName']
            password = request.form['newPassword']
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            data = {"name": name, "plain_password": password}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            if name != "" and password != "":
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.user_profile'))
                else:
                    return redirect(url_for('users.user_profile'))
            elif name != "":
                data = {"name": name}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.user_profile'))
                else:
                    return redirect(url_for('users.user_profile'))
            elif password != "":
                data = {"plain_password": password}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.user_profile'))
                else:
                    return redirect(url_for('users.user_profile'))
            else:
                return redirect(url_for('users.modify_user'))
    return redirect(url_for('app.login'))

@users.route('/profile/user/delete', methods=['GET', 'POST'])
def delete_user():
    jwt = request.cookies.get('access_token')
    if jwt:
        api_url = f'{current_app.config["API_URL"]}/user/{request.cookies.get("id")}'
        headers = {"Content-Type" : "application/json","Authorization":f"Bearer {jwt}"}
        response = requests.delete(api_url, headers=headers)
        return redirect(url_for('app.logout'))
    else:
        return redirect(url_for('main.login'))