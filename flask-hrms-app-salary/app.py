from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

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

if __name__ == '__main__':
    app.run(debug=True)
