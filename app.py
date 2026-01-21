from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Student  # Make sure your models.py exists

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Student, int(user_id))

# Create DB tables
with app.app_context():
    db.create_all()

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return redirect(url_for("login"))

# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        if Student.query.filter_by(mobile=mobile).first():
            flash("Mobile number already registered", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        student = Student(
            name=name,
            mobile=mobile,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        student = Student.query.filter_by(mobile=mobile).first()

        if student and check_password_hash(student.password, password):
            login_user(student)
            return redirect(url_for("student_dashboard"))

        flash("Invalid mobile or password", "danger")

    return render_template("login.html")

# -------- LOGOUT --------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -------- STUDENT DASHBOARD --------
@app.route("/student_dashboard")
@login_required
def student_dashboard():
    return render_template("student_dashboard.html")

# -------- UPDATE GPS LOCATION --------
@app.route("/update_location", methods=["POST"])
@login_required
def update_location():
    data = request.get_json()  # or request.json
    current_user.latitude = data.get("latitude")
    current_user.longitude = data.get("longitude")
    db.session.commit()
    return jsonify({"status": "success"})

# -------- ADMIN DASHBOARD --------
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

# -------- ALL STUDENT LOCATIONS --------
@app.route("/student_locations")
def student_locations():
    students = Student.query.all()
    locations = []

    for s in students:
        if s.latitude and s.longitude:
            locations.append({
                "name": s.name,
                "mobile": s.mobile,
                "lat": s.latitude,
                "lng": s.longitude
            })

    return jsonify(locations)

# -------- RUN --------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
