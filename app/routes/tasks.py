from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from app import db,get_indian_time
from app.models import Task,User


tasks_bp = Blueprint('tasks',__name__)


@tasks_bp.route("/")
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(username=session['user']).first()
    tasks = user.tasks

    # tasks = Task.query.filter_by(username=session['user']).all()
    return render_template('tasks.html',tasks=tasks,name=user.username)


@tasks_bp.route('/add',methods = ["POST"])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('app.login'))
    
    title = request.form.get('title')
    if title:
        user_id = User.query.filter_by(username=session['user']).first().id
        new_task = Task(title=title,status='Pending',user_id=user_id,created_at=get_indian_time())
        db.session.add(new_task)
        db.session.commit()
        flash("Task Added successfully ",'success')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>',methods=["POST"])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('app.login'))
    
    task = Task.query.get(task_id)
    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Done"
        else:
            task.status = "Pending"
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete-task/<int:task_id>',methods = ["POST"])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for('app.login'))
    
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task Deleted successfully.",'success')
    else:
        flash("Task not found or unauthorized.", "error")
    return redirect(url_for('tasks.view_tasks'))

