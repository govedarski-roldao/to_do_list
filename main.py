from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, Boolean, String, DATETIME, desc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_ckeditor import CKEditor
from datetime import datetime
from wtforms.validators import DataRequired
from wtforms.fields.simple import StringField, BooleanField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_memo.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# database
class ToDo(db.Model):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean)


with app.app_context():
    db.create_all()


# Form
class NewTodo(FlaskForm):
    text = StringField("New todo", validators=[DataRequired()])
    submit = SubmitField("Add Todo")


@app.route("/", methods=['GET', 'POST'])
def home():
    form = NewTodo()
    if form.validate_on_submit():
        new_todo = ToDo(
            message=form.text.data,
            done=0
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    todo_list = ToDo.query.order_by(desc(ToDo.id)).all()
    return render_template("index.html", form=form, list=todo_list)


@app.route("/done/<int:id>", methods=['GET', 'POST'])
def mark_as_done(id):
    todo = ToDo.query.get(id)
    todo.done = 1
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_done(id):
    post_to_delete = db.get_or_404(ToDo, id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
