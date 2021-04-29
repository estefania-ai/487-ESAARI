from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  complete =db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
  return '<task%r>' % self.id 

@app.route('/', methods=['POST', 'GET'] )

def index():
  if request.method=="POST":
    pass
  else:
    pass
  return render_template('index.html')

@app.route('/loginpage/')
def login():
  return render_template('login.html')

@app.route('/create/')
def create():
  if request.method=="POST":
    pass
  return render_template('create.html')

@app.route('/reqride/')
def loginnext():
  return render_template('requestride.html')

if __name__ == "__main__":
  app.run(debug=True)



