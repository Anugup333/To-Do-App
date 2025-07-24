from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from app.models import User
from app import db,get_indian_time

auth_bp  = Blueprint('auth', __name__)



@auth_bp.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username,password=password).first()

        if user:
            session['user'] = username
            user.last_login = get_indian_time()
            db.session.commit()
            flash("Login Successful",'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash("Invalid username or password ",'danger')

    return render_template('login.html')



@auth_bp.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if not user:
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash("Username is already Exists",'danger')

    return render_template('signup.html')



@auth_bp.route('/logout')
def logout():
    session.pop("user",None)
    flash('Logged out ','info')
    return redirect(url_for('auth.login'))