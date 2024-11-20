import os.path
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = "./static"
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Surfboard(db.Model):
    __tablename__ = 'surfboards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    length = db.Column(db.String(80), nullable=True)
    width = db.Column(db.String(80), nullable=True)
    thickness = db.Column(db.String(80), nullable=True)
    volume = db.Column(db.String(80), nullable=True)
    image_filename = db.Column(db.String(80), unique=False, nullable=False)
    reviews = db.relationship('Review', backref='surfboard', lazy=True)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    surfboard_id = db.Column(db.Integer, db.ForeignKey('surfboards.id'), nullable=False)

@app.route('/')
def homepage():
    surfboards = Surfboard.query.all()
    return render_template("homepage.html", surfboards=surfboards)

@app.route("/surfboard/<int:surfboard_id>", methods=['GET', 'POST'])
def surfboard(surfboard_id):
    surfboard = Surfboard.query.get_or_404(surfboard_id)
    if request.method == 'POST':
        author = request.form['author']
        content = request.form['content']
        new_review = Review(author=author, content=content, surfboard=surfboard)
        db.session.add(new_review)
        db.session.commit()
        return redirect(f'/surfboard/{surfboard_id}')
    return render_template("description.html", surfboard=surfboard)

@app.route("/insert", methods=['GET', 'POST'])
def insert_board():
    if request.method == 'POST':
        title = request.form.get("title")
        length = request.form.get("length")
        width = request.form.get("width")
        thickness = request.form.get("thickness")
        volume = request.form.get("volume")
        file = request.files.get("image_filename")
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        surfboard = Surfboard(title=title, length=length, width=width, thickness=thickness, volume=volume, image_filename=filename)
        db.session.add(surfboard)
        db.session.commit()
        surfboards = Surfboard.query.all()
        return render_template("homepage.html", surfboards=surfboards)
    elif request.method == 'GET':
        return render_template("insert_board.html")


if __name__ == '__main__':
    app.run(debug=True)

