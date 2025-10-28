from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/demo_login"
app.config["SECRET_KEY"]="patata123"
db=SQLAlchemy(app)

class Users (db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username =db.Column(db.String(150),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)

# Mostra directament el registre
@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("login"))

# Formulari de registre
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            flash("Cal usuari i contrasenya.", "error")
            return render_template("register.html")

        if Users.query.filter_by(username=username).first():
            flash("L’usuari ja existeix.", "error")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        db.session.add(Users(username=username, password=hashed))
        db.session.commit()
        flash("Usuari creat correctament!", "success")
        return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username= request.form.get("username","").strip()
        password= request.form.get("password","")
        user= Users.query.filter_by(username=username).first()
        if not user:
            flash("el usuario no existe","")
            return render_template("login.html")
        if not check_password_hash(user.password,password):
            flash ("contraseña incorrecta","error")
        else:
            session["user"]=user.username
            return redirect(url_for("dashboard"))
    return render_template("login.html")     

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html",username=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

