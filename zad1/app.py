from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'scrtkey'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(100), nullable=False)

    @validates('name', 'surname')
    def validate_names(self, key, value):
        if any(char.isdigit() for char in value):
            raise ValueError(f"Field '{key}' cannot contain numbers!")
        return value


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')

        if not name or not surname:
            flash("All fields are required!")
            return redirect(url_for('main'))

        try:
            new_user = User(name=name, surname=surname)
            db.session.add(new_user)
            db.session.commit()
            flash("Data saved successfully!")
        except ValueError as e:
            db.session.rollback()
            flash(str(e))
        except Exception:
            db.session.rollback()
            flash("A database error occurred.")

        return redirect(url_for('main'))

    users = User.query.all()
    return render_template('index.html', users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
