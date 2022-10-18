from venv import create
from flask import Flask , render_template , request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    firstname = db.Column(db.String(100) , nullable = False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone = True), server_default = func.now())
    classes  = db.relationship("Class" , back_populates = "student")

    def __repr__(self):
        return f'<Student{self.firstname}>'


class Class(db.Model):
    id = db.Column (db.Integer , primary_key = True)
    name = db.Column (db.String(200) , nullable = False)
    credit = db.Column(db.Integer , nullable= False)
    student_id = db.Column ( db.Integer , db.ForeignKey("student.id"))
    student = db.relationship("Student" , back_populates = "classes")


@app.route("/")
def index():
    students = Student.query.all()
    return render_template('index.html' , students = students)

@app.route("/alunos")
def alunos():
    filtro = "a%"
    students = Student.query.filter(Student.firstname.like(filtro)).all()   
    return render_template('alunos.html' , students = students)
