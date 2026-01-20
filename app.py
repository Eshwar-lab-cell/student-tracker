from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Student
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Student, int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        mobile = request.form['mobile']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        student = Student(name=name, mobile_number=mobile, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash("Registered successfully! Please login.", "success")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form['mobile']
        password = request.form['password']
        student = Student.query.filter_by(mobile_number=mobile).first()
        if student and check_password_hash(student.password, password):
            login_user(student)
            return redirect(url_for("student_dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/student_dashboard")
@login_required
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/update_location", methods=["POST"])
@login_required
def update_location():
    data = request.json
    current_user.lat = data["latitude"]
    current_user.lng = data["longitude"]
    db.session.commit()
    return jsonify({"status": "success"})

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/student_locations")
def student_locations():
    students = Student.query.all()
    data = []
    for s in students:
        if s.lat and s.lng:
            data.append({
                "name": s.name,
                "mobile": s.mobile_number,
                "lat": s.lat,
                "lng": s.lng
            })
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
