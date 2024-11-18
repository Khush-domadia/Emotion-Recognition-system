from flask import request, redirect, render_template,session,flash
from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.vo.login_vo import LoginVO
import secrets


@app.route('/load_login')
def login_page():
    return render_template("admin/login.html")


@app.route("/admin/index", methods=['POST'])
def login_controller():
    email = request.form.get('email')
    password = request.form.get('password')

    login_dao = LoginDAO()
    login_vo = LoginVO()

    login_vo.login_email = email
    login_vo.login_password = password
    # Validate credentials using LoginDAO
    is_valid_user = login_dao.login_validate_email(
        login_vo)  # Replace with actual validation logic

    if is_valid_user:
        # Generate a secure session key using secrets module
        session_key = secrets.token_urlsafe(32)
        session['user_email'] = email  # Store only necessary user data
        session['session_key'] = session_key

        flash('Login successful!', 'success')
        return render_template("admin/index.html")  # Redirect to authorized
        # area

    else:
        flash('Invalid username or password.', 'danger')
        return redirect('/load_login')