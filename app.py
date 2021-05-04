from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'oh_so_secret'
db = SQLAlchemy(app)


class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  complete =db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Driver(db.Model):
  id = db.Column("id", db.Integer, primary_key=True)
  name = db.Column("name", db.String(50), nullable=False)
  email = db.Column("email", db.String(50), nullable=False)
  password = db.Column("password", db.String(50), nullable=False)
  cardname = db.Column("cardname", db.String(50), nullable=False)
  cardnum = db.Column("cardnum", db.Integer, nullable=False)
  rating = db.Column("rating", db.Integer)

class Rider(db.Model):
  id = db.Column("id", db.Integer, primary_key=True)
  name = db.Column("name", db.String(50), nullable=False)
  email = db.Column("email", db.String(50), nullable=False)
  password = db.Column("password", db.String(50), nullable=False)
  cardname = db.Column("cardname", db.String(50), nullable=False)
  cardnum = db.Column("cardnum", db.Integer, nullable=False)
  
def __repr__(self):
  return '<task%r>' % self.id 

@app.route('/', methods=['POST', 'GET'] )
def index():
  if request.method=="POST":
    if request.form.get("submit_a"):
      return render_template("login.html")
    if request.form.get('submit_b'):
      return redirect('/create')

    if request.form.get('continue_login'):
      print("insdie")
      account_name= request.form.get['name']
      account_email= request.form['email']
      account_pass = request.form['password']
      session["name"] = account_name
      session["email"] = account_email
      session["password"] = account_pass
      #print("account name" + account_name)
      #print("account email" + account_email)  
      #print("account pass" + account_pass)  
      #print(session["name"])
      #print(session["email"])
      #print(session["password"])
  else:
    return render_template('index.html')

@app.route('/loginpage/', methods=['POST', "GET"])
def login():
  if request.method=="GET":
    return render_template('login.html')
  if request.method=="POST":
    em=request.form["email"]
    print(em)
    passw=request.form['password']
    print(passw)
    def validate_login(db,username, password):
      sql_string="select id,email,password from Rider;"
      results= db.engine.execute(sql_string)
      for row in results:
          user_id=row.id
          #pdb.set_trace()
          if username == row.email and password == row.password:
              return user_id
      return 0
    user_id=validate_login(db, em,passw)
    print("user id"+ str(user_id))
    if user_id==0:
      print("invalid user")
      return render_template('login.html')
    else:
      return render_template('requestride.html')
    


@app.route('/create/', methods=["POST", "GET"])
def create():
  if request.method=="GET":
    return render_template('create.html')
  if request.method=="POST":
    print("init")
    account_name= request.form['name']
    account_email= request.form['email']
    account_pass = request.form['password']
    cardname = request.form['cardname']
    cardnum = request.form['cardnumber']
    session["name"] = account_name
    session["email"] = account_email
    session["password"] = account_pass
    print("account name" + account_name)
    print("account email" + account_email)  
    print("account pass" + account_pass)  
    print("card name" + cardname) 
    print("nard num" + cardnum) 
    print(session["password"])
    if request.form.get('rider'):
      new_rider=Rider(name=account_name, email=account_email, password=account_pass,cardname=cardname, cardnum=cardnum)
      try:
        db.session.add(new_rider)
        db.session.commit()
        print('rider added')
      except:
        return 'There was an issue adding rider'

    if request.form.get('driver'):
      new_driver=Driver(name=account_name, email=account_email, password=account_pass,cardname=cardname, cardnum=cardnum, rating=0)
      try:
        db.session.add(new_driver)
        db.session.commit()
        print('driver added')
      except:
        return 'There was an issue adding your driver'
  print("before riders next")
  sql_string3="select * from Rider;"
  resultsRider= db.engine.execute(sql_string3)
  for row in resultsRider:
    print(row)
  sql_string2="select * from Driver;"
  resultsDriver= db.engine.execute(sql_string2)
  for row in resultsDriver:
    print(row)
  print("after")

  return redirect(url_for('login'))

@app.route('/createcont/', methods=['POST'])
def createtwo():
  if request.method=="GET":
    return render_template("create2.html")
  if request.method=="POST":
    pass
    if request.form['rider'].checked:
      new_rider=Rider(name=name, email=email, password=password,cardname=cardname, cardnum=cardnum)
      try:
        db.session.add(new_rider)
        db.session.commit()
        print('rider added')
      except:
        return 'There was an issue adding rider'

    if request.form['driver'].checked:
      new_driver=Driver(name=name, email=email, password=password,cardname=cardname, cardnum=cardnum, rating=0)
      try:
        db.session.add(new_driver)
        db.session.commit()
        print('driver added')
      except:
        return 'There was an issue adding your driver'

  print("before riders next")
  sql_string3="select * from Rider;"
  resultsRider= db.engine.execute(sql_string3)
  for row in resultsRider:
    print(row)
  sql_string2="select * from Driver;"
  resultsDriver= db.engine.execute(sql_string2)
  for row in resultsDriver:
    print(row)
  print("after")


def validate_login(db,username, password):
    sql_string="select id,email,password from Rider;"
    results= db.engine.execute(sql_string)
    for row in results:
        user_id=row.id
        #pdb.set_trace()
        if username == row.email and password == row.password:
            return user_id
    return 0
@app.route('/reqride/', methods=['POST'])
def loginnext():
  user_id=validate_login
  if user_id==0:
    return render_template('login.html')
  else:
    return render_template('requestride.html')

@app.route('/choosedriver/', methods=['POST'])
def selectdriver():
  return render_template('choosedriver.html')

@app.route('/confirmride/', methods=['POST'])
def confirmride():
  return render_template('riderconfirmation.html')

if __name__ == "__main__":
  app.run(debug=True)
  

