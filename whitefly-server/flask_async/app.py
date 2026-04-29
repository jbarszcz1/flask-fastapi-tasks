import os
from flask import Flask, render_template, request, redirect, url_for, flash
from asgiref.wsgi import WsgiToAsgi
from models import db, User
from tasks import insert_user_task

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'scrtkey'

db.init_app(app)


@app.before_request
def init_db():
    if not getattr(app, '_db_initialized', False):
        db.create_all()
        app._db_initialized = True

asgi_app = WsgiToAsgi(app)


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')

        if not name or not surname:
            flash("All fields are required!", "error")
            return redirect(url_for('main'))

        task = insert_user_task.delay(name, surname)
        try:
            result_message = task.get(timeout=5)
            category = "success" if "successfully" in result_message else "error"
            flash(result_message, category)
        except Exception:
            flash("Task is still processing in the background...", "info")

        return redirect(url_for('main'))

    users = User.query.order_by(User.id.desc()).limit(10).all()
    return render_template('index.html', users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
