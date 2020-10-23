from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pyodbc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://@' + 'DESKTOP-9EKC071\\SQLEXPRESS' + '/' + 'test' + '?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    receta = db.Column(db.String(70), unique = True)
    descripcion = db.Column(db.String(200))

    def __init__(self, receta, descripcion):
        self.receta = receta
        self.descripcion = descripcion

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'receta', 'descripcion')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many = True)

@app.route('/tasks', methods=['POST'])
def create_task():

    receta = request.json['receta']
    descripcion = request.json['descripcion']

    new_task = Task(receta, descripcion)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_task():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
