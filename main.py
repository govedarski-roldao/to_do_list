from tkinter.font import names

from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap5(app)


if __name__ == "__main__":
    app.run(debug=True)
