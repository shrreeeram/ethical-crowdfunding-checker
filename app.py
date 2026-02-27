from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)

# ------------------ CONFIG ------------------

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# ------------------ MODELS ------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    trust_score = db.Column(db.Integer)
    status = db.Column(db.String(20))

# ------------------ CREATE TABLES (IMPORTANT FIX) ------------------

with app.app_context():
    db.create_all()

# ------------------ LOGIN MANAGER ------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ TRUST SCORE ------------------

def calculate_trust_score(amount, address, description):
    score = 100

    if amount > 100000:
        score -= 30

    if not address or len(address) < 10:
        score -= 20

    suspicious_words = ["urgent", "double money", "guaranteed return"]

    for word in suspicious_words:
        if word in description.lower():
            score -= 15

    return max(score, 0)

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    description = request.form["description"]
    amount = int(request.form["amount"])
    address = request.form["address"]

    trust_score = calculate_trust_score(amount, address, description)
    status = "Approved" if trust_score >= 70 else "Potential Fraud"

    new_campaign = Campaign(
        name=name,
        description=description,
        amount=amount,
        address=address,
        trust_score=trust_score,
        status=status
    )

    db.session.add(new_campaign)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/admin")
@login_required
def admin():
    campaigns = Campaign.query.all()
    return render_template("admin.html", campaigns=campaigns)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("admin"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)