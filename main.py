from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, Boolean, String, DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_ckeditor import CKEditor
from datetime import datetime
from wtforms.validators import DataRequired
from wtforms.fields.simple import StringField, BooleanField, SubmitField

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_memo.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# database
class ToDo(db.model):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean)


with app.app_context():
    db.create_all()


# Form
class NewTodo(FlaskForm):
    text = StringField("New todo",validators=[DataRequired()])
    submit = SubmitField("Add Todo")

@app.route("/", methods=['GET', 'POST'])
def home():
    form = NewTodo
    if form.validate_on_submit():
        pass
    todo_list = ToDo.qwery.all()
    return render_template("index", form=form, list=todo_list)


if __name__ == "__main__":
    app.run(debug=True)
