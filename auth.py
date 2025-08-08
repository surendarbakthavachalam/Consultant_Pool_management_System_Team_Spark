# project/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def main_login_page():
    return render_template('main_login_page.html')

@auth_bp.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        user = current_app.db.users.find_one({
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "role": "admin"
        })
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('admin.admin_home'))
        else:
            error = "Invalid username or password. Please try again."
    return render_template('admin/admin_login.html', error=error)

@auth_bp.route('/login/consultant', methods=['GET', 'POST'])
def consultant_login():
    error = None
    if request.method == 'POST':
        user = current_app.db.users.find_one({
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "role": "consultant"
        })
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user.get('name', user['username'])
            return redirect(url_for('consultant.consultant_home'))
        else:
            error = "Invalid username or password. Please try again."
    return render_template('consultant/consultant_login.html', error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.main_login_page'))
