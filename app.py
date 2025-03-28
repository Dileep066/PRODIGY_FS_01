from flask import Flask, render_template, request, redirect,flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
app=Flask(__name__)
app.secret_key = "Dileep66$"
bcrypt = Bcrypt(app) 
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///register.db"
db=SQLAlchemy(app)

class register(db.Model):
    
    email = db.Column(db.String(200),primary_key=True)
    password = db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return f"{self.email}-{self.password}"
with app.app_context():
    db.create_all()  
@app.route('/',methods=['POST','GET'])
def start():
    if request.method=="POST":
            email= request.form['email']
            password = request.form['password']
            reg=register.query.filter_by(email=email).first()
            if reg==None:
                messagee="You are not registered"
                return render_template('start.html',message=messagee)
    
            re_pass = reg.password
            is_valid = bcrypt.check_password_hash(re_pass,password)
            if is_valid:
                return redirect(url_for('dashboard',email=email))
            else:
                messagee="You entered incorect Password "
                return render_template('start.html',message=messagee)
    return render_template('start.html')
@app.route('/register',methods=['POST','GET'])
def index1():
    if request.method=="POST":
        email=request.form['email']
        password =request.form['password']
        req_password=request.form['re_password']
        if password==req_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
            regi=register(email=email,password=hashed_password)
            db.session.add(regi)
            db.session.commit()
            msg="You are registered"
            return render_template('start.html',success=msg)
        else:
            messagee="Incorrect passsword Please give correct details"
            
            return render_template('index.html',message=messagee)
    return render_template('index.html')
@app.route('/dashboard/<string:email>',methods=['POST','GET'])
def dashboard(email):
    return render_template('session.html',email=email)
if __name__=="__main__":
    app.run(debug=True,port=8000)