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

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    check_in = db.Column(db.DateTime, default=datetime.utcnow)
    check_out = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    attendance = Attendance.query.order_by(Attendance.id.desc()).all()
    return render_template('index.html', employees=employees, attendance=attendance)

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

@app.route('/checkin/<int:id>')
def checkin(id):
    record = Attendance(employee_id=id)
    db.session.add(record)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/checkout/<int:id>')
def checkout(id):
    record = Attendance.query.filter_by(employee_id=id, check_out=None).order_by(Attendance.id.desc()).first()
    if record:
        record.check_out = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)