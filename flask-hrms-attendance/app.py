from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    attendance = Attendance.query.all()
    return render_template('index.html', employees=employees, attendance=attendance)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    department = request.form['department']
    salary = request.form['salary']
    new_employee = Employee(name=name, department=department, salary=int(salary))
    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/checkin/<int:id>')
def checkin(id):
    record = Attendance(employee_id=id, check_in=datetime.now())
    db.session.add(record)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/checkout/<int:id>')
def checkout(id):
    record = Attendance.query.filter_by(employee_id=id).order_by(Attendance.id.desc()).first()
    if record and not record.check_out:
        record.check_out = datetime.now()
        db.session.commit()
    return redirect(url_for('index'))