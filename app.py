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
    kind="none"
    def validate_login(db,username, password):
      sql_string="select id,email,password from Rider;"
      results= db.engine.execute(sql_string)
      for row in results:
          #user_id=row.id
          if username == row.email and password == row.password:
            return "rider"
            #return user_id
      sql_stringdriver="select id,email,password from Driver;"
      resultsdriver= db.engine.execute(sql_stringdriver)
      for row in resultsdriver:
          #user_id=row.id
          if username == row.email and password == row.password:
            return "driver"
            #return user_id
      return 0
    user_id = validate_login(db, em,passw)
    print("user id "+ str(user_id))
    if user_id=="rider":
      return redirect(url_for('loginnext'))
    if user_id =="driver":
      return redirect(url_for('potential'))
    else:
      print("invalid user")
      return render_template('login.html')
    
    


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



@app.route('/reqride/', methods=['POST', 'GET'])
def loginnext():
  if request.method=="GET":
    return render_template('requestride.html')
  if request.method=="POST":
    return redirect(url_for('selectdriver'))

@app.route('/potential/', methods=['POST', "GET"])
def potential():
  if request.method=="GET":
    return render_template('potentialride.html')
  if request.method=="POST":
    return redirect(url_for('selectrider'))
  
@app.route('/chooserider/', methods=['POST', "GET"])
def selectrider():
  if request.method=="GET":
    return render_template('chooserider.html')
  if request.method=="POST":
    return redirect(url_for('confirmpass'))

@app.route('/confirmpass/', methods=['POST', "GET"])
def confirmpass():
  if request.method=="GET":
    return render_template('driverconfirmation.html')
  if request.method=="POST":
    pass

@app.route('/choosedriver/', methods=['POST', "GET"])
def selectdriver():
  if request.method=="GET":
    return render_template('choosedriver.html')
  if request.method=="POST":
    return redirect(url_for('confirmride'))

@app.route('/confirmride/', methods=['POST', "GET"])
def confirmride():
  if request.method=="GET":
    return render_template('riderconfirmation.html')
  if request.method=="POST":
    return redirect(url_for('ratedriver'))

@app.route('/rate/', methods=['POST', "GET"])
def ratedriver():
  if request.method=="GET":
    return render_template('rateride.html')
  if request.method=="POST":
    pass


if __name__ == "__main__":
  app.run(debug=True)
  