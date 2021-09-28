#Import Flask
from flask import Flask, jsonify, request

#Import SQLAlchemy for Flask
from flask_sqlalchemy import SQLAlchemy

#Serialization 
from flask_marshmallow import Marshmallow

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Configurations

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# DATABASE ---------------------------------------------------------------------

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    todo_type = db.Column(db.Text())
    description = db.Column(db.Text())
    deadline = db.Column(db.Text())

    def __repr__(self):
      return f"{self.name} - {self.todo_type} - {self.description} - {self.deadline}"

    def __init__(self, name, todo_type, description, deadline):
      self.name = name
      self.todo_type = todo_type
      self.description = description
      self.deadline = deadline

class ToDoSchema(ma.Schema):
  class Meta:
    #Fields we want to serialise
    fields = ('id', 'name', 'type', 'description', 'deadline')

todo_schema = ToDoSchema()
todos_schema = ToDoSchema(many=True)


todos_list = [
        {
        "name": "Do Laundry",
        "type": "Delegate",
        "description": "Get my mom to wash my pants", 
        "deadline": "17th December", 
      },
       {
        "name": "Finish Todo App",
        "type": "Do",
        "description": "Create a full stack application with Python and Vue.js", 
        "deadline": "25th September", 
     },
  ]

# METHODS -------------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def user():

  # GET ---------------------------------------------------------------------------------------
  if request.method == 'GET':
    print('GET')
    #IF DB IS SET UP -------------------------
    # all_todos = Todos.query.all()
    # results = todos_schema.dump(all_todos)
    # return jsonify(results)

    # WITHOUT DB ------------------------------
    return jsonify(todos_list)
  # GET ---------------------------------------------------------------------------------------




  # POST --------------------------------------------------------------------------------------
  if request.method == 'POST':
    data = request.json

    # WITH DB -------------------------------
    # todo = Todos(data['name'], data['type'], data['description'], data['deadline'])
    # db.session.add(todo)
    # db.session.commit()
    # return todo_schema.jsonify(todo)
    
    # WITHOUT DB -----------------------------
    todos_list.append(data)
    return jsonify(todos_list)
  # POST --------------------------------------------------------------------------------------






  # DELETE ------------------------------------------------------------------------------------
  if request.method == 'DELETE':
    todo_id = int(request.data.decode("utf-8"))

    # WITH DB -------------------------------
    # todo = Todos.query.get(todo_id)
    # db.session.delete(todo)
    # db.session.commit()
    # return todo_schema.jsonify(todo)
    
    # WITHOUT DB ---------------------------
    del todos_list[todo_id]
    return jsonify(todos_list)
  # DELETE ------------------------------------------------------------------------------------





# @app.route('/add', methods=['POST'])
# def add_todo():
#   print('POSTED')
#   title = request.json['title']
#   description = request.json['description']
#   todo_type = request.json['todo_type']
#   deadline = request.json['deadline']

#   todos = Todos(title, todo_type, description, deadline)
#   return jsonify(todos)
  # db.session.add(todos)
  # db.session.commit()
  #return todo_schema.jsonify(todos)

  # return jsonify(
  #   {
  #     "Test":"Icles"
  #   }
  # )

# @app.route('/delete/<id>/', methods=['DELETE'])
# def todo_delete(id): 
#   todo = Todos.query.get(id)
#   db.session.delete(todo)
#   db.session.commit()

#   return todo_schema.jsonify(todo)


if __name__ == '__main__':
  app.run(debug=True)