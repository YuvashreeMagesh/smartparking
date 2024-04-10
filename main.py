from flask import Flask,render_template,request,session,redirect,url_for,flash from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash from flask_login import login_user,logout_user,login_manager,LoginManager from flask_login import login_required,current_user
from flask_mail import Mail import json
from datetime import datetime

with open('config.json','r') as c: params = json.load(c)["params"]
 

# MY db connection local_server= True app = Flask( name ) app.secret_key='abc'


# this is for getting unique user access login_manager=LoginManager(app) login_manager.login_view='login'

# SMTP MAIL SERVER SETTINGS

app.config.update( MAIL_SERVER='smtp.gmail.com', MAIL_PORT='465', MAIL_USE_SSL=True,
MAIL_USERNAME=params['gmail-user'], MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)


@login_manager.user_loader def load_user(user_id):
return User.query.get(int(user_id))

#
app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/dat abas_table_name' app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:xyzabc@localhost/spa' db=SQLAlchemy(app)

class User(UserMixin,db.Model): id=db.Column(db.Integer,primary_key=True) username=db.Column(db.String(50)) email=db.Column(db.String(50),unique=True) password=db.Column(db.String(1000))

class booking(db.Model): uid=db.Column(db.Integer,primary_key=True) email=db.Column(db.String(50)) name=db.Column(db.String(50)) vtype=db.Column(db.String(50)) slot=db.Column(db.String(50)) date=db.Column(db.String(50),nullable=False) vehicle=db.Column(db.String(50)) number=db.Column(db.String(50))
 
class Trigr(db.Model): tid=db.Column(db.Integer,primary_key=True) uid=db.Column(db.Integer) email=db.Column(db.String(50)) name=db.Column(db.String(50)) action=db.Column(db.String(50)) timestamp=db.Column(db.String(50))






# here we will pass endpoints and run the fuction @app.route('/')
def index():
a=params['gmail-user']
return render_template('index.html')



@app.route('/aboutus',methods=['POST','GET']) def doctors():

return render_template('aboutus.html')



@app.route('/booking',methods=['POST','GET']) @login_required
def booking(): maxSlot=3 f=0
if request.method=="POST": email=request.form.get('email') name=request.form.get('name') vtype=request.form.get('vtype') slot=request.form.get('slot') date=request.form.get('date') vehicle=request.form.get('vehicle') number=request.form.get('number') subject="SMART PARKING APPLICATION"
q1=db.engine.execute(f"SELECT (`vtype`) FROM `booking`") r1=q1.fetchall()
q2=db.engine.execute(f"SELECT (`date`) FROM `booking`") r2=q2.fetchall()
q3=db.engine.execute(f"SELECT (`slot`) FROM `booking`") r3=q3.fetchall()
q5=db.engine.execute(f"SELECT `vtype`, `slot`,`date` FROM `booking`") r5=q5.fetchall()
 

t=(vtype,slot,datetime.strptime(date,'%Y-%m-%d').date()) c=0
for i in r5:
if(i==t):
c+=1


t=(email,name,vtype,slot,date,vehicle,number) q4=db.engine.execute(f"SELECT
`email`,`name`,`vtype`,`slot`,`date`,`vehicle`,`number` FROM `booking`") r4=q4.fetchall()
for i in r4:
if t==i:
f+=1


if(c<maxSlot and f==0): query=db.engine.execute(f"INSERT INTO `booking`
(`email`,`name`,`vtype`,`slot`,`date`,`vehicle`,`number`) VALUES ('{email}','{name}','{vtype}','{slot}','{date}','{vehicle}','{number}')")
flash("Booking Confirmed","info") else:
flash("Not Available","danger") return render_template('booking.html')


@app.route('/booked') @login_required
def bookings(): em=current_user.email
query=db.engine.execute(f"SELECT * FROM `booking` WHERE email='{em}'") return render_template('booked.html',query=query)


@app.route("/edit/<string:uid>",methods=['POST','GET']) @login_required
def edit(uid): posts=booking.query.filter_by(uid=uid).first() if request.method=="POST":
email=request.form.get('email') name=request.form.get('name') vtype=request.form.get('vtype') slot=request.form.get('slot') date=request.form.get('date') vehicle=request.form.get('vehicle') number=request.form.get('number')
 
db.engine.execute(f"UPDATE `booking` SET `email` = '{email}', `name` = '{name}', `vtype` = '{vtype}', `slot` = '{slot}', `date` = '{date}', `vehicle`
= '{vehicle}', `number` = '{number}' WHERE `booking`.`uid` = {uid}") flash("Slot is Updates","success")
return redirect('/booked')

return render_template('edit.html',posts=posts)


@app.route("/delete/<string:uid>",methods=['POST','GET']) @login_required
def delete(uid):
db.engine.execute(f"DELETE FROM `booking` WHERE `booking`.`uid`={uid}") flash("Slot Deleted Successful","danger")
return redirect('/booked')
@app.route('/signup',methods=['POST','GET']) def signup():
if request.method == "POST": username=request.form.get('username') email=request.form.get('email') password=request.form.get('password') user=User.query.filter_by(email=email).first() if user:
flash("Email Already Exist","warning") return render_template('/signup.html')
encpassword=generate_password_hash(password)

new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

flash("Signup Success Please Login","success") return render_template('login.html')

return render_template('signup.html')

@app.route('/login',methods=['POST','GET']) def login():
if request.method == "POST": email=request.form.get('email') password=request.form.get('password') user=User.query.filter_by(email=email).first()

if user and check_password_hash(user.password,password): login_user(user)
flash("Login Success","primary") return redirect(url_for('index'))
 
else:
flash("invalid credentials","danger") return render_template('login.html')
return render_template('login.html') @app.route('/logout')
@login_required
def logout():
logout_user()
flash("Logout SuccessFul","warning") return redirect(url_for('login'))



@app.route('/details') @login_required
def details():
# posts=Trigr.query.all() posts=db.engine.execute("SELECT * FROM `trigr`") return render_template('trigers.html',posts=posts)


app.run(debug=True)
