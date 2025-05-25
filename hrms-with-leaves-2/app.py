from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    leaves = LeaveRequest.query.order_by(LeaveRequest.id.desc()).all()
    return render_template('index.html', employees=employees, leaves=leaves)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    department = request.form['department']
    salary = int(request.form['salary'])
    new_emp = Employee(name=name, department=department, salary=salary)
    db.session.add(new_emp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/leave', methods=['POST'])
def request_leave():
    employee_id = int(request.form['employee_id'])
    leave_type = request.form['leave_type']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    leave = LeaveRequest(
        employee_id=employee_id,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(leave)
    db.session.commit()
    return redirect(url_for('index'))